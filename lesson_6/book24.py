# -*- coding: utf-8 -*-
import scrapy
import pprint
import json
import sqlalchemy
from sqlalchemy.sql import text
from sqlalchemy.orm import sessionmaker
from sqlalchemy import (
    create_engine,
    Table,
    Column,
    Integer,
    String,
    MetaData,
    ForeignKey,
    Numeric,
    inspect,
)
from scrapy.http import HtmlResponse
import html
from scraper.items import BookItem
from scrapy.loader import ItemLoader


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
    Column("photos", String),
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
    MAX_PAGE = 3

    # def __init__(self, name=None, **kwargs):
    #     super().__init__(name, **kwargs)
    #     self.start_urls = [f"https://book24.ru/catalog/"]

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
            if self.current_page < self.MAX_PAGE:
                for book in self.book_urls:
                    self.current_url = book
                    yield response.follow(book, callback=self.parse_book)
                yield response.follow(
                    self.process_paging(self.current_page), callback=self.parse
                )

    def parse_book(self, response: HtmlResponse):
        # Name
        name = response.css("h1.product-detail-page__title::text").extract_first()
        name = name.strip() if name else ""

        # Link
        link_book = response.xpath(
            '//div[@itemscope="itemscope"]/link[@itemprop="url"]/@href'
        ).get()
        link_book = link_book.strip() if link_book else ""

        # Authors
        authors = response.xpath(
            '//span[@itemprop="author"]/meta[@itemprop="name"]/@content'
        ).get()
        authors = authors.strip() if authors else ""

        # Fullprice
        fullprice = response.css(
            ".product-sidebar-price__price-old::text"
        ).extract_first()
        if fullprice:
            fullprice = html.unescape(fullprice)
            if fullprice:
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
                fullprice = float(fullprice) if fullprice else 0
        else:
            fullprice = 0

        # Price
        price = response.xpath(
            '//meta[@property="product:price:amount"]/@content'
        ).get()
        price = float(price) if price else 0

        # Rating
        rating = response.css("span.rating-widget__main-text::text").extract_first()
        rating = float((rating.strip().replace(",", "."))) if rating else 0

        # Photos
        photos = [
            photo.attrib["data-src"]
            if "data-src" in photo.attrib
            else photo.attrib["src"]
            if "src" in photo.attrib
            else ""
            for photo in response.css("img.product-poster__main-image")
        ]
        # pprint.pprint(photos)
        # Items
        BookItem(
            name=name,
            authors=authors,
            fullprice=fullprice,
            price=price,
            link=link_book,
            rating=rating,
            photos=photos,
        )
        l = ItemLoader(item=BookItem(), response=response)
        l.add_value("name", name)
        l.add_value("authors", authors)
        l.add_value("fullprice", fullprice)
        l.add_value("price", price)
        l.add_value("link", link_book)
        l.add_value("rating", rating)
        l.add_value("photos", photos)
        yield l.load_item()
        # pprint.pprint(BookItem)
        book = {
            "name": name,
            "authors": authors,
            "fullprice": fullprice,
            "price": price,
            "link": link_book,
            "rating": rating,
            "photos": photos,
        }
        statement = books.insert().values(
            name=book["name"],
            authors=book["authors"],
            fullprice=book["fullprice"],
            price=book["price"],
            link=book["link"],
            rating=book["rating"],
            photos=json.dumps(photos),
        )
        session.execute(statement)
        session.commit()
        # pprint.pprint(book)
