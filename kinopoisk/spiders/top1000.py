from typing import Iterable
import scrapy
from scrapy.http import Request


class Top1000Spider(scrapy.Spider):
    name = "top1000"
    allowed_domains = ["kinopoisk.ru"]
    start_urls = ["https://www.kinopoisk.ru/lists/movies/top_1000/"]
    count_pages = 20

    def start_requests(self) -> Iterable[Request]:
        for page in range(1, self.count_pages + 1):
            url = f"https://www.kinopoisk.ru/lists/movies/top_1000/?page={page}"
            yield scrapy.Request(url, callback=self.parse_pages)

    def parse_pages(self, response):
        names_of_the_movie = response.css('span.styles_mainTitle__IFQyZ.styles_activeMovieTittle__kJdJj::text')
        years_of_films = response.css('div.styles_root__ti07r'). \
                                css('div.desktop-list-main-info_secondaryTitleSlot__mc0mI'). \
                                css('span.desktop-list-main-info_secondaryText__M_aus::text')

        filtered_years_of_films = list(filter(lambda year : year != ',', map(lambda year: year.get().strip(), years_of_films)))

        adddional_info = response.css('div.styles_root__ti07r').css('span.desktop-list-main-info_truncatedText__IMQRP::text')
        countries = [adddional_info[i] for i in range(len(adddional_info)) if i % 2 == 0]

        producers = response.css('div.styles_root__ti07r').css('span.desktop-list-main-info_truncatedText__IMQRP::text')
        movie_ratings = response.css('span.styles_kinopoiskValue__9qXjg::text')
        links = [resp.css('div.styles_inlineItem___co22') != [] for resp in response.css('div.styles_root__ti07r')]
        for i in range(50):
            yield {
                'name_of_the_movie': names_of_the_movie[i].get(),
                'year': filtered_years_of_films[i].split(',')[0],
                'country': countries[i].get().split()[0],
                'producer': ' '.join(producers[i].get().split()[-2:]),
                'raiting': movie_ratings[i].get(),
                'link': links[i]
            }

# 'https://hd.kinopoisk.ru/' + response.css('div.styles_root__ti07r').css('div.styles_root__ZH67U.styles_sizeS__zzgWP')[i].get().xpah('@href')

