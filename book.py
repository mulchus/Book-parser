import functions
import main

from pathlib import Path
from bs4 import BeautifulSoup
from urllib import parse


def get_book(book_page_url, parser_args):
    book_id = parse.urlsplit(book_page_url).path.replace('/', '').replace('b', '')
    book_file_basis_url = 'https://tululu.org/txt.php'
    filepath = ''
    book_page = functions.get_page(book_page_url)
    page_content = BeautifulSoup(book_page.text, 'lxml')
    about_book = parse_book_page(page_content, book_page_url)

    if not parser_args.skip_txt:
        txt_book = functions.get_page(book_file_basis_url, {'id': book_id})
        filepath, filename = functions.save_txt_file(txt_book, f'{book_id}.{about_book["title"]}',
                                                     Path.joinpath(parser_args.dest_folder, main.FILE_DIR))
        relative_path = str(Path(main.FILE_DIR).joinpath(f'{filename}.txt')).replace('\\', '/')
        about_book['book_path'] = relative_path

    if not parser_args.skip_imgs:
        filename = functions.download_image(about_book['img_scr'],
                                            Path.joinpath(parser_args.dest_folder, main.IMAGE_DIR))
        img_relative_path = str(Path(main.IMAGE_DIR).joinpath(filename)).replace('\\', '/')
        about_book['img_scr'] = img_relative_path

    return filepath, about_book


def parse_book_page(page_content, book_page_url):
    splitresult = parse.urlsplit(book_page_url)
    site_url = parse.urlunsplit([splitresult.scheme, splitresult.netloc, '', '', ''])

    book_title = page_content.select_one('div#content h1').text.split('::')[0].rstrip()
    book_author = page_content.select_one('body div#content h1 a').text

    book_genres = []
    if page_content.select_one('span.d_book'):
        book_genres = [genre.text for genre in page_content.select('span.d_book a')]

    book_img_url = parse.urljoin(site_url, page_content.select_one('div.bookimage a img')['src'])

    book_comments = []
    if page_content.select_one('div.texts'):
        book_comments = [comment.text for comment in page_content.select('div.texts span.black')]

    about_book = {
        'title': book_title,
        'author': book_author,
        'img_scr': book_img_url,
        'book_path': '',
        'comments': book_comments,
        'genres': book_genres,
    }
    return about_book
