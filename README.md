## Kinopoisk Parser

Этот скрипт на Python 3 позволяет вам подключаться к https://www.kinopoisk.ru/lists/movies/top_1000/ 
и собирать информацию о 1000 лучших фильмах: название, год, страна, рейтинг, режиссер и ссылка, если 
таковая имеется.

### Dependencies
* scrapy

### Usage

```
scrapy crawl top1000 -o films.csv
```

### Lint
```
flake8 .
```
