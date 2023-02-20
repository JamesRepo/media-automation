from typing import List
from dataclasses import dataclass
from bs4 import BeautifulSoup


@dataclass
class BookMetadata:
    title: str
    author: str
    genres: List[str]
    published_date: str
    pages: str


@dataclass
class BookRating:
    rating: float


@dataclass
class BookSummary:
    summary: str


class Book:
    def __init__(self, soup: BeautifulSoup):
        self.metadata = self._get_metadata(soup)
        self.rating = self._get_rating(soup)
        self.summary = self._get_summary(soup)

    def _get_metadata(self, soup: BeautifulSoup) -> BookMetadata:
        title = soup.find('h1').text.strip()
        author = soup.find('span', attrs={'class': 'ContributorLink__name'}).text
        genres_list = soup.find_all('span', attrs={'class': 'BookPageMetadataSection__genreButton'})
        genres = [genre.find('span', attrs={'class': 'Button__labelItem'}).text for genre in genres_list]
        published_date = soup.find('p', attrs={'data-testid': 'publicationInfo'}).text
        pages = soup.find('p', attrs={'data-testid': 'pagesFormat'}).text
        return BookMetadata(title=title, author=author, genres=genres, published_date=published_date, pages=pages)

    def _get_rating(self, soup: BeautifulSoup) -> BookRating:
        rating_str = soup.find('div', attrs={'class': 'RatingStatistics__rating'}).text
        try:
            rating = float(rating_str)
        except ValueError:
            rating = None
        return BookRating(rating=rating)

    def _get_summary(self, soup: BeautifulSoup) -> BookSummary:
        summary = soup.find('div', attrs={'class': 'DetailsLayoutRightParagraph__widthConstrained'}).find('span').text
        return BookSummary(summary=summary)
