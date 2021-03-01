import scrapy
from scrapy_splash import SplashRequest
from realestate_scraper.items import AtlantiqueSudItem


class AlantiqueSudSpider(scrapy.Spider):
    name = "atlantique_sud"

    url = "https://realestatelasterrenas.com/villas-for-sale"
    script = """
            function main(splash, args)
                splash:go(args.url)
                local scroll_to = splash:jsfunc("window.scrollTo")
                scroll_to(0, 10300)
                splash:runjs("setInterval(function () {document.getElementsByClassName('pagination-item-{page}')[0].children[0].click();}, 1000);")
                scroll_to(0, 2300)
                splash:wait(8)
                return {html=splash:html()}
            end
        """

    def start_requests(self):
        splash_args = {
            "html": 1,
            "width": 600,
            "render_all": 1,
        }
        # yield scrapy.Request(self.url, callback=self.save_files_page_2)
        # yield SplashRequest(
        #     self.url,
        #     self.parse_properties_page,
        #     endpoint="execute",
        #     args={"lua_source": self.script},
        #     dont_filter=True,
        # )
        scroll = """
            function main(splash, args)
                splash:go(args.url)
                local scroll_to = splash:jsfunc("window.scrollTo")
                scroll_to(0, 10300)
                splash:wait(5)
                return {html=splash:html()}
            end
        """

        yield SplashRequest(
            self.url,
            self.parse_properties_page,
            endpoint="execute",
            args={"lua_source": scroll},
            # dont_filter=True,
        )

        # yield scrapy.Request(
        #     self.url,
        #     self.parse_properties_page,
        #     # endpoint="execute",
        #     # args={"lua_source": script},
        # )

    def parse(self, response):
        self.parse_properties_page(response)
        # page = response.url.split("/")[-1]
        # filename = f"data/test-page-2/atlantiquesud-{page}.html"
        # with open(filename, "wb") as f:
        #     f.write(response.body)

    def parse_properties_page(self, response):
        properties_page_links = response.css("a.summary-title-link::attr(href)")

        for href in properties_page_links:
            print("PARRSING!")
            url = response.urljoin(href.get())
            yield scrapy.Request(url, callback=self.save_files_page_1)
            # yield SplashRequest(
            #     url,
            #     self.save_files_page_2,
            #     args={
            #         # optional; parameters passed to Splash HTTP API
            #         "wait": 0,
            #         # 'url' is prefilled from request url
            #         # 'http_method' is set to 'POST' for POST requests
            #         # 'body' is set to request body for POST requests
            #     },
            # )
        # yield from response.follow_all(properties_page_links, self.save_files_page_2)
        print("LET's GO!")
        current_page = int(response.css("div.page-number.active a::text").get())
        last_page = int(response.css("div.page-number-last a::text").get())
        if current_page != last_page:
            next_page = str(current_page + 1)
            print(f"Crawling page {next_page}")
            print(self.script.replace("{page}", next_page))
            yield SplashRequest(
                self.url,
                self.parse_properties_page,
                endpoint="execute",
                args={"lua_source": self.script.replace("{page}", next_page)},
                dont_filter=True,
            )

    def save_files_page_1(self, response):
        page = response.url.split("/")[-1]
        filename = f"data/output/test-3/atlantiquesud-{page}.html"
        with open(filename, "wb") as f:
            f.write(response.body)

    def save_files_page_2(self, response):
        page = response.url.split("/")[-1]
        filename = f"data/output/atlantiquesud-{page}.html"
        with open(filename, "wb") as f:
            f.write(response.body)

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
