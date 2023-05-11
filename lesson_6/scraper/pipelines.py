# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.pipelines.images import ImagesPipeline
from scrapy import Request


class ScraperPipeline:
    def process_item(self, item, spider):
        return item


class Book24PhotosPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        # return super().get_media_requests(item, info)
        if item["photos"]:
            for img in item["photos"]:
                try:
                    print(f"DOWNLOAD IMAGE: {img}")
                    yield Request(img)
                except Exception as e:
                    print(e)
        else:
            print("NO_PHOTOS_IN_ITEM_PIPELINE")
            print(item)
