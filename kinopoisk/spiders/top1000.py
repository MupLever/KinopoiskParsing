import scrapy
from scrapy.http import Response


class Top1000Spider(scrapy.Spider):
    '''Page parser top 1000 movies'''
    name = "top1000"
    allowed_domains = ["www.kinopoisk.ru"]
    COUNT_PAGES = 20
    start_url = "https://www.kinopoisk.ru/lists/movies/top_1000/?page=%d"

    def _movie_titles(self, response: Response) -> list:
        '''Takes in the response and returns an list of movie titles'''
        return \
            response. \
            css("span.styles_mainTitle__IFQyZ::text"). \
            getall()

    def _years_of_premieres(self, response: Response) -> list:
        '''Takes in the response and returns a list of prime years'''
        years_of_premieres = map(
            lambda year: year.get().strip().split(',')[0],
            response.css("div.styles_root__ti07r").
            css("div.desktop-list-main-info_secondaryTitleSlot__mc0mI").
            css("span.desktop-list-main-info_secondaryText__M_aus::text")
            )

        filtered_years_of_premieres = list(
            filter(lambda year: year != '', years_of_premieres)
            )

        return filtered_years_of_premieres

    def _clean_additional_info(self, response: Response) -> list:
        '''
        Takes in the response and returns a list of additional
        information, such as country and producer
        '''
        adddional_info = response.css("div.styles_root__ti07r"). \
            css("span.desktop-list-main-info_truncatedText__IMQRP::text")

        adddional_info = map(lambda info: info.get().split(), adddional_info)

        clean_info = list(
            filter(lambda info: len(info[0]) > 1, adddional_info)
            )

        return clean_info

    def _movie_ratings(self, response: Response) -> list:
        '''Takes in the response and returns an list of movie ratings'''
        movie_ratings = response.css("div.styles_rating__LU3_x")

        clean_movie_ratings = [
            rating.css("span.styles_kinopoiskValue__9qXjg::text").get() or "-"
            for rating in movie_ratings
            ]

        return clean_movie_ratings

    def start_requests(self) -> None:
        for page in range(1, self.COUNT_PAGES + 1):
            url = self.start_url % (page)
            yield scrapy.Request(url=url, callback=self.parse_pages)

    def parse_pages(self, response: Response) -> None:
        '''Parser method for each page of the top 1000'''
        movie_titles = self._movie_titles(response)
        years_of_premieres = self._years_of_premieres(response)
        clean_info = self._clean_additional_info(response)
        movie_ratings = self._movie_ratings(response)
        existence_of_links = [
            item.css("div.styles_onlineCaption__ftChy") != []
            for item in response.css("div.styles_root__ti07r")
            ]

        for title, year, info, rating, link in zip(movie_titles,
                                                   years_of_premieres,
                                                   clean_info,
                                                   movie_ratings,
                                                   existence_of_links):
            yield {
                "name_of_the_movie": title,
                "year": year,
                "country": info[0],
                "producer": " ".join(info[-2:]),
                "raiting": rating,
                "link": link
            }
