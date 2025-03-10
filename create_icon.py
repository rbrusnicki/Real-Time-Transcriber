from PIL import Image, ImageDraw
import os

def create_microphone_icon():
    """Create a microphone icon and save it as an .ico file"""
    # Create a new image with a white background
    img = Image.new('RGBA', (256, 256), color=(0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    
    # Colors
    main_color = (65, 105, 225)  # Royal Blue
    highlight_color = (30, 144, 255)  # Dodger Blue
    
    # Draw a microphone body
    # Main body
    d.rectangle((96, 56, 160, 160), fill=main_color, outline=highlight_color, width=3)
    
    # Rounded top
    d.ellipse((96, 36, 160, 76), fill=main_color, outline=highlight_color, width=3)
    
    # Stand
    d.rectangle((118, 160, 138, 200), fill=main_color, outline=highlight_color, width=2)
    d.ellipse((98, 190, 158, 230), fill=main_color, outline=highlight_color, width=3)
    
    # Sound waves
    for i in range(3):
        radius = 20 + i * 20
        d.arc((128 - radius, 100 - radius, 128 + radius, 100 + radius), 
              315, 45, fill=highlight_color, width=3)
    
    # Save as ico file
    img.save('microphone.ico')
    
    return os.path.abspath('microphone.ico')

if __name__ == "__main__":
    icon_path = create_microphone_icon()
    print(f"Icon created at: {icon_path}") 