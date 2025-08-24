import os
import pprint

from utils.loaders import load_config, load_corpus_words, get_asset_paths
from utils.image_gen import generate_image

if __name__ == "__main__":

    config = load_config()
    corpus_words = load_corpus_words(config['paths']['corpus_dir'])
    font_paths = get_asset_paths(config['paths']['fonts_dir'], ['.ttf', '.otf'])
    background_paths = get_asset_paths(config['paths']['backgrounds_dir'], ['.jpg', '.jpeg', '.png'])
    
    print("3. Loading asset paths...")
    print(f"   > Found {len(font_paths)} fonts.")
    print(f"   > Found {len(background_paths)} backgrounds.")
    
    if not corpus_words or not font_paths or not background_paths:
        print("\n[ERROR] Missing essential assets. Please check your config paths.")
        exit(1)
    
    print("\nSetup complete. All assets loaded successfully!")

    default_num = config['dataset']['num_images']
    try:
        user_input = input(f"Enter number of images to generate [{default_num}]: ")
        num_to_generate = default_num if user_input == "" else int(user_input)
    except ValueError:
        print(f"Invalid input. Using default value: {default_num}")
        num_to_generate = default_num

    confirm = input(f"\nReady to generate {num_to_generate} images? (y/n): ")
    if confirm.lower() != 'y':
        print("Generation cancelled by user.")
        exit()

    output_dir = config['paths']['output_dir']
    images_output_dir = os.path.join(output_dir, 'images')
    os.makedirs(images_output_dir, exist_ok=True)

    labels_path = os.path.join(output_dir, 'labels.csv')
    with open(labels_path, 'w', encoding='utf-8') as labels_file:
        labels_file.write("filename,text\n")

    print("\nStarting generation...")
    for i in range(num_to_generate):
        filename, text = generate_image(i + 1, config, corpus_words, font_paths, background_paths)
        
        with open(labels_path, 'a', encoding='utf-8') as labels_file:
            labels_file.write(f'"{filename}","{text}"\n')
            
        print(f"  > Generated image {i+1}/{num_to_generate}: {filename}")
    
    print(f"\nGeneration complete! {num_to_generate} images and labels.csv created in '{output_dir}'.")