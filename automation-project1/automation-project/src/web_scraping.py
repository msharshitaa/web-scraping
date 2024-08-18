import requests
from bs4 import BeautifulSoup
import re
import os
import base64
from urllib.parse import urljoin, urlparse


def save_image(img_url, directory, base_url):
    try:

        if img_url.startswith('data:image'):

            base64_data = img_url.split(',')[1]

            img_data = base64.b64decode(base64_data)

            img_filename = f"data_image_{len(os.listdir(directory)) + 1}.png"
            img_path = os.path.join(directory, img_filename)
            with open(img_path, 'wb') as file:
                file.write(img_data)
            print(f"Downloaded data image {img_filename}")
        else:
            img_url = urljoin(base_url, img_url)
            img_response = requests.get(img_url, headers=headers)
            img_response.raise_for_status()

            img_filename = os.path.basename(img_url.split('?')[0])
            img_filename = re.sub(r'[<>:"/\\|?*]', '', img_filename)
            img_path = os.path.join(directory, img_filename)

            with open(img_path, 'wb') as file:
                file.write(img_response.content)

            print(f"Downloaded {img_filename}")

    except Exception as e:
        print(f"Failed to download {img_url}: {e}")


def web_scraping(url):
    global headers
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
        'Accept-Language': 'en-US,en;q=0.9',
    }

    website_name = urlparse(url).netloc
    scraped_dir = 'scraped'
    website_dir = os.path.join(scraped_dir, website_name)
    images_dir = os.path.join(website_dir, 'images')
    css_dir = os.path.join(website_dir, 'css')

    os.makedirs(images_dir, exist_ok=True)
    os.makedirs(css_dir, exist_ok=True)

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        page_title = soup.title.string if soup.title else "No title found"
        print("Page Title:", page_title)

        images = soup.find_all('img')
        image_urls = [img['src'] for img in images if 'src' in img.attrs]

        print("\nImages URLs:")
        for img_url in image_urls:
            save_image(img_url, images_dir, url)

        css_links = [link['href'] for link in soup.find_all('link', rel='stylesheet') if 'href' in link.attrs]

        print("\nCSS File URLs:")
        for css in css_links:
            css_url = urljoin(url, css)

            try:
                css_response = requests.get(css_url, headers=headers)
                css_response.raise_for_status()

                css_filename = os.path.basename(css_url)
                css_filename = re.sub(r'[<>:"/\\|?*]', '', css_filename)
                css_path = os.path.join(css_dir, css_filename)

                with open(css_path, 'w', encoding='utf-8') as file:
                    file.write(css_response.text)

                print(f"Downloaded {css_filename}")

            except requests.RequestException as e:
                print(f"Failed to download {css_url}: {e}")

    else:
        print(f"Failed to retrieve content. Status code: {response.status_code}")
