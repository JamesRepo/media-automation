import requests
from bs4 import BeautifulSoup
from video import Film, TvShow
from book import Book


def get_imdb_id(media):
    imdb_api_url = f'https://v2.sg.media-imdb.com/suggestion/h/{media}.json'
    imdb_response = requests.get(imdb_api_url)
    imdb_response.raise_for_status()
    json_response = imdb_response.json()
    media_list = json_response['d']
    if len(media_list) == 0:
        raise ValueError('Film or TV show not found')

    result_found = False
    item_index = 0
    while not result_found:
        media_item = media_list[item_index]
        try:
            media_id = media_item['id']
            title = media_item['l']
            year = media_item['y']
            result_found = True
        except KeyError:
            item_index += 1
            if item_index == len(media_list):
                raise ValueError('Film or TV show not found')

    return media_id, title, year


def get_imdb_soup(media_id):
    url = f'https://www.imdb.com/title/{media_id[0]}/'
    print(f'IMDB URL = {url}')
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:98.0) Gecko/20100101 Firefox/98.0"}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    return soup


def get_rotten_tomatoes_url(media, film: bool):
    url = f"https://www.rottentomatoes.com/search?search={media}"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:98.0) Gecko/20100101 Firefox/98.0"}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")
    if film:
        type_string = 'movie'
    elif not film:
        type_string = 'tvSeries'
    else:
        return None
    list_item = soup.find("search-page-result", {"type": type_string}).find("ul").find_all("search-page-media-row")[0].find_all("a")[1]
    media_url = list_item.get("href")
    print(f"Rotten Tomatoes Link = " + media_url)
    return media_url


def get_rotten_tomatoes_soup(media_url):
    media_response = requests.get(media_url)
    rt_soup = BeautifulSoup(media_response.text, "html.parser")
    return rt_soup


def get_goodreads_url(media):
    url = f"https://www.goodreads.com/search?q={media}"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    list_item = soup.find('table', {"class": "tableList"}).find_all('tr')[0].find_all('a')[0]
    url = list_item.get('href')
    book_url = "https://www.goodreads.com" + url
    print(f"Goodreads URL = {book_url}")
    return book_url


def get_goodreads_soup(book_url):
    book_response = requests.get(book_url)
    book_soup = BeautifulSoup(book_response.text, 'html.parser')

    return book_soup


def main():
    media_type_list = ['film', 'tv', 'book']
    is_app_continuing = True
    while is_app_continuing:
        media_type = input(f'Input one of: {media_type_list} : ').lower()
        if media_type not in media_type_list:
            print('Inputted media type not in media list')
            exit_program = input('Exit program? y to confirm ')
            if exit_program == 'y':
                is_app_continuing = False
            continue

        if media_type == 'film':
            film = input('What film? ')
            imdb_soup = get_imdb_soup(get_imdb_id(film))
            rt_soup = get_rotten_tomatoes_soup(get_rotten_tomatoes_url(film, True))
            film = Film(imdb_soup, rt_soup)
            print(f'{film.title} \n{film.imdb_rating} \n{film.rt_rating} \n{film.summary} \n{film.genre_list} \n{film.runtime} \n{film.release_date} \n{film.where_to_watch}')

        elif media_type == 'tv':
            tv = input('What TV show? ')
            imdb_soup = get_imdb_soup(get_imdb_id(tv))
            rt_soup = get_rotten_tomatoes_soup(get_rotten_tomatoes_url(tv, False))
            tv_show = TvShow(imdb_soup, rt_soup)
            print(f'{tv_show.title} \n{tv_show.imdb_rating} \n{tv_show.rt_rating} \n{tv_show.summary} \n{tv_show.season_number} \n{tv_show.episode_number} \n{tv_show.where_to_watch}')

        elif media_type == 'book':
            book = input('What book? ')
            imdb_soup = get_goodreads_soup(get_goodreads_url(book))
            book = Book(imdb_soup)
            print(f'{book.metadata.title} \n {book.rating} \n{book.metadata.pages} \n{book.metadata.genres} \n{book.summary} \n{book.metadata.author} \n{book.metadata.published_date}')

        another_input = input('Would you like to input again? y or n ')
        if another_input != 'y':
            is_app_continuing = False


if __name__ == '__main__':
    main()
