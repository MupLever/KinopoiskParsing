from typing import Iterable
import scrapy
from scrapy.http import Request


class Top1000Spider(scrapy.Spider):
    name = "top1000"
    allowed_domains = ["kinopoisk.ru"]
    start_urls = ["https://www.kinopoisk.ru/lists/movies/top_1000/"]
    count_pages = 20

    def parse(self, response):
        for page in range(1, self.count_pages + 1):
            url = f"https://www.kinopoisk.ru/lists/movies/top_1000/?page={page}"
            yield response.follow(url, callback=self.parse_pages)

    def parse_pages(self, response):
        for i in range(50):
            yield {
                'name_of_the_movie': response.css('span.styles_mainTitle__IFQyZ.styles_activeMovieTittle__kJdJj::text')[i].get(),
                'year': response.css('span.desktop-list-main-info_secondaryText__M_aus::text')[i].get().split(',')[0],
                'country': response.css('span.desktop-list-main-info_truncatedText__IMQRP::text')[i].get().split()[0],
                'producer': ' '.join(response.css('span.desktop-list-main-info_truncatedText__IMQRP::text')[i].get().split()[-2:]),
                'raiting': response.css('span.styles_kinopoiskValue__9qXjg::text')[i].get(),
                'link': response.css('div.styles_root__ZH67U.styles_sizeS__zzgWP')[i].get()
            }
