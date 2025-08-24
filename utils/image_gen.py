import os
import random
import numpy as np
from PIL import Image, ImageDraw, ImageFont

from utils import augmentations

def generate_image(index, config, corpus_words, font_paths, background_paths):
    # --- Select Random Elements ---
    word_count = random.randint(*config['dataset']['word_count_range'])
    start_index = random.randint(0, len(corpus_words) - word_count)
    text_snippet = ' '.join(corpus_words[start_index : start_index + word_count])

    font_path = random.choice(font_paths)
    background_path = random.choice(background_paths)
    font_size = random.randint(*config['text']['font_size_range'])
    
    # --- Determine Text Color ---
    text_config = config['text']
    if text_config['color']['enabled']:
        color_range = text_config['color']['rgb_range']
        r = random.randint(color_range[0], color_range[1])
        g = random.randint(color_range[0], color_range[1])
        b = random.randint(color_range[0], color_range[1])
        text_color = (r, g, b)
    else:
        text_color = (0, 0, 0) # Default to black
    
    # --- Prepare for Rendering ---
    font = ImageFont.truetype(font_path, font_size)
    padding = text_config['padding']

    # --- Calculate Dimensions ---
    temp_draw = ImageDraw.Draw(Image.new('RGB', (1, 1)))
    text_bbox = temp_draw.textbbox((0, 0), text_snippet, font=font)
    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]
    
    canvas_width = text_width + padding['left'] + padding['right']
    canvas_height = text_height + padding['top'] + padding['bottom']

    # --- Handle the Background ---
    background_img = Image.open(background_path).convert("RGB")
    if background_img.width < canvas_width or background_img.height < canvas_height:
        canvas = Image.new('RGB', (canvas_width, canvas_height))
        for x in range(0, canvas_width, background_img.width):
            for y in range(0, canvas_height, background_img.height):
                canvas.paste(background_img, (x, y))
    else:
        max_x = background_img.width - canvas_width
        max_y = background_img.height - canvas_height
        crop_x = random.randint(0, max_x)
        crop_y = random.randint(0, max_y)
        canvas = background_img.crop((crop_x, crop_y, crop_x + canvas_width, crop_y + canvas_height))

    # --- Render the Text ---
    draw = ImageDraw.Draw(canvas)
    draw.text(
        (padding['left'], padding['top']),
        text_snippet,
        font=font,
        fill=text_color
    )
    
    # --- Apply Augmentations ---
    cv_image = np.array(canvas)
    aug_config = config['augmentations']
    
    if aug_config['warp']['enabled']:
        cv_image = augmentations.apply_warp(cv_image, aug_config['warp'])
    if aug_config['tilt']['enabled']:
        cv_image = augmentations.apply_tilt(cv_image, aug_config['tilt'])
    if aug_config['blur']['enabled']:
        cv_image = augmentations.apply_blur(cv_image, aug_config['blur'])
    if aug_config['noise']['enabled']:
        cv_image = augmentations.apply_noise(cv_image, aug_config['noise'])
    if aug_config['brightness_contrast']['enabled']:
        cv_image = augmentations.apply_brightness_contrast(cv_image, aug_config['brightness_contrast'])
        
    canvas = Image.fromarray(cv_image)

    # --- Save the Image and Label ---
    output_dir = config['paths']['output_dir']
    image_name = f"image_{index:05d}.png"
    output_image_path = os.path.join(output_dir, 'images', image_name)
    
    canvas.save(output_image_path)
    
    return image_name, text_snippet