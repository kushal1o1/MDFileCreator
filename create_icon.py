from PIL import Image, ImageDraw, ImageFont
import os

# Create a 256x256 image with a transparent background
icon_size = (256, 256)
icon = Image.new('RGBA', icon_size, color=(0, 0, 0, 0))
draw = ImageDraw.Draw(icon)

# Draw a rounded rectangle as background
bg_color = (52, 152, 219)  # Nice blue color
draw.rounded_rectangle([(20, 20), (icon_size[0]-20, icon_size[1]-20)], 
                      radius=30, 
                      fill=bg_color)

# Try to load a font, fall back to default if not available
try:
    # Try to load a bold font if available
    font = ImageFont.truetype("arial.ttf", 120)
except IOError:
    # Fall back to default font
    font = ImageFont.load_default().font_variant(size=120)

# Draw "MD" text in white
text = "MD"
text_color = (255, 255, 255)  # White
text_width, text_height = draw.textbbox((0, 0), text, font=font)[2:4]
position = ((icon_size[0] - text_width) // 2, (icon_size[1] - text_height) // 2 - 10)
draw.text(position, text, fill=text_color, font=font)

# Save as .ico file
icon_path = "md_icon.ico"
icon.save(icon_path, format="ICO")

print(f"Icon created at {os.path.abspath(icon_path)}") 