from typing import Iterable
import scrapy
from scrapy.http import Request, Response
from scrapy.selector.unified import Selector


class Top1000Spider(scrapy.Spider):
    '''Page parser top 1000 movies'''
    name = "top1000"
    allowed_domains = ["www.kinopoisk.ru"]
    COUNT_PAGES = 20
    start_url = "https://www.kinopoisk.ru/lists/movies/top_1000/?page=%d"

    def _movie_title(self, item: Selector) -> str:
        '''Takes in the selector with one item and returns a movie title'''
        return item. \
            css("span.styles_mainTitle__IFQyZ::text"). \
            get()

    def _year_of_premiere(self, item: Selector) -> str:
        '''
        Takes in the selector with one item and
        returns the year of the premiere
        '''
        main_info = item. \
            css("div.desktop-list-main-info_secondaryTitleSlot__mc0mI"). \
            css("span.desktop-list-main-info_secondaryText__M_aus::text")

        return main_info[0].get().strip().split(',')[0] or \
            main_info[1].get().strip().split(',')[0]

    def _additional_info(self, item: Selector) -> str:
        '''
        Takes in the selector with one item and returns an
        additional information, such as country and producer
        '''
        return item. \
            css("span.desktop-list-main-info_truncatedText__IMQRP::text"). \
            get(). \
            split()

    def _movie_rating(self, item: Selector) -> str:
        '''Takes in the selector with one item and returns movie rating'''
        rating = item. \
            css("div.styles_rating__LU3_x"). \
            css("span.styles_kinopoiskValue__9qXjg::text"). \
            get()

        return rating or "-"

    def _parse_item(self, item: Selector) -> dict:
        '''
        Takes in the selector with one item and
        returns a dict with all attributes
        '''
        info = self._additional_info(item)
        return {
                "name_of_the_movie": self._movie_title(item),
                "year": self._year_of_premiere(item),
                "country": info[0],
                "producer": ' '.join(info[-2:]),
                "raiting": self._movie_rating(item),
                "link": item.css("div.styles_onlineCaption__ftChy") != [],
            }

    def start_requests(self) -> Iterable[Request]:
        for page in range(1, self.COUNT_PAGES + 1):
            url = self.start_url % page
            yield scrapy.Request(url=url, callback=self.parse_page)

    def parse_page(self, response: Response) -> Iterable[dict]:
        '''Parser method for each page of the top 1000'''
        items = response.css("div.styles_root__ti07r")
        for item in items:
            yield self._parse_item(item)
