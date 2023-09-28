all: clean build

build:
	scrapy crawl top1000 -O films.csv

lint: 
	flake8 kinopoisk/spiders/top1000.py
	pylint kinopoisk/spiders/top1000.py

clean:
	rm -f films.csv
