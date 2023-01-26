
class Video:

    def __init__(self, soup):
        self.title = self._get_title(soup)
        self.rating = self._get_rating(soup)
        self.summary = self._get_summary(soup)

    def _get_title(self, soup):
        return soup.find('h1').text.strip()

    def _get_rating(self, soup):
        return soup.find('div', attrs={'data-testid': 'hero-rating-bar__aggregate-rating__score'}).find('span').text

    def _get_summary(self, soup):
        return soup.find('div', attrs={'data-testid': 'plot'}).find('span').text


class Film(Video):

    def __init__(self, soup):
        super().__init__(soup)
        self.release_date = self._get_release_date(soup)
        self.genre_list = self._get_genre_list(soup)
        self.runtime = self._get_runtime(soup)

    def _get_release_date(self, soup):
        return soup.find('li', attrs={'data-testid': 'title-details-releasedate'}).find('div').find('a').text

    def _get_genre_list(self, soup):
        genres_list = soup.find('div', attrs={'data-testid': 'genres'}).find_all('a')
        return [genre.text for genre in genres_list]

    def _get_runtime(self, soup):
        return soup.find('ul', attrs={'data-testid': 'hero-title-block__metadata'}).find_all('li')[2].text


class TvShow(Video):

    def __init__(self, soup):
        super().__init__(soup)
        self.season_number = self._get_season_number(soup)
        self.episode_number = self._get_episode_number(soup)

    def _get_season_number(self, soup):
        return soup.find('div', attrs={'data-testid': 'episodes-browse-episodes'}).find('label', attrs={'for': 'browse-episodes-season'}).text

    def _get_episode_number(self, soup):
        return soup.find('div', attrs={'data-testid': 'episodes-header'}).find('h3').find_all('span')[1].text








