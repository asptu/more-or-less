from PIL import Image, ImageEnhance, ImageFilter
from PIL import ImageFont
from PIL import ImageDraw 
from pathlib import Path

# Define images and names
path1 = 'images/America.png'
path2 = 'images/Toothbrush.png'
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
top_font = ImageFont.truetype("data/cera.otf", 140)
small_font = ImageFont.truetype("data/cera.otf", 70)
main_font = ImageFont.truetype("data/cera.otf", 190)
or_font = ImageFont.truetype("data/cera.otf", 100)

im1_width = 560.2
im2_width = 1685.2

im1_height = 560
im2_height = 560

# Results text
draw.text((im1_width, im1_height),f'"{im1_name}"',(245,147,66),font=top_font,anchor="mm")
draw.text((im2_width, im2_height),f'"{im2_name}"',(245,147,66),font=top_font,anchor="mm")
draw.text((im1_width, im1_height*1.22),'has',(255,255,255),font=small_font,anchor="mm")
draw.text((im2_width, im2_height*1.22),'has',(255,255,255),font=small_font,anchor="mm")
draw.text((im1_width, im1_height*1.5),im1_results,(245,198,69),font=main_font,anchor="mm")
#draw.text((im2_width, im2_height*1.5),im2_results,(245,198,69),font=main_font,anchor="mm")
draw.text((im1_width, im1_height*1.75),'results on the internet',(255,255,255),font=small_font,anchor="mm")
draw.text((im2_width, im2_height*1.75),'results on the internet',(255,255,255),font=small_font,anchor="mm")
draw.text((im2_width, im2_height*1.48),'or',(245,198,69),font=or_font,anchor="mm")

# Add VS
vs = Image.open('data/vs.png').convert("RGBA")
vs = vs.resize((128, 128))
dst.paste(vs, (1062,700), mask = vs)

# Add arrows
up = Image.open('data/up_arrow.png').convert("RGBA")
down = Image.open('data/down_arrow.png').convert("RGBA")
up = up.resize((170, 170))
down = down.resize((170, 170))
dst.paste(up, (1400,750), mask = up)
dst.paste(down, (1800,750), mask = down)



dst.show()
dst.save('out.png')

