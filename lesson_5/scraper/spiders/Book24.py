import scrapy


class Book24Spider(scrapy.Spider):
    name = "Book24"
    allowed_domains = ["book24.ru"]
    start_urls = ["http://book24.ru/"]

    def parse(self, response):
        pass
