from PIL import Image, ImageEnhance, ImageFilter
from PIL import ImageFont
from PIL import ImageDraw 
from pathlib import Path
from math import floor
import json
import random

def create():
     
    with open('./results.json') as fp:
        d = json.load(fp)

    rkey1 = random.choice(list(d.keys()))
    rkey2 = random.choice(list(d.keys()))

    while rkey1 == rkey2:
        rkey2 = random.choice(list(d.keys()))

    rkey1_v = d[rkey1]
    rkey2_v = d[rkey2]

    magnitudeDict={0:'', 1:'Thousand', 2:'Million', 3:'Billion', 4:'Trillion', 5:'Quadrillion', 6:'Quintillion', 7:'Sextillion', 8:'Septillion', 9:'Octillion', 10:'Nonillion', 11:'Decillion'}

    def simplify(num):
        num=floor(num)
        magnitude=0
        while num>=1000.0:
            magnitude+=1
            num=num/1000.0
        return(f'{floor(num*100.0)/100.0} {magnitudeDict[magnitude]}')
        
    rkey1_v_formatted = simplify(int(rkey1_v))
    rkey2_v_formatted = simplify(int(rkey2_v))

    with open('./scores.json') as fp:
            scores = json.load(fp)


    if rkey1_v > rkey2_v:
        print(f'{rkey1} is bigger than {rkey2}')
        print(f'{rkey1_v} is bigger than {rkey2_v}')
        scores.update({"lower": 1 + scores['extra_points'],})
        scores.update({"higher": 0,})
        print(rkey1_v)
        print(rkey2_v)


        with open('./scores.json', 'w') as json_file:
            json.dump(scores, json_file, 
                                indent=4,  
                                separators=(',',': '))


    elif rkey1_v < rkey2_v:
        print(f'{rkey2} is bigger than {rkey1}')
        print(f'{rkey2_v} is bigger than {rkey1_v}')
        scores.update({"lower": 0,})
        scores.update({"higher": 1 + scores['extra_points'],})
        print(rkey2_v)
        print(rkey1_v)

        with open('./scores.json', 'w') as json_file:
            json.dump(scores, json_file, 
                                indent=4,  
                                separators=(',',': '))
    else:
        print(f'{rkey2} and {rkey1} are the same')
        scores.update({"lower": 1 + scores['extra_points'],})
        scores.update({"higher": 1 + scores['extra_points'],})

        with open('./scores.json', 'w') as json_file:
            json.dump(scores, json_file, 
                                indent=4,  
                                separators=(',',': '))

    # Define images, names and values
    path1 = f'images/{str(rkey1)}.png'
    path2 = f'images/{str(rkey2)}.png'
    im1 = Image.open(path1)
    im2 = Image.open(path2)
    im1_name = str(Path(path1).stem)
    im1_name = im1_name.replace('-', ' ')
    im2_name = str(Path(path2).stem)
    im2_name = im2_name.replace('-', ' ')

    if '-' in str(rkey1):
        rkey1 = str(rkey1).replace('-', ' ')

    if '-' in str(rkey2):
        rkey2 = str(rkey2).replace('-', ' ')

    im1_results = str(rkey1_v_formatted)
    im2_results = str(rkey2_v_formatted)
    dst = Image.new('RGB', (im1.width + im2.width, im1.height))
    dst.paste(im1, (0, 0))
    dst.paste(im2, (im1.width, 0))

    # Make Darker + Blur
    enhancer = ImageEnhance.Brightness(dst)
    dst = enhancer.enhance(0.35)
    dst = dst.filter(ImageFilter.BoxBlur(3))

    # Add text
    draw = ImageDraw.Draw(dst)
    top_font = ImageFont.truetype("data/cera.otf", 120)
    small_font = ImageFont.truetype("data/cera.otf", 70)
    main_font = ImageFont.truetype("data/cera.otf", 160)
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

    #dst.show()
    dst.save('out.png')

    dst = Image.new('RGB', (im1.width + im2.width, im1.height))
    dst.paste(im1, (0, 0))
    dst.paste(im2, (im1.width, 0))

    # Make Darker + Blur
    enhancer = ImageEnhance.Brightness(dst)
    dst = enhancer.enhance(0.35)
    dst = dst.filter(ImageFilter.BoxBlur(3))

    # Add text
    draw = ImageDraw.Draw(dst)
    top_font = ImageFont.truetype("data/cera.otf", 120)
    small_font = ImageFont.truetype("data/cera.otf", 70)
    main_font = ImageFont.truetype("data/cera.otf", 160)
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
    draw.text((im2_width, im2_height*1.5),im2_results,(245,198,69),font=main_font,anchor="mm")
    draw.text((im1_width, im1_height*1.75),'results on the internet',(255,255,255),font=small_font,anchor="mm")
    draw.text((im2_width, im2_height*1.75),'results on the internet',(255,255,255),font=small_font,anchor="mm")
    #draw.text((im2_width, im2_height*1.48),'or',(245,198,69),font=or_font,anchor="mm")

    # Add VS
    vs = Image.open('data/vs.png').convert("RGBA")
    vs = vs.resize((128, 128))
    dst.paste(vs, (1062,700), mask = vs)

    # Add arrows
    # up = Image.open('data/up_arrow.png').convert("RGBA")
    # down = Image.open('data/down_arrow.png').convert("RGBA")
    # up = up.resize((170, 170))
    # down = down.resize((170, 170))
    # dst.paste(up, (1400,750), mask = up)
    # dst.paste(down, (1800,750), mask = down)

    dst.save('done.png')


