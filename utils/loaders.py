import os
import glob
import yaml
import docx

def load_config(config_path='config.yaml'):
    """Loads the YAML configuration file."""
    print("1. Loading configuration from config.yaml...")
    with open(config_path, 'r') as file:
        return yaml.safe_load(file)

def load_corpus_words(corpus_dir):
    """
    This function finds all .txt and .docx files in our corpus directory,
    extracts the text, and returns a single list of words.
    """
    print(f"2. Loading corpus from: {corpus_dir}")
    all_words = []
    
    for filepath in glob.glob(os.path.join(corpus_dir, '*.txt')):
        with open(filepath, 'r', encoding='utf-8') as file:
            text = file.read().replace('\n', ' ')
            all_words.extend(text.split())

    for filepath in glob.glob(os.path.join(corpus_dir, '*.docx')):
        try:
            doc = docx.Document(filepath)
            full_text = []
            for para in doc.paragraphs:
                full_text.append(para.text)
            text = '\n'.join(full_text).replace('\n', ' ')
            all_words.extend(text.split())
        except Exception as e:
            print(f"   > Could not read {filepath}: {e}")

    all_words = [word for word in all_words if word]
    print(f"   > Found {len(all_words)} total words from .txt and .docx files.")
    return all_words

def get_asset_paths(dir_path, extensions):
    """Gets a list of all file paths in a directory with given extensions."""
    paths = []
    for ext in extensions:
        pattern = os.path.join(dir_path, f'*{ext}')
        paths.extend(glob.glob(pattern))
    return paths