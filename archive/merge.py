from PIL import Image, ImageEnhance, ImageFilter
from PIL import ImageFont
from PIL import ImageDraw 
from pathlib import Path

# Define images and names
path1 = 'images/Dog.png'
path2 = 'images/Cat.png'
im1 = Image.open(path1)
im2 = Image.open(path2)
im1_name = str(Path(path1).stem)
im2_name = str(Path(path2).stem)

print(im1_name)
print(im2_name)

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
main_font = ImageFont.truetype("data/cera.otf", 180)
or_font = ImageFont.truetype("data/cera.otf", 100)

im1_width = 500
im2_width = 1500

anchor = 280
im1_height = anchor
im2_height = anchor

draw.text((im1_width, im1_height),f'"{im1_name}"',(245,147,66),font=top_font,anchor="mm")
draw.text((im2_width, im2_height),f'"{im2_name}"',(245,147,66),font=top_font,anchor="mm")
draw.text((im1_width, im1_height*1.45),'has',(255,255,255),font=small_font,anchor="mm")
draw.text((im2_width, im2_height*1.45),'has',(255,255,255),font=small_font,anchor="mm")
draw.text((im1_width, im1_height*2),im1_results,(245,198,69),font=main_font,anchor="mm")
#draw.text((im2_width, im2_height*1.5),im2_results,(245,198,69),font=main_font,anchor="mm")
draw.text((im1_width, im1_height*2.5),'results on the internet',(255,255,255),font=small_font,anchor="mm")
draw.text((im2_width, im2_height*2.5),'results on the internet',(255,255,255),font=small_font,anchor="mm")
draw.text((im2_width, im2_height*1.95),'or',(245,198,69),font=or_font,anchor="mm")


# Add VS
vs = Image.open('data/vs.png').convert("RGBA")
vs = vs.resize((128, 128))
dst.paste(vs, (936,470), mask = vs)

# Add arrows
up = Image.open('data/up_arrow.png').convert("RGBA")
down = Image.open('data/down_arrow.png').convert("RGBA")
up = up.resize((170, 170))
down = down.resize((170, 170))
dst.paste(up, (1216,int(im2_height*1.65)), mask = up)
dst.paste(down, (1616,int(im2_height*1.65)), mask = down)

dst.show()
dst.save('out.png')



# OLD CODE
# top_font = ImageFont.truetype("data/cera.otf", 140)
# small_font = ImageFont.truetype("data/cera.otf", 70)
# main_font = ImageFont.truetype("data/cera.otf", 190)

# draw.text((1000/2, 770/2),f'"{im1_name}"',(245,147,66),font=top_font,anchor="mm")
# draw.text((3000/2, 770/2),f'"{im2_name}"',(245,147,66),font=top_font,anchor="mm")
# draw.text((1000/2, 930/2),'has',(255,255,255),font=small_font,anchor="mm")
# draw.text((3000/2, 930/2),'has',(255,255,255),font=small_font,anchor="mm")
# draw.text((1000/2, 1100/2),im1_results,(245,198,69),font=main_font,anchor="mm")
# draw.text((3000/2, 1100/2),im2_results,(245,198,69),font=main_font,anchor="mm")
# draw.text((1000/2, 1280/2),'results on the internet',(255,255,255),font=small_font,anchor="mm")
# draw.text((3000/2, 1280/2),'results on the internet',(255,255,255),font=small_font,anchor="mm")