import os
import random
from PIL import Image, ImageDraw, ImageFont

def generate_image(index, config, corpus_words, font_paths, background_paths):
    """
    Generates a single synthetic image with text.
    """
    
    # --- A. Select Random Elements ---
    word_count = random.randint(*config['dataset']['word_count_range'])
    start_index = random.randint(0, len(corpus_words) - word_count)
    text_snippet = ' '.join(corpus_words[start_index : start_index + word_count])

    font_path = random.choice(font_paths)
    background_path = random.choice(background_paths)
    font_size = random.randint(*config['text']['font_size_range'])
    
    # --- B. Prepare for Rendering ---
    font = ImageFont.truetype(font_path, font_size)
    padding = config['text']['padding']

    # --- C. Calculate Dimensions ---
    temp_draw = ImageDraw.Draw(Image.new('RGB', (1, 1)))
    text_bbox = temp_draw.textbbox((0, 0), text_snippet, font=font)
    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]
    
    canvas_width = text_width + padding['left'] + padding['right']
    canvas_height = text_height + padding['top'] + padding['bottom']

    # --- D. Handle the Background ---
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

    # --- E. Render the Text ---
    draw = ImageDraw.Draw(canvas)
    draw.text((padding['left'], padding['top']), text_snippet, font=font, fill=(0, 0, 0))

    # --- F. Save the Image and Label ---
    output_dir = config['paths']['output_dir']
    image_name = f"image_{index:05d}.png"
    output_image_path = os.path.join(output_dir, 'images', image_name)
    
    canvas.save(output_image_path)
    
    return image_name, text_snippet