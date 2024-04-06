import requests
from bs4 import BeautifulSoup
import pandas as pd
import urllib.parse
import time

def search_products(search_query, base_url="https://www.amazon.in", page=1):
    """Search for products across multiple pages and return their URLs."""
    print(f"Searching for products on page {page}...")
    search_url = f"{base_url}/s?k={urllib.parse.quote(search_query)}&page={page}"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
    product_urls = []

    try:
        response = requests.get(search_url, headers=headers, timeout=10, proxies=urllib.request.getproxies())
        soup = BeautifulSoup(response.content, "html.parser")
        product_links = soup.find_all(
            "a", {"class": "a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal"})
        product_urls = [urllib.parse.urljoin(
            base_url, link['href']) for link in product_links if '/dp/' in link['href']]
        print(f"Found {len(product_urls)} products.")
    except requests.exceptions.Timeout:
        print(f"Request timed out for page {page}.")
    except Exception as e:
        print(f"An error occurred while fetching products from page {page}: {e}")

    return product_urls



def fetch_product_details(product_url):
    """Fetch details from a product page."""
    print(f"Fetching product details for {product_url}")
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
    try:
        response = requests.get(product_url, headers=headers, timeout=10, proxies=urllib.request.getproxies())
        soup = BeautifulSoup(response.content, "html.parser")

        title = soup.find("span", class_="a-size-large product-title-word-break")
        price = soup.find("span", class_="a-price-whole")
        image = soup.find("img", class_="a-dynamic-image a-stretch-vertical")
        features = soup.find("div", id="feature-bullets")
        description = soup.find("div", class_="a-section feature detail-bullets-wrapper bucket")

        title = title.text.strip() if title else None
        price = price.text.strip() if price else None
        image = image['src'] if image else None
        features = features.text.strip() if features else None
        description = description.text.strip() if description else None

        return {"title": title, "price": price, "image": image, "features": features, "description": description, "url": product_url}
    except requests.exceptions.Timeout:
        print(f"Request timed out for {product_url}")
        return None
    except Exception as e:
        print(f"Failed to fetch product details for {product_url}: {e}")
        return None
    

def aggregate_data(search_query, pages):
    """Aggregate product details across multiple pages into a JSON-like structure."""
    print(f"Starting data aggregation for query: {search_query}")
    base_url = "https://www.amazon.in"
    products_data = []

    for page in range(1, pages + 1):
        product_urls = search_products(search_query, base_url, page)
        for url in product_urls:
            try:
                time.sleep(1)  # Respectful delay between requests
                product_info = fetch_product_details(url)
                products_data.append(product_info)
            except Exception as e:
                print(f"Failed to fetch product details for {url}: {e}")

    print(f"Aggregated data for {len(products_data)} products.")
    return products_data


def export_to_excel(data, filename="output.xlsx"):
    """Export the aggregated data to an Excel file."""
    print(f"Exporting data to {filename}...")
    df = pd.DataFrame(data)
    df.to_excel(filename, index=False)
    print(f"Data successfully exported to {filename}.")


if __name__ == "__main__":
    search_query = input("Enter search query: ")
    pages = input("Enter no of pages: ")
    aggregated_data = aggregate_data(search_query, int(pages))
    export_to_excel(aggregated_data)
