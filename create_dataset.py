import os
from PIL import Image, ImageDraw
from PIL.ImageFont import FreeTypeFont
from rich_tqdm import tqdm

def generate_font_images(dataset_folder, font_name, font_file, characters, image_size=128, font_size=100):
    os.makedirs(f'{dataset_folder}/{font_name}', exist_ok=True)

    background = Image.new('L', (image_size, image_size), 'white')
    font = FreeTypeFont(font_file, font_size)

    for character in tqdm(characters, desc=font_name):
        image = background.copy()
        draw = ImageDraw.Draw(image)
        draw.text((image_size / 2, image_size / 2), character, 'black', font, 'mm')
        image.save(f'{dataset_folder}/{font_name}/{character}.jpg')

if __name__ == '__main__':
    from composition import compositions
    from args import get_create_dataset_args

    args = get_create_dataset_args()
    dataset_folder = args.dataset_folder
    font_folder = args.font_folder
    source_font = args.source_font
    image_size = args.image_size
    font_size = args.font_size

    print('[unit predict]')
    compositions.init(f'{dataset_folder}/compositions.json')
    characters = compositions.get_characters()
    font_name = source_font.split('.')[0]
    generate_font_images(f'{dataset_folder}/unit_predict', font_name, f'{font_folder}/{source_font}', characters, image_size, font_size)

    print('[font generate]')
    with open(f'{dataset_folder}/characters.txt', encoding='utf-8') as file:
        characters = file.read()
    fonts = os.listdir(font_folder)
    for font in fonts:
        font_name = font.split('.')[0]
        generate_font_images(f'{dataset_folder}/font_generate', font_name, f'{font_folder}/{font}', characters, image_size, font_size)
