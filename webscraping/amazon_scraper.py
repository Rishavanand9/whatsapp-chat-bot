import requests
from bs4 import BeautifulSoup
import pandas as pd

def scrape_amazon(search_query, pages=1):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}

    data = []

    for page in range(1, pages + 1):
        url = f'https://www.amazon.in/s?k={search_query}&page={page}'
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.content, 'html.parser')

        product_titles = soup.find_all('span', class_='a-size-base-plus a-color-base a-text-normal')
        product_prices = soup.find_all('span', class_='a-price-whole')

        for title, price in zip(product_titles, product_prices):
            data.append({'Product Name': title.text, 'Product Price': price.text})

    return pd.DataFrame(data)

if __name__ == '__main__':
    search_query = input('Enter the search query: ')
    pages = int(input('Enter the number of pages to scrape: '))
    df = scrape_amazon(search_query, pages)
    print(df)
    filename = f'{search_query}.xlsx'
    df.to_excel(filename, index=False)
    print(f'Data saved to {filename}')
