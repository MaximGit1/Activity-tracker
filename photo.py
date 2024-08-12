import os

from PIL import Image, ImageDraw, ImageFont

from config import settings, BASE_DIR
from db_conn import db  # get_all_activities_time

TEMPLATE_DIR = BASE_DIR / 'other-files'
FILES_PATH = TEMPLATE_DIR / 'trash'


def crop_stack_line():  # -> all_cropped.png
    barh_cut = Image.open(f'{FILES_PATH}/barh.png')
    barh_cropped = barh_cut.crop((242, 223, 1727, 391))  # (1920, 1440)
    barh_cropped.save(f'{FILES_PATH}/all_cropped.png')


def crop_general_line():  # -> general_cropped.png
    barh_cut = Image.open(f'{FILES_PATH}/barh.png')
    barh_cropped = barh_cut.crop((242, 1063, 1727, 1231))
    barh_cropped.save(f'{FILES_PATH}/general_cropped.png')


def paste_pie():
    im1 = Image.open(f'{TEMPLATE_DIR}/template.jpg')
    im2 = Image.open(f'{FILES_PATH}/pie.png')
    im1.paste(im2, (-40, -270))
    im1.save(f'{FILES_PATH}/step-1.jpg', quality=95)
    im1.close()
    im2.close()


def paste_all_cropped_line():  # 1485 168
    im1 = Image.open(f'{FILES_PATH}/step-1.jpg')
    im2 = Image.open(f'{FILES_PATH}/all_cropped2.png')
    im1.paste(im2, (525, 990))
    im1.save(f'{FILES_PATH}/next_2.jpg', quality=95)
    im1.close()
    im2.close()


def resize_all_cropped_line():
    image_path = f'{FILES_PATH}/all_cropped.png'
    fixed_width = 700
    img = Image.open(image_path)
    width_percent = (fixed_width / float(img.size[0]))
    height_size = int((float(img.size[1]) * float(width_percent)))
    new_image = img.resize((fixed_width, height_size))
    new_image.save(f'{FILES_PATH}/all_cropped2.png')


def resize_general_cropped_line():
    image_path = f'{FILES_PATH}/general_cropped.png'
    fixed_width = 700
    img = Image.open(image_path)
    width_percent = (fixed_width / float(img.size[0]))
    height_size = int((float(img.size[1]) * float(width_percent)))
    new_image = img.resize((fixed_width, height_size))
    new_image.save(f'{FILES_PATH}/general_cropped2.png')


def paste_general_cropped_line():  # 1485 168
    im1 = Image.open(f'{FILES_PATH}/next_2.jpg')
    im2 = Image.open(f'{FILES_PATH}/general_cropped2.png')
    im1.paste(im2, (525, 1075))
    im1.save(f'{FILES_PATH}/next_3.jpg', quality=95)
    im1.close()
    im2.close()


def draw_stats():
    sum_ = round(db.get_all_activities_time() / 3600, 3)
    goal = round(settings.goal / 3600, 1)
    percentage = round(sum_ / goal * 100, 1)
    sum_ = str(sum_)[:-2]

    im = Image.new('RGB', (550, 155), color=('#4B4A4A'))
    font = ImageFont.truetype(f'{TEMPLATE_DIR}/MonospaceRegular.ttf', size=45)
    draw_text = ImageDraw.Draw(im)
    text_ = f"Goal: {goal}h\nTime spent: {sum_}h\nCompleted by: {percentage}%"
    draw_text.text((10, 10), text_, font=font, fill='#FFF')
    im.save(f'{FILES_PATH}/stats.jpg', quality=95)
    im.close()


def paste_stats():
    im1 = Image.open(f'{FILES_PATH}/next_3.jpg')
    im2 = Image.open(f'{FILES_PATH}/stats.jpg')
    im1.paste(im2, (1150, 1075))
    im1.save(settings.save_path / f'week_{str(db.get_week_number())}.jpg', quality=95)
    im1.close()
    im2.close()


def del_other_photo():
    os.remove(f'{FILES_PATH}/all_cropped.png')
    os.remove(f'{FILES_PATH}/all_cropped2.png')
    os.remove(f'{FILES_PATH}/barh.png')
    os.remove(f'{FILES_PATH}/pie.png')
    os.remove(f'{FILES_PATH}/general_cropped.png')
    os.remove(f'{FILES_PATH}/general_cropped2.png')
    os.remove(f'{FILES_PATH}/next_2.jpg')
    os.remove(f'{FILES_PATH}/next_3.jpg')
    os.remove(f'{FILES_PATH}/step-1.jpg')
    os.remove(f'{FILES_PATH}/stats.jpg')


def take_photo():
    paste_pie()
    crop_stack_line()
    resize_all_cropped_line()
    paste_all_cropped_line()
    crop_general_line()
    resize_general_cropped_line()
    paste_general_cropped_line()
    draw_stats()
    paste_stats()
    # del_other_photo()
