import os
from PIL import Image, ImageDraw, ImageFont
from dataBase import select_sum
from settings import GOAL
from settings import SAVE_PATH


def crop_stack_line():  # -> all_cropped.png
    barh_cut = Image.open('./fig/barh.png')
    barh_cropped = barh_cut.crop((242, 223, 1727, 391))  # (1920, 1440)
    barh_cropped.save('./fig/all_cropped.png')


def crop_general_line():  # -> general_cropped.png
    barh_cut = Image.open('./fig/barh.png')
    barh_cropped = barh_cut.crop((242, 1063, 1727, 1231))
    barh_cropped.save('./fig/general_cropped.png')


def paste_pie():
    im1 = Image.open('./fig/template.jpg')
    im2 = Image.open('./fig/pie.png')
    im1.paste(im2, (-40, -270))
    im1.save('./fig/step-1.jpg', quality=95)
    im1.close()
    im2.close()


def paste_all_cropped_line():  # 1485 168
    im1 = Image.open('./fig/step-1.jpg')
    im2 = Image.open('./fig/all_cropped2.png')
    im1.paste(im2, (525, 990))
    im1.save('./fig/next_2.jpg', quality=95)
    im1.close()
    im2.close()


def resize_all_cropped_line():
    image_path = './fig/all_cropped.png'
    fixed_width = 700
    img = Image.open(image_path)
    width_percent = (fixed_width / float(img.size[0]))
    height_size = int((float(img.size[1]) * float(width_percent)))
    new_image = img.resize((fixed_width, height_size))
    new_image.save('./fig/all_cropped2.png')


def resize_general_cropped_line():
    image_path = './fig/general_cropped.png'
    fixed_width = 700
    img = Image.open(image_path)
    width_percent = (fixed_width / float(img.size[0]))
    height_size = int((float(img.size[1]) * float(width_percent)))
    new_image = img.resize((fixed_width, height_size))
    new_image.save('./fig/general_cropped2.png')


def paste_general_cropped_line():  # 1485 168
    im1 = Image.open('./fig/next_2.jpg')
    im2 = Image.open('./fig/general_cropped2.png')
    im1.paste(im2, (525, 1075))
    im1.save('./fig/next_3.jpg', quality=95)
    im1.close()
    im2.close()


def draw_stats():
    sum_ = round(select_sum() / 3600, 3)
    goal = round(GOAL / 3600, 1)
    percentage = round(sum_ / goal * 100, 1)
    sum_ = str(sum_)[:-2]

    im = Image.new('RGB', (550, 155), color=('#4B4A4A'))
    font = ImageFont.truetype('MonospaceRegular.ttf', size=45)
    draw_text = ImageDraw.Draw(im)
    text_ = f"Goal: {goal}h\nTime spent: {sum_}h\nCompleted by: {percentage}%"
    draw_text.text((10, 10), text_, font=font, fill='#FFF')
    im.save('./fig/stats.jpg', quality=95)
    im.close()

def paste_stats():
    im1 = Image.open('./fig/next_3.jpg')
    im2 = Image.open('./fig/stats.jpg')
    im1.paste(im2, (1150, 1075))
    im1.save(SAVE_PATH, quality=95)
    im1.close()
    im2.close()

def del_other_photo():
    os.remove('./fig/all_cropped.png')
    os.remove('./fig/all_cropped2.png')
    os.remove('./fig/barh.png')
    os.remove('./fig/pie.png')
    os.remove('./fig/general_cropped.png')
    os.remove('./fig/general_cropped2.png')
    os.remove('./fig/next_2.jpg')
    os.remove('./fig/next_3.jpg')
    os.remove('./fig/stats.jpg')
    os.remove('./fig/step-1.jpg')


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
    del_other_photo()