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
        movie_titles = response.css('span.styles_mainTitle__IFQyZ::text').getall()

        years_of_premieres = response.css('div.styles_root__ti07r'). \
                                css('div.desktop-list-main-info_secondaryTitleSlot__mc0mI'). \
                                css('span.desktop-list-main-info_secondaryText__M_aus::text')

        filtered_years_of_premieres = list(filter(lambda year : year != ',', map(lambda year: year.get().strip(), years_of_premieres)))
        adddional_info = response.css('div.styles_root__ti07r').css('span.desktop-list-main-info_truncatedText__IMQRP::text')
        adddional_info = map(lambda info: info.get().split(), adddional_info)
        clean_info = list(filter(lambda info: len(info[0]) > 1, adddional_info))

        movie_ratings = response.css('div.styles_rating__LU3_x')
        clean_movie_ratings = [rating.css('span.styles_kinopoiskValue__9qXjg::text').get() or '-' for rating in movie_ratings]

        links = [resp.css('div.styles_inlineItem___co22') != [] for resp in response.css('div.styles_root__ti07r')]
        for i in range(50):
            yield {
                'name_of_the_movie': movie_titles[i],
                'year': filtered_years_of_premieres[i].split(',')[0],
                'country': clean_info[i][0],
                'producer': ' '.join(clean_info[i][-2:]),
                'raiting': clean_movie_ratings[i],
                'link': links[i]
            }

# 'https://hd.kinopoisk.ru/' + response.css('div.styles_root__ti07r').css('div.styles_root__ZH67U.styles_sizeS__zzgWP')[i].get().xpah('@href')
