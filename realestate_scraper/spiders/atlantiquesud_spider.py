import scrapy
from scrapy.spiders import SitemapSpider

from realestate_scraper.items import AtlantiqueSudItem


class AlantiqueSudSpider(SitemapSpider):
    name = "atlantique_sud"

    # def start_requests(self):
    #     urls = [
    #         "https://realestatelasterrenas.com/properties/large-apartment-in-beachfront-community",
    #     ]
    #     for url in urls:
    #         yield scrapy.Request(url=url, callback=self.parse)
    sitemap_urls = ["https://realestatelasterrenas.com/sitemap.xml"]
    sitemap_rules = [("/properties/", "parse_properties")]

    def parse_properties(self, response):
        item = AtlantiqueSudItem()
        item["url"] = response.url

        item["name"] = response.xpath("//title/text()").get().split(" |")[0]
        item["built_area"] = (
            response.xpath(
                "//div[@class='sqs-block html-block sqs-block-html']/div/h3[contains(text(), 'Built')]/strong/text()"
            )
            .get()
            .strip()
        )
        item["lot_area"] = (
            response.xpath(
                "//div[@class='sqs-block html-block sqs-block-html']/div/h3[contains(text(), 'Lot')]/strong/text()"
            )
            .get()
            .strip()
        )
        item["bedrooms"] = (
            response.xpath(
                "//div[@class='sqs-block html-block sqs-block-html']/div/h3[contains(text(), 'Beds')]/strong[1]/text()"
            )
            .get()
            .strip()
        )
        item["bathrooms"] = (
            response.xpath(
                "//div[@class='sqs-block html-block sqs-block-html']/div/h3[contains(text(), 'Beds')]/strong[2]/text()"
            )
            .get()
            .strip()
        )
        item["price"] = (
            response.xpath(
                "//div[@class='sqs-block html-block sqs-block-html']/div/h3[contains(text(), 'Price')]/strong/text()"
            )
            .get()
            .strip()
        )
        item["location"] = (
            response.xpath(
                "//div[@class='sqs-block html-block sqs-block-html']/div/h3[contains(text(), 'Location')]/strong/text()"
            )
            .get()
            .strip()
        )
        return item
