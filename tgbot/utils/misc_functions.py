from os import listdir
import os
from random import randint
from PIL import Image, ImageFont, ImageDraw

from tgbot.services.api_sqlite import get_file_name_with_template_id
from tgbot.services.api_sqlite import get_all_layers
import qrcode
from qrcode.image.styledpil import StyledPilImage
from qrcode.image.styles.moduledrawers import RoundedModuleDrawer
from qrcode.image.styles.colormasks import RadialGradiantColorMask


async def create_qr_code(url, file_name):
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(url)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    file_url = url.replace(':','').replace('/','')
    qr_path = "tgbot/files/image cache/{}_{}.png".format(file_url,file_name)
    with open(qr_path, 'wb') as f:
        img.save(f)
    return str(url) + ':' + str(file_name)

async def prescreen_func(template_id):
    try:
        qr_codes = []
        file_name = (await get_file_name_with_template_id(template_id))[0]
        layers = get_all_layers(template_id)
        blank_image = Image.open(f'tgbot/files/image source/{file_name}.jpg')
        d = ImageDraw.Draw(blank_image)
        for layer in layers:
            font_name = layer['font']
            text = layer['layer_name']
            cord = layer['coordinates']
            cord_1 = str(cord).split(',')[0]
            cord_2 = str(cord).split(',')[1]
            font_size = layer['font_size']
            if 'https' in text or 'http' in text:
                while True:
                    qr_name = randint(0, 99999999)
                    if os.path.exists('tgbot/files/image cache/{}_{}.png'.format(text,qr_name)):
                        pass
                    else:
                        qr_path = qr_name
                        break
                qr_link = text.split(':')[0] + ':' + text.split(':')[1]
                qr_path = await create_qr_code(qr_link,qr_path)
                qr_path = qr_path.replace('/','')
                parts = qr_path.rsplit(':', 1)
                qr_path = parts[0] + '_' + parts[1]
                qr_path = qr_path.replace(':','')
                im1 = Image.open('tgbot/files/image cache/{}.png'.format(qr_path))   
                im1 = im1.resize((int(font_size), int(font_size)))
                blank_image.paste(im1, (int(cord_1), int(cord_2)))
            else:   
                font_name = ImageFont.truetype(f'tgbot/files/fonts/{font_name}.ttf', int(font_size))
                font_color = layer['font_color']
                if int(layer['align_center']) == 1:
                    d.text((int(cord_1), int(cord_2)), text, font=font_name, fill=font_color, anchor='ma')
                elif int(layer['align_right']) == 1:
                    d.text((int(cord_1), int(cord_2)), text, font=font_name, fill=font_color, anchor='ra')
                else:
                    d.text((int(cord_1), int(cord_2)), text, font=font_name, fill=font_color)
        blank_image.save(f"tgbot/files/image reference/{file_name}.jpg", "PNG")
        for qr in qr_codes:
            os.remove(qr)
        return open(F'tgbot/files/image reference/{file_name}.jpg', 'rb')
    except Exception as e:
        print(e)


async def prescreen_user_func(template_id, file_name, layers_name):
    layers = get_all_layers(template_id)
    blank_image = Image.open(f'tgbot/files/image source/{file_name}.jpg')
    d = ImageDraw.Draw(blank_image)
    i = 0
    qr_codes = []
    for layer in layers:
        font_size = layer['font_size']
        font= layer['font']
        font_time = ImageFont.truetype(f'tgbot/files/fonts/{font}.ttf', int(font_size))
        cord = layer['coordinates']
        font_color = layer['font_color']
        cord_1 = cord.split(',')[0]
        cord_2 = cord.split(',')[1]
        text = layers_name[i]
        if 'https' in text or 'http' in text:
                while True:
                    qr_name = randint(0, 99999999)
                    if os.path.exists('tgbot/files/image cache/{}_{}.png'.format(text,qr_name)):
                        pass
                    else:
                        qr_path = qr_name
                        break
                qr_path = await create_qr_code(text,qr_path)
                qr_path = qr_path.replace('/','')
                parts = qr_path.rsplit(':', 1)
                qr_path = parts[0] + '_' + parts[1]
                qr_path = qr_path.replace(':','')
                qr_path = 'tgbot/files/image cache/{}.png'.format(qr_path)
                im1 = Image.open(qr_path)   
                im1 = im1.resize((int(font_size), int(font_size)))
                blank_image.paste(im1, (int(cord_1), int(cord_2)))
                qr_codes.append(qr_path)
        else:
            if int(layer['align_center']) == 1:
                d.text((int(cord_1), int(cord_2)), text, font=font_time, fill=font_color, anchor='ma')
            elif int(layer['align_right']) == 1:
                d.text((int(cord_1), int(cord_2)), text, font=font_time, fill=font_color, anchor='ra')
            else:
                d.text((int(cord_1), int(cord_2)), text, font=font_time, fill=font_color)
        i += 1
    blank_image.save(f"tgbot/files/image reference/{file_name}.jpg", "PNG")
    for qr in qr_codes:
            os.remove(qr)
    return open(F'tgbot/files/image reference/{file_name}.jpg', 'rb')


def get_all_fonts():
    myList = listdir("tgbot/files/fonts/")
    font_list = []
    for element in myList:
        font_list.append({'font_name': element})
    return font_list

def is_font(font_name):
    if font_name.split('.')[1] == 'ttf':
        myList = listdir("tgbot/files/fonts/")
        if font_name not in myList:
            return True

async def edit_coordinates_pre_check_func(template_id, coordinates):
    file_name = (await get_file_name_with_template_id(template_id))[0]
    tink = Image.open(f'tgbot/files/image source/{file_name}.jpg')
    d = ImageDraw.Draw(tink)
    center = (int(coordinates[0]), int(coordinates[1]))
    radius = 7
    d.ellipse((center[0]-radius, center[1]-radius, center[0]+radius, center[1]+radius), fill='red',outline=(0, 0, 0))
    tink.save(f"tgbot/files/image reference/{file_name}.jpg", "PNG")
    return open(F'tgbot/files/image reference/{file_name}.jpg', 'rb')