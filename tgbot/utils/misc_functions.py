from os import listdir
from PIL import Image, ImageFont, ImageDraw

from tgbot.services.api_sqlite import get_file_name_with_template_id
from tgbot.services.api_sqlite import get_all_layers

async def prescreen_func(template_id):
    try:
        file_name = (await get_file_name_with_template_id(template_id))[0]
        layers = get_all_layers(template_id)
        blank_image = Image.open(f'tgbot/files/image source/{file_name}.jpg')
        d = ImageDraw.Draw(blank_image)
        for layer in layers:
            font_name = layer['font']
            text = layer['layer_name']
            font_size = layer['font_size']
            font_name = ImageFont.truetype(f'tgbot/files/fonts/{font_name}.ttf', int(font_size))
            cord = layer['coordinates']
            font_color = layer['font_color']
            cord_1 = cord.split(',')[0]
            cord_2 = cord.split(',')[1]
            if int(layer['align_center']) == 1:
                d.text((int(cord_1), int(cord_2)), text, font=font_name, fill=font_color, anchor='ma')
            elif int(layer['align_right']) == 1:
                d.text((int(cord_1), int(cord_2)), text, font=font_name, fill=font_color, anchor='ra')
            else:
                d.text((int(cord_1), int(cord_2)), text, font=font_name, fill=font_color)
            blank_image.save(f"tgbot/files/image reference/{file_name}.jpg", "PNG")
        return open(F'tgbot/files/image reference/{file_name}.jpg', 'rb')
    except Exception as e:
        print(e)


async def prescreen_user_func(template_id, file_name, layers_name):
    layers = get_all_layers(template_id)
    blank_image = Image.open(f'tgbot/files/image source/{file_name}.jpg')
    d = ImageDraw.Draw(blank_image)
    i = 0
    for layer in layers:
        font_size = layer['font_size']
        font= layer['font']
        font_time = ImageFont.truetype(f'tgbot/files/fonts/{font}.ttf', int(font_size))
        cord = layer['coordinates']
        font_color = layer['font_color']
        cord_1 = cord.split(',')[0]
        cord_2 = cord.split(',')[1]
        if int(layer['align_center']) == 1:
            d.text((int(cord_1), int(cord_2)), layers_name[i], font=font_time, fill=font_color, anchor='ma')
        elif int(layer['align_right']) == 1:
            d.text((int(cord_1), int(cord_2)), layers_name[i], font=font_time, fill=font_color, anchor='ra')
        else:
            d.text((int(cord_1), int(cord_2)), layers_name[i], font=font_time, fill=font_color)
        blank_image.save(f"tgbot/files/image reference/{file_name}.jpg", "PNG")
        i += 1
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
    d.ellipse((int(coordinates[0]), int(coordinates[1]), 111, 111), fill='red', outline=(0, 0, 0))
    tink.save(f"tgbot/files/image reference/{file_name}.jpg", "PNG")
    return open(F'tgbot/files/image reference/{file_name}.jpg', 'rb')