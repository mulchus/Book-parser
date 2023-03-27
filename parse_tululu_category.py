import functions
import requests
import time


from bs4 import BeautifulSoup
from urllib import parse


def get_books_urls(page_of_category_url, start_page, end_page):
    books_urls = []
    splitresult = parse.urlsplit(page_of_category_url)
    site_url = parse.urlunsplit([splitresult.scheme, splitresult.netloc, '', '', ''])
    page_of_category_url_text = functions.get_page(page_of_category_url).text
    soup = BeautifulSoup(page_of_category_url_text, 'lxml')
    last_page = int(soup.select('a.npage')[-1].text)

    if not end_page:
        end_page = last_page
    for page in range(start_page, min(end_page, last_page)+1):
        while True:
            try:
                current_page = parse.urljoin(page_of_category_url, str(page))
                category_page = functions.get_page(current_page)
                break
            except requests.exceptions.HTTPError as error:
                print(f'Ошибка ссылки на категорию книг. Ошибка {error}')
                break
            except requests.exceptions.ConnectionError as error:
                print(f'Ошибка сети. Ошибка {error}')
                time.sleep(1)
                continue

        category_content = BeautifulSoup(category_page.text, 'lxml')
        for table in category_content.select('div#content table'):
            book_url = parse.urljoin(site_url, table.select_one('a')['href'])
            books_urls.append(book_url)
    return books_urls
