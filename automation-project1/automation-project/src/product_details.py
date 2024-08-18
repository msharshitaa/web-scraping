import os
import requests
from bs4 import BeautifulSoup


def details():
    url = 'https://www.flipkart.com/clothing-and-accessories/bottomwear/jeans/women-jeans/pr?sid=clo,vua,k58,4hp&otracker=categorytree&otracker=nmenu_sub_Women_0_Jeans'
    response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})

    folder_path = os.path.join(os.getcwd(), 'scraped', 'www.flipkart.com')

    os.makedirs(folder_path, exist_ok=True)

    file_path = os.path.join(folder_path, 'product_details.txt')

    with open(file_path, 'w', encoding='utf-8') as file:

        if response.status_code == 200:

            soup = BeautifulSoup(response.text, 'html.parser')

            title_tag = soup.find('title')
            if title_tag:
                page_title = title_tag.get_text()
                file.write(f"Page Title: {page_title}\n\n")
            else:
                file.write("Page title not found.\n\n")

            style_tags = soup.find_all('style')
            for style in style_tags:
                file.write(f"Inline CSS:\n{style.get_text()}\n\n")

            link_tags = soup.find_all('link', rel='stylesheet')
            for link in link_tags:
                css_url = link.get('href')
                if css_url:

                    if not css_url.startswith('http'):
                        css_url = requests.compat.urljoin(url, css_url)
                    css_response = requests.get(css_url, headers={'User-Agent': 'Mozilla/5.0'})
                    if css_response.status_code == 200:
                        file.write(f"CSS URL: {css_url}\nCSS Content:\n{css_response.text}\n\n")
                    else:
                        file.write(f"Failed to retrieve CSS file. Status code: {css_response.status_code}\n\n")

            titles = soup.find_all('div', class_='syl9yP')
            for title in titles:
                file.write(f"Product Title: {title.get_text()}\n")

            prices = soup.find_all('div', class_='Nx9bqj')
            for price in prices:
                file.write(f"Price: {price.get_text()}\n")

            offers = soup.find_all('div', class_='UkUFwK')
            for offer in offers:
                file.write(f"Offer: {offer.get_text()}\n")
        else:
            file.write(f"Failed to retrieve the page. Status code: {response.status_code}\n")
