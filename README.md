# Web Scraping and Color Analysis

## Overview

This project involves web scraping to count and analyze distinct colors on a webpage, including those from images and CSS styles. It utilizes Python libraries for web scraping, image processing, and color extraction.

## Project Structure

- `webscraping.py`: Handles the web scraping process.
- `colour_counting.py`: Counts distinct colors from images and CSS.
- `colour_extraction.py`: Extracts color codes from images and CSS.
- `main.py`: Entry point to run the entire project.
- `scraped/`: Folder containing all outputs.
- `css/`: Folder containing CSS files.
- `images/`: Folder containing image files.
- `colour_codes.txt`: File with extracted color codes.
- `product_details.txt`: File containing detailed information about products.

## Setup Instructions

1. **Clone the Repository**

   ```bash
   git clone <repository_url>
   cd <repository_directory>
   ```

2. **Create a Virtual Environment**

   ```bash
   python -m venv venv
   ```

3. **Activate the Virtual Environment**

   - **Windows:**

     ```bash
     venv\Scripts\activate
     ```

   - **macOS/Linux:**

     ```bash
     source venv/bin/activate
     ```

4. **Install Dependencies**

   ```bash
   pip install -r requirements.txt
   ```

## Running the Scripts

1. **Run the Main Script**
   python main.py
   This script will execute the entire process of web scraping, color extraction, and counting.

## Interpreting the Results

1. **CSS URLs**

   - Located in the `css/` folder within the `scraped/` folder.
   - Contains CSS files from the webpage.

2. **Images**

   - Found in the `images/` folder within the `scraped/` folder.
   - Contains image files scraped from the webpage.

3. **Color Codes**

   - Available in the `colour_codes.txt` file within the `scraped/` folder.
   - Lists all extracted color codes.

4. **Product Details**

   - Found in the `product_details.txt` file.
   - Contains various details about products such as titles, prices, offers, and CSS content.

