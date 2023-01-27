
class Book:

    def __init__(self, soup):
        self.title = self._get_title(soup)
        self.rating = self._get_rating(soup)
        self.pages = self._get_pages(soup)
        self.genres = self._get_genres(soup)
        self.author = self._get_author(soup)
        self.published_date = self._get_publishing_date(soup)
        self.summary = self._get_summary(soup)

    def _get_title(self, soup):
        return soup.find('h1').text.strip()

    def _get_rating(self, soup):
        return soup.find('div', attrs={'class': 'RatingStatistics__rating'}).text

    def _get_pages(self, soup):
        return soup.find('p', attrs={'data-testid': 'pagesFormat'}).text

    def _get_genres(self, soup):
        genres_list = soup.find_all('span', attrs={'class': 'BookPageMetadataSection__genreButton'})
        genre_names = []
        for genre in genres_list:
            genre_name = genre.find('span', attrs={'class': 'Button__labelItem'}).text
            genre_names.append(genre_name)
        return genre_names

    def _get_author(self, soup):
        return soup.find('span', attrs={'class': 'ContributorLink__name'}).text

    def _get_publishing_date(self, soup):
        return soup.find('p', attrs={'data-testid': 'publicationInfo'}).text

    def _get_summary(self, soup):
        return soup.find('div', attrs={'class': 'DetailsLayoutRightParagraph__widthConstrained'}).find('span').text
