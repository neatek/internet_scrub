# -*- coding: utf-8 -*-
import scrapy
import pprint
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.sql import text
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey, Numeric
from sqlalchemy import inspect
from scrapy.http import HtmlResponse
import html
from scraper.items import ScraperItem


metadata = MetaData()
books = Table(
    "books",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String),
    Column("authors", String),
    Column("fullprice", Numeric),
    Column("price", Numeric),
    Column("link", String),
    Column("rating", Numeric),
)
engine = create_engine("sqlite:///books.db")
metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()


class Book24(scrapy.Spider):
    name = "Book24"
    allowed_domains = ["book24.ru"]
    current_page = 1
    start_urls = [f"https://book24.ru/catalog/"]
    book_urls = []
    current_url = ""

    def process_paging(self, current_page=1):
        if self.current_page == 1:
            return "https://book24.ru/catalog/"
        else:
            return f"https://book24.ru/catalog/page-{current_page}"

    def parse(self, response: HtmlResponse):
        if response.body:
            self.book_urls = [
                link.attrib["href"]
                for link in response.css("a.product-card__image-link")
            ]

            self.current_page += 1

            for book in self.book_urls:
                self.current_url = book
                yield response.follow(book, callback=self.parse_book)

            yield response.follow(
                self.process_paging(self.current_page), callback=self.parse
            )

    def parse_book(self, response: HtmlResponse):
        name = (
            response.css("h1.product-detail-page__title::text").extract_first().strip()
        )
        link_book = (
            response.xpath('//div[@itemscope="itemscope"]/link[@itemprop="url"]/@href')
            .get()
            .strip()
        )
        print(link_book)
        authors = (
            response.xpath('//span[@itemprop="author"]/meta[@itemprop="name"]/@content')
            .get()
            .strip()
        )
        fullprice = response.css(
            ".product-sidebar-price__price-old::text"
        ).extract_first()

        if fullprice:
            print(fullprice)
            fullprice = html.unescape(fullprice)
            print(fullprice)
            fullprice = (
                (
                    fullprice.replace(" ", "")
                    .replace("&nbsp;", "")
                    .replace("₽", "")
                    .strip()
                )
                .replace(" ", "")
                .replace("\xa0", " ")
            ).replace(" ", "")
            print(fullprice)
            fullprice = float(fullprice)
        else:
            fullprice = 0

        price = float(
            response.xpath('//meta[@property="product:price:amount"]/@content').get()
        )
        rating = float(
            (
                response.css("span.rating-widget__main-text::text")
                .extract_first()
                .strip()
                .replace(",", ".")
            )
        )
        if not rating:
            rating = 0
        book = {
            "name": name,
            "authors": authors,
            "fullprice": fullprice,
            "price": price,
            "link": link_book,
            "rating": rating,
        }
        statement = books.insert().values(
            name=book["name"],
            authors=book["authors"],
            fullprice=book["fullprice"],
            price=book["price"],
            link=book["link"],
            rating=book["rating"],
        )
        session.execute(statement)
        session.commit()
        pprint.pprint(book)
