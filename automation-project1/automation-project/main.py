from src.web_scraping import web_scraping
from src.color_extraction import extract_colors
from src.visualize import visualize
from src.product_details import details
def main():
    url = 'https://www.flipkart.com'
    web_scraping(url)
    extract_colors(url)
    visualize()
    details()


if __name__ == "__main__":
    main()
