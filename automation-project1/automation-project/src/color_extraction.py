import os
import re
from PIL import Image
from collections import Counter
from urllib.parse import urlparse


def extract_colors_from_image(image_path):
    try:
        with Image.open(image_path) as img:
            img = img.convert('RGB')
            colors = img.getdata()
            return Counter(colors)
    except Exception as e:
        return Counter()


def extract_colors_from_css(css_path):
    color_codes = []
    try:
        with open(css_path, 'r', encoding='utf-8') as file:
            css_content = file.read()

            color_codes = re.findall(
                r'#[0-9a-fA-F]{6}|#[0-9a-fA-F]{3}|rgb\(\s*\d{1,3}\s*,\s*\d{1,3}\s*,\s*\d{1,3}\s*\)',
                css_content
            )
    except Exception as e:
        print(f"Failed to process CSS {css_path}: {e}")
    return color_codes


def rgb_to_hex(rgb):
    return '#%02x%02x%02x' % rgb


def hex_to_rgb(hex_code):
    hex_code = hex_code.lstrip('#')
    length = len(hex_code)
    return tuple(int(hex_code[i:i + length // 3], 16) for i in range(0, length, length // 3))


def extract_colors(url):
    website_name = urlparse(url).netloc
    images_dir = os.path.join('scraped', website_name, 'images')
    css_dir = os.path.join('scraped', website_name, 'css')
    output_dir = os.path.join('scraped', website_name)

    all_image_colors = Counter()
    all_css_colors = []

    if os.path.exists(images_dir):
        for image_file in os.listdir(images_dir):
            if image_file.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):
                image_path = os.path.join(images_dir, image_file)
                colors = extract_colors_from_image(image_path)
                all_image_colors.update(colors)

    if os.path.exists(css_dir):
        for css_file in os.listdir(css_dir):
            if css_file.lower().endswith('.css'):
                css_path = os.path.join(css_dir, css_file)
                colors = extract_colors_from_css(css_path)
                all_css_colors.extend(colors)

    distinct_image_colors = set(all_image_colors.keys())
    distinct_css_colors = set()

    for color in all_css_colors:
        if color.startswith('#'):
            rgb = hex_to_rgb(color)
            distinct_css_colors.add((color, f"RGB{rgb}"))
        else:

            match = re.match(r'rgb\(\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)\s*\)', color)
            if match:
                rgb = tuple(map(int, match.groups()))
                hex_color = rgb_to_hex(rgb)
                distinct_css_colors.add((hex_color, f"RGB{rgb}"))

    distinct_css_colors = sorted(distinct_css_colors)
    distinct_css_colors_hex, distinct_css_colors_rgb = zip(*distinct_css_colors) if distinct_css_colors else ([], [])

    image_hex_colors = [rgb_to_hex(color) for color in distinct_image_colors]
    image_rgb_colors = [f"RGB{color}" for color in distinct_image_colors]

    os.makedirs(output_dir, exist_ok=True)
    output_file = os.path.join(output_dir, 'colour_codes.txt')

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("Distinct Image Colors:\n")
        for hex_color, rgb_color in zip(image_hex_colors, image_rgb_colors):
            f.write(f"Hex: {hex_color}, RGB: {rgb_color}\n")

        f.write("\nDistinct CSS Colors:\n")
        for hex_color, rgb_color in zip(distinct_css_colors_hex, distinct_css_colors_rgb):
            f.write(f"Hex: {hex_color}, RGB: {rgb_color}\n")

    print(f"Distinct image colors count: {len(distinct_image_colors)}")
    print(f"Distinct CSS colors count: {len(distinct_css_colors_hex)}")
    print(f"Total distinct colors count: {len(distinct_image_colors.union(distinct_css_colors_hex))}")
