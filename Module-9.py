import requests
from bs4 import BeautifulSoup
import json

def scrape_quotes(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    quotes = []
    for quote in soup.select('div.quote'):
        text = quote.find('span', class_='text').get_text()
        author = quote.find('small', class_='author').get_text()
        tags = [tag.get_text() for tag in quote.select('div.tags a')]
        quotes.append({'text': text, 'author': author, 'tags': tags})
    return quotes

def get_all_pages(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    pages = [a['href'] for a in soup.select('ul.pager a') if a.text == 'Next']
    return pages

def main():
    base_url = 'http://quotes.toscrape.com'
    all_quotes = []
    next_page = '/page/1'
    
    while next_page:
        url = base_url + next_page
        all_quotes.extend(scrape_quotes(url))
        next_page = get_all_pages(url)
        if next_page:
            next_page = next_page[0]

    with open('quotes.json', 'w') as f:
        json.dump(all_quotes, f, indent=4)

if __name__ == "__main__":
    main()
