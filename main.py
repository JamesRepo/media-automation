import requests
from bs4 import BeautifulSoup
from video import Film, TvShow
from book import Book


def get_imdb_soup(media):
    imdb_api_url = f'https://v2.sg.media-imdb.com/suggestion/h/{media}.json'
    imdb_response = requests.get(imdb_api_url)
    imdb_response.raise_for_status()
    json_response = imdb_response.json()
    media_list = json_response['d']
    if len(media_list) == 0:
        print('Film or TV show not found')
        exit(0)
    # Just retrieve the first item in the list
    media_item = media_list[0]
    try:
        media_id = media_item['id']
        title = media_item['l']
        year = media_item['y']
    except KeyError:
        print("Unable to narrow results, can you be more specific?")
        exit(0)
    print(f'Getting film : {title} - {year}')
    url = f'https://www.imdb.com/title/{media_id}/'
    print(f'IMDB URL = {url}')
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:98.0) Gecko/20100101 Firefox/98.0"}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    return soup


def get_goodreads_soup(media):
    url = f"https://www.goodreads.com/search?q={media}"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    try:
        list_item = soup.find('table', {"class": "tableList"}).find_all('tr')[0].find_all('a')[0]
    except AttributeError:
        print('Error finding book')
        exit(0)
    url = list_item.get('href')
    book_url = "https://www.goodreads.com" + url
    print(f"Goodreads URL = {book_url}")
    book_response = requests.get(book_url)
    book_soup = BeautifulSoup(book_response.text, 'html.parser')
    return book_soup


def main():
    media_type_list = ['Film', 'TV', 'Book']
    media_type = input(f'Input one of: {media_type_list} : ')
    if media_type not in media_type_list:
        print('Inputted media type not in media list')
        exit(0)

    if media_type == 'Film':
        film = input('What film? ')
        soup = get_imdb_soup(film)
        imdb_film = Film(soup)
        print(f'{imdb_film.title} \n {imdb_film.rating} \n {imdb_film.summary} \n {imdb_film.genre_list} \n {imdb_film.runtime} \n {imdb_film.release_date}')

    elif media_type == 'TV':
        tv = input('What TV show? ')
        soup = get_imdb_soup(tv)
        imdb_tv = TvShow(soup)
        print(f'{imdb_tv.title} \n {imdb_tv.rating} \n {imdb_tv.summary} \n {imdb_tv.season_number} \n {imdb_tv.episode_number}')

    elif media_type == 'Book':
        book = input('What book? ')
        soup = get_goodreads_soup(book)
        book = Book(soup)
        print(f'{book.title} \n {book.rating} \n {book.pages} \n {book.genres} \n {book.summary} \n {book.author} \n {book.published_date}')


if __name__ == '__main__':
    main()
