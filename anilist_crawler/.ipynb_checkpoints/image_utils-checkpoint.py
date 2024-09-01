from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
from PIL import ImageOps
import requests
from io import BytesIO
import textwrap
import random

def get_char_img(char_imgUrl, char_name, series_name="", max_txt_line = 13, max_seriestxt_line = 30):
    response = requests.get(char_imgUrl)
    img = Image.open(BytesIO(response.content))
    
    img = ImageOps.fit(img, (460//2,700//2))
    W,H = img.size
    fontsize= int((W//10 + H//20) * 2/3)
    font = ImageFont.truetype("honoka.ttf", fontsize)
    
    listTxt_name = textwrap.wrap(char_name, width=max_txt_line)
    
    slicer = 12
    
    i = 0
    draw = ImageDraw.Draw(img)
    
    shadowColor = 'black'
    fillColor = 'white'
    
    listTxt_seriesname = textwrap.wrap(series_name, width=max_seriestxt_line)
    for txt in reversed(listTxt_name):
        _, _, w, h = draw.textbbox((0, 0), txt, font=font)

        x,y = (W-w)/2, (slicer*2-2-len(listTxt_seriesname)-i*2)*(H-h)/(slicer*2)

        # thicker border
        draw.text((x-1, y-1), txt, font=font, fill=shadowColor)
        draw.text((x+1, y-1), txt, font=font, fill=shadowColor)
        draw.text((x-1, y+1), txt, font=font, fill=shadowColor)
        draw.text((x+1, y+1), txt, font=font, fill=shadowColor)

        draw.text((x,y), txt, font=font, fill=fillColor)
        
        i+= 1
        
    
    
    i = 0
    for txt in reversed(listTxt_seriesname):

        fontsize_small = int((W//10 + H//20) * 1/3)
        font_small = ImageFont.truetype("honoka.ttf", fontsize_small)
        _, _, w, h = draw.textbbox((0, 0), txt, font=font_small)
        x,y = (W-w)/2, (slicer*2 - 1-i)*(H-h)/(slicer*2)

        # thicker border
        draw.text((x-1, y-1), txt, font=font_small, fill=shadowColor)
        draw.text((x+1, y-1), txt, font=font_small, fill=shadowColor)
        draw.text((x-1, y+1), txt, font=font_small, fill=shadowColor)
        draw.text((x+1, y+1), txt, font=font_small, fill=shadowColor)

        draw.text((x,y), txt, font=font_small, fill=fillColor)
        
        i+= 1
    
    return img

def concat_images(images, horizontal=True, pad_width = 10, pad_height=10):
    if (horizontal):
        widths, heights = zip(*(i.size for i in images))

        total_width = sum(widths) + pad_width * (len(images) +1)
        max_height = max(heights) + pad_height * 2

        new_im = Image.new('RGB', (total_width, max_height))

        x_offset = pad_width
        y_offset = pad_height
        for im in images:
            new_im.paste(im, (x_offset,y_offset))
            x_offset += im.size[0] + pad_width

        return new_im
    else:
        widths, heights = zip(*(i.size for i in images))

        total_width = max(widths) + pad_width * 2
        max_height = sum(heights) + pad_height * (len(images) +1)

        new_im = Image.new('RGB', (total_width, max_height))

        x_offset = pad_width
        y_offset = pad_height
        for im in images:
            new_im.paste(im, (x_offset,y_offset))
            y_offset += im.size[1] + pad_height

        return new_im


def make_img_grid(listImages, max_horizontal = 3):
    
    listVertical = []
    listHorizontal = []
    for i in range(len(listImages)):
        listHorizontal += [listImages[i]]
        if (i+1)%max_horizontal == 0:
            hor_img = concat_images(listHorizontal, horizontal=True)
            listVertical += [hor_img]    
            listHorizontal = []
        elif (i+1 == len(listImages)):
            hor_img = concat_images(listHorizontal, horizontal=True)
            listVertical += [hor_img] 
            
    fullGrid = concat_images(listVertical, horizontal=False)
            
    return fullGrid
    
    