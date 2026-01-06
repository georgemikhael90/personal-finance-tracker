"""
Simple script to create a basic application icon
Run this once to generate the icon file
"""

from PIL import Image, ImageDraw, ImageFont
import os

def create_icon():
    """Create a simple icon for the application"""
    # Create a 256x256 image with a green background
    size = 256
    img = Image.new('RGB', (size, size), color='#4caf50')
    draw = ImageDraw.Draw(img)

    # Draw a dollar sign
    # Draw circle background
    circle_margin = 30
    draw.ellipse(
        [circle_margin, circle_margin, size-circle_margin, size-circle_margin],
        fill='#2e7d32',
        outline='#1b5e20',
        width=5
    )

    # Draw dollar sign
    font_size = 140
    try:
        # Try to use a system font
        font = ImageFont.truetype("arial.ttf", font_size)
    except:
        # Fall back to default font
        font = ImageFont.load_default()

    text = "$"
    # Get text size for centering
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]

    position = ((size - text_width) // 2, (size - text_height) // 2 - 10)
    draw.text(position, text, fill='white', font=font)

    # Save as ICO
    icon_dir = os.path.join(os.path.dirname(__file__), 'resources')
    os.makedirs(icon_dir, exist_ok=True)
    icon_path = os.path.join(icon_dir, 'app_icon.ico')

    # Save in multiple sizes for ICO format
    img.save(icon_path, format='ICO', sizes=[(256, 256), (128, 128), (64, 64), (32, 32), (16, 16)])
    print(f"Icon created successfully at: {icon_path}")

if __name__ == '__main__':
    try:
        create_icon()
    except ImportError:
        print("PIL/Pillow not installed. Installing...")
        import subprocess
        subprocess.check_call(['pip', 'install', 'Pillow'])
        create_icon()
