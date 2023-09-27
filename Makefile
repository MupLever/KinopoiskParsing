all: clean build

build:
	scrapy crawl top1000 -O films.csv
clean:
	rm -rf films.csv
