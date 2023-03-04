
class Video:

    def __init__(self, imdb_soup, rt_soup):
        self.title = self._get_title(imdb_soup)
        self.imdb_rating = self._get_imdb_rating(imdb_soup)
        self.rt_rating = self._get_rt_rating(rt_soup)
        self.summary = self._get_summary(imdb_soup)
        self.where_to_watch = self._get_where_to_watch(rt_soup)

    def _get_title(self, soup):
        return soup.find('h1').text.strip()

    def _get_imdb_rating(self, soup):
        return soup.find('div', attrs={'data-testid': 'hero-rating-bar__aggregate-rating__score'}).find('span').text

    def _get_rt_rating(self, soup):
        tomato_meter = \
            soup.find('div', attrs={'class': 'thumbnail-scoreboard-wrap'}).find('score-board')['tomatometerscore']
        audience_score = \
            soup.find('div', attrs={'class': 'thumbnail-scoreboard-wrap'}).find('score-board')['audiencescore']
        return f'tomato: {tomato_meter} / audience: {audience_score}'

    def _get_summary(self, soup):
        return soup.find('span', attrs={'data-testid': 'plot-l'}).text

    def _get_where_to_watch(self, soup):
        where_to_watch_bubbles = soup.find_all('where-to-watch-meta')
        platform_map = {}
        for bubble in where_to_watch_bubbles:
            platform = bubble['affiliate']
            platform_license = bubble.find('span', attrs={'slot': 'license'}).text
            platform_map.update({platform: platform_license})
        return platform_map


class Film(Video):

    def __init__(self, imdb_soup, rt_soup):
        super().__init__(imdb_soup, rt_soup)
        self.release_date = self._get_release_date(imdb_soup)
        self.genre_list = self._get_genre_list(imdb_soup)
        self.runtime = self._get_runtime(imdb_soup)

    def _get_release_date(self, soup):
        return soup.find('li', attrs={'data-testid': 'title-details-releasedate'}).find('div').find('a').text

    def _get_genre_list(self, soup):
        genres_list = soup.find('div', attrs={'data-testid': 'genres'}).find_all('a')
        return [genre.text for genre in genres_list]

    def _get_runtime(self, soup):
        return soup.find('ul', attrs={'data-testid': 'hero-title-block__metadata'}).find_all('li')[2].text


class TvShow(Video):

    def __init__(self, imdb_soup, rt_soup):
        super().__init__(imdb_soup, rt_soup)
        self.season_number = self._get_season_number(imdb_soup)
        self.episode_number = self._get_episode_number(imdb_soup)

    def _get_season_number(self, soup):
        return soup.\
            find('div', attrs={'data-testid': 'episodes-browse-episodes'}).\
            find('label', attrs={'for': 'browse-episodes-season'}).text

    def _get_episode_number(self, soup):
        return soup.find('div', attrs={'data-testid': 'episodes-header'}).find('h3').find_all('span')[1].text

