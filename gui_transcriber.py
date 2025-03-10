import tkinter as tk
import threading
import time
import sys
import os
import whisper
import pyaudio
import numpy as np
import threading
import queue
import keyboard
from pynput.keyboard import Controller, Listener as KeyboardListener, Key
from pynput.mouse import Listener as MouseListener
import datetime

# Interface gráfica
class TranscriberGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Real-Time Transcriber")
        self.root.geometry("400x300")
        self.root.resizable(False, False)
        
        # Definir ícone
        try:
            self.root.iconbitmap("microphone.ico")  # Será criado mais tarde
        except:
            pass  # Se o ícone não existir, ignore
        
        # Frame principal
        main_frame = tk.Frame(root, padx=10, pady=10)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Status label
        self.status_var = tk.StringVar()
        self.status_var.set("Carregando modelo Whisper...")
        self.status_label = tk.Label(main_frame, textvariable=self.status_var, font=("Arial", 12))
        self.status_label.pack(pady=10)
        
        # Área de log
        log_frame = tk.Frame(main_frame)
        log_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        log_label = tk.Label(log_frame, text="Log de detecção:", font=("Arial", 10))
        log_label.pack(anchor=tk.W)
        
        # Área de texto com scrollbar
        scrollbar = tk.Scrollbar(log_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.log_text = tk.Text(log_frame, height=10, width=40, yscrollcommand=scrollbar.set)
        self.log_text.pack(fill=tk.BOTH, expand=True)
        self.log_text.config(state=tk.DISABLED)
        
        scrollbar.config(command=self.log_text.yview)
        
        # Botão de parar
        self.stop_button = tk.Button(main_frame, text="Parar", command=self.stop_transcription)
        self.stop_button.pack(pady=10)
        
        # Inicializar variáveis
        self.transcriber = None
        self.is_running = False
        
    def start_transcription(self):
        """Inicia o processo de transcrição em uma nova thread."""
        if not self.is_running:
            self.is_running = True
            self.transcriber = TranscriberThread(self)
            self.transcriber.start()
            
    def stop_transcription(self):
        """Para o processo de transcrição."""
        if self.is_running and self.transcriber:
            self.transcriber.stop()
            self.status_var.set("Transcrição parada.")
            self.is_running = False
            
    def update_status(self, text):
        """Atualiza o texto de status."""
        self.status_var.set(text)
        
    def add_log(self, text):
        """Adiciona texto ao log."""
        self.log_text.config(state=tk.NORMAL)
        self.log_text.insert(tk.END, text + "\n")
        self.log_text.see(tk.END)
        self.log_text.config(state=tk.DISABLED)
        
    def on_closing(self):
        """Função chamada quando a janela é fechada."""
        self.stop_transcription()
        self.root.destroy()
        sys.exit(0)

# Thread que executa a transcrição
class TranscriberThread(threading.Thread):
    def __init__(self, gui):
        super().__init__()
        self.gui = gui
        self.daemon = True
        
        # Flags para controle
        self.running = True
        self.triggered = False
        
        # Inicializar variáveis
        self.TRIGGER_PHRASE = "hey jarvis"
        self.TRIGGER_VARIATIONS = ["hey jarvis", "ei jarvis", "hey service", "hey travis", "a jarvis", "hey jarbas", "hey davis"]
        self.input_lock = threading.Lock()
        self.INPUT_COOLDOWN = 2.0
        self.last_input_time = 0
        self.is_typing = False
        self.acknowledgment_typed = False
        self.audio_queue = queue.Queue()
        self.keyboard_controller = Controller()
        self.LOG_FILE = "whisper_detection_log.txt"
        
        # Audio settings
        self.FORMAT = pyaudio.paInt16
        self.CHANNELS = 1
        self.RATE = 16000
        self.CHUNK = 1024
        self.RECORD_SECONDS = 3
        
    def run(self):
        """Executa o processo de transcrição."""
        self.gui.update_status("Carregando modelo Whisper...")
        self.gui.add_log("Iniciando carregamento do modelo Whisper (large)...")
        
        # Carregar modelo
        try:
            self.model = whisper.load_model("large")
            self.gui.add_log("Modelo Whisper carregado com sucesso!")
        except Exception as e:
            self.gui.add_log(f"Erro ao carregar modelo: {e}")
            self.gui.update_status("Erro ao carregar modelo")
            return
        
        # Configurar keyboard hook
        keyboard.add_hotkey('esc', lambda: self.stop())
        
        # Criar arquivo de log ou adicionar à ele
        with open(self.LOG_FILE, "a", encoding="utf-8") as f:
            f.write(f"\n--- Nova sessão iniciada: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ---\n")
        
        # Iniciar listeners
        self.gui.update_status("Iniciando detecção de teclado e mouse...")
        self.keyboard_listener = KeyboardListener(on_press=self.on_key_press)
        self.mouse_listener = MouseListener(on_click=self.on_mouse_click)
        
        self.keyboard_listener.start()
        self.mouse_listener.start()
        
        # Iniciar threads de gravação e processamento
        self.gui.update_status("Aguardando comando 'Hey Jarvis'...")
        self.gui.add_log("Sistema pronto! Diga 'Hey Jarvis' para ativar.")
        
        # Iniciar threads
        self.record_thread = threading.Thread(target=self.record_audio)
        self.process_thread = threading.Thread(target=self.process_audio)
        
        self.record_thread.start()
        self.process_thread.start()
        
        # Aguardar threads
        self.record_thread.join()
        self.process_thread.join()
        
        # Parar listeners
        self.keyboard_listener.stop()
        self.mouse_listener.stop()
        
        self.gui.update_status("Transcrição finalizada.")
        self.gui.add_log("Sessão encerrada.")
    
    def stop(self):
        """Para a transcrição."""
        self.running = False
        self.gui.add_log("Parando transcrição...")
    
    def log_detection_attempt(self, transcription, trigger_detected=False, detected_phrase=""):
        """Registra tentativas de detecção."""
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] "
        if trigger_detected:
            log_entry += f"DETECTADO ({detected_phrase}): {transcription}"
        else:
            log_entry += f"NÃO DETECTADO: {transcription}"
        
        # Atualizar GUI
        self.gui.add_log(log_entry)
        
        # Escrever no arquivo
        with open(self.LOG_FILE, "a", encoding="utf-8") as f:
            f.write(log_entry + "\n")
    
    def on_key_press(self, key):
        """Callback para quando uma tecla é pressionada."""
        if not self.is_typing:
            with self.input_lock:
                if self.triggered:
                    self.triggered = False
                    self.gui.update_status("Aguardando comando 'Hey Jarvis'...")
                    self.gui.add_log("Teclado detectado. Transcrição pausada.")
                self.last_input_time = time.time()
        return True
    
    def on_mouse_click(self, x, y, button, pressed):
        """Callback para quando o mouse é clicado."""
        if pressed:
            with self.input_lock:
                if self.triggered:
                    self.triggered = False
                    self.gui.update_status("Aguardando comando 'Hey Jarvis'...")
                    self.gui.add_log("Mouse detectado. Transcrição pausada.")
                self.last_input_time = time.time()
        return True
    
    def type_with_flag(self, text):
        """Digita texto com flag para prevenir detecção do próprio teclado."""
        self.is_typing = True
        try:
            self.keyboard_controller.type(text)
        finally:
            self.is_typing = False
    
    def erase_text(self, length):
        """Apaga um número específico de caracteres."""
        self.is_typing = True
        try:
            # Usar backspace
            for _ in range(length):
                self.keyboard_controller.press(Key.backspace)
                self.keyboard_controller.release(Key.backspace)
                time.sleep(0.05)
            
            # Esperar um pouco
            time.sleep(0.1)
        finally:
            self.is_typing = False
    
    def record_audio(self):
        """Grava áudio do microfone em chunks."""
        self.gui.add_log("Iniciando gravação do microfone...")
        p = pyaudio.PyAudio()
        
        # Abrir stream
        stream = p.open(format=self.FORMAT,
                        channels=self.CHANNELS,
                        rate=self.RATE,
                        input=True,
                        frames_per_buffer=self.CHUNK)
        
        self.gui.add_log("Gravação iniciada. Fale ao microfone.")
        
        # Continuar gravando até parar
        while self.running:
            frames = []
            for _ in range(0, int(self.RATE / self.CHUNK * self.RECORD_SECONDS)):
                if not self.running:
                    break
                data = stream.read(self.CHUNK, exception_on_overflow=False)
                frames.append(data)
            
            # Converter dados de áudio e adicionar à fila
            if frames and self.running:
                audio_data = np.frombuffer(b''.join(frames), dtype=np.int16).astype(np.float32) / 32768.0
                self.audio_queue.put(audio_data)
        
        # Limpar
        stream.stop_stream()
        stream.close()
        p.terminate()
        self.gui.add_log("Gravação parada.")
    
    def process_audio(self):
        """Processa chunks de áudio e transcreve usando Whisper."""
        last_text = ""
        
        while self.running or not self.audio_queue.empty():
            if not self.audio_queue.empty():
                # Obter chunk de áudio da fila
                audio_data = self.audio_queue.get()
                
                # Transcrever áudio usando Whisper
                try:
                    # Se não estiver no modo de transcrição ativa, procurar pela trigger phrase
                    if not self.triggered:
                        # Para detecção de trigger, usar modelo geral (sem forçar idioma)
                        result = self.model.transcribe(audio_data, fp16=False)
                        transcription = result["text"].strip().lower()
                        
                        # Verificar se estamos no período de cooldown após input
                        with self.input_lock:
                            cooldown_active = (time.time() - self.last_input_time) < self.INPUT_COOLDOWN
                        
                        # Verificar trigger phrase com detecção melhorada
                        trigger_detected = False
                        detected_phrase = ""
                        
                        # Procurar por todas as variações possíveis do trigger
                        for phrase in self.TRIGGER_VARIATIONS:
                            if phrase in transcription:
                                trigger_detected = True
                                detected_phrase = phrase
                                break
                        
                        # Se não encontrar match exato, tentar detecção aproximada
                        if not trigger_detected:
                            # Verificar se pelo menos a parte "jarvis" foi detectada
                            if "jarvis" in transcription or "travis" in transcription or "jarbas" in transcription or "davis" in transcription:
                                trigger_detected = True
                                detected_phrase = "palavra similar a jarvis"
                        
                        # Registrar tentativa de detecção
                        # Só registra quando estamos tentando detectar o trigger (não no modo de transcrição)
                        self.log_detection_attempt(transcription, trigger_detected, detected_phrase)
                        
                        if trigger_detected and not cooldown_active:
                            self.gui.update_status("Trigger detectado! Transcrição ativada.")
                            self.gui.add_log(f"Trigger detectado! ({detected_phrase}) Iniciando transcrição...")
                            with self.input_lock:
                                self.triggered = True
                            
                            # Digitar "Sim?" como reconhecimento
                            acknowledgment = "Sim?"
                            self.type_with_flag(acknowledgment)
                            self.acknowledgment_typed = True
                            self.gui.add_log("Digitado: 'Sim?'")
                            
                            # Não precisa processar o texto do trigger
                            continue
                    
                    else:
                        # Para transcrição real, forçar português
                        result = self.model.transcribe(audio_data, fp16=False, language="pt", task="transcribe")
                        transcription = result["text"].strip().lower()
                        
                        # Só processar se estiver em modo trigger e tivermos transcrição não vazia
                        if transcription and transcription != last_text:
                            self.gui.add_log(f"Transcrito: {transcription}")
                            
                            # Filtro para frases em inglês indesejadas
                            unwanted_phrases = ["thank you", "thanks", "thank", "you", "obrigado", "obrigada", "thanks for"]
                            for phrase in unwanted_phrases:
                                if phrase in transcription.lower():
                                    transcription = transcription.lower().replace(phrase, "").strip()
                                    self.gui.add_log(f"Removida frase indesejada: '{phrase}'")
                            
                            # Se a transcrição estiver vazia após filtragem, pular
                            if not transcription.strip():
                                self.gui.add_log("Transcrição vazia após filtragem, ignorando")
                                continue
                            
                            # Se digitamos um reconhecimento anteriormente, apagar antes de digitar
                            if self.acknowledgment_typed:
                                # Usar comprimento real do reconhecimento
                                acknowledgment_length = len("Sim?")
                                self.gui.add_log(f"Apagando {acknowledgment_length} caracteres do reconhecimento")
                                self.erase_text(acknowledgment_length)
                                self.acknowledgment_typed = False
                                self.gui.add_log("Reconhecimento apagado")
                            
                            # Debug print antes de digitar
                            self.gui.add_log(f"Digitando: '{transcription + ' '}'")
                            
                            # Digitar a transcrição
                            self.type_with_flag(transcription + " ")
                            
                            last_text = transcription
                except Exception as e:
                    self.gui.add_log(f"Erro de transcrição: {e}")
                    # Garantir que a flag de digitação seja resetada em caso de erro
                    self.is_typing = False
                
                # Pequeno delay para evitar uso excessivo de CPU
                time.sleep(0.1)
            else:
                # Se a fila estiver vazia, esperar um pouco
                time.sleep(0.1)

# Função principal
def main():
    root = tk.Tk()
    app = TranscriberGUI(root)
    
    # Iniciar após um breve delay
    root.after(500, app.start_transcription)
    
    # Configurar função de fechamento
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    
    # Iniciar loop principal
    root.mainloop()

if __name__ == "__main__":
    main() 