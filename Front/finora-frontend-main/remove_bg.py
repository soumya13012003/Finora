"""
Remove white background from the Finora logo.jpg and save as transparent logo.png.
Usage: python remove_bg.py
"""
from PIL import Image
import os

script_dir = os.path.dirname(os.path.abspath(__file__))
input_path = os.path.join(script_dir, "public", "logo.jpg")
output_path = os.path.join(script_dir, "public", "logo.png")

img = Image.open(input_path).convert("RGBA")
pixels = img.load()

# Replace white/near-white pixels with transparent
threshold = 235  # pixels with R,G,B all above this become transparent
for y in range(img.height):
    for x in range(img.width):
        r, g, b, a = pixels[x, y]
        if r >= threshold and g >= threshold and b >= threshold:
            pixels[x, y] = (r, g, b, 0)  # fully transparent
        # Also handle very light gray edges with partial transparency
        elif r >= 220 and g >= 220 and b >= 220:
            # Fade out near-white pixels for smoother edges
            avg = (r + g + b) / 3
            alpha = int((235 - avg) / (235 - 220) * 255)
            pixels[x, y] = (r, g, b, max(0, min(255, alpha)))

# Crop to content (remove empty transparent borders)
bbox = img.getbbox()
if bbox:
    img = img.crop(bbox)

img.save(output_path, "PNG")
print(f"Done! Saved transparent logo to: {output_path}")
print(f"Size: {img.width}x{img.height}")
