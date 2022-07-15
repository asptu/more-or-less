from PIL import Image, ImageEnhance, ImageFilter
from PIL import ImageFont
from PIL import ImageDraw 
from pathlib import Path

# Define images and names
path1 = 'images/Toothbrush.png'
path2 = 'images/America.png'
im1 = Image.open(path1)
im2 = Image.open(path2)
im1_name = str(Path(path1).stem)
im2_name = str(Path(path2).stem)
im1_results = '6.6 Billion'
im2_results = '5.9 Billion'

# Concatenate
dst = Image.new('RGB', (im1.width + im2.width, im1.height))
dst.paste(im1, (0, 0))
dst.paste(im2, (im1.width, 0))

# Make Darker + Blur
enhancer = ImageEnhance.Brightness(dst)
dst = enhancer.enhance(0.35)
dst = dst.filter(ImageFilter.BoxBlur(3))

# Add text
draw = ImageDraw.Draw(dst)
top_font = ImageFont.truetype("data/cera.otf", 90)
small_font = ImageFont.truetype("data/cera.otf", 30)
main_font = ImageFont.truetype("data/cera.otf", 100)

im1_width = 600
im2_width = 1750

draw.text((im1_width, 770/2),f'"{im1_name}"',(245,147,66),font=top_font,anchor="mm")
draw.text((im2_width, 770/2),f'"{im2_name}"',(245,147,66),font=top_font,anchor="mm")
draw.text((im1_width, 930/2),'has',(255,255,255),font=small_font,anchor="mm")
draw.text((im2_width, 930/2),'has',(255,255,255),font=small_font,anchor="mm")
draw.text((im1_width, 1100/2),im1_results,(245,198,69),font=main_font,anchor="mm")
draw.text((im2_width, 1100/2),im2_results,(245,198,69),font=main_font,anchor="mm")
draw.text((im1_width, 1280/2),'results on the internet',(255,255,255),font=small_font,anchor="mm")
draw.text((im2_width, 1280/2),'results on the internet',(255,255,255),font=small_font,anchor="mm")

# Add VS
vs = Image.open('data/vs.png').convert("RGBA")
vs = vs.resize((128, 128))
dst.paste(vs, (1062,700), mask = vs)

dst.show()
dst.save('out.png')

