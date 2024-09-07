import scrapy
import json

from ..items import FielmannItem

hartlauer_url = "https://www.hartlauer.at/on/demandware.store/Sites-Hartlauer-Site/de_AT/Search-UpdateGrid?cgid={0}&pmin=0.01&start={1}&sz=200"

class HartlauerSpider(scrapy.Spider):
    name = 'hartlauer'
    allowed_domains = ['hartlauer.at']

    def start_requests(self):
        yield scrapy.Request(hartlauer_url.format("OPT_L2_0000", "0"), callback=self.parse_catalog_page, meta={"search_category": "OPT_L2_0000", "page_offset": 0, "subcategory": "glasses"})

        yield scrapy.Request(hartlauer_url.format("OPT_L2_0001", "0"), callback=self.parse_catalog_page, meta={"search_category": "OPT_L2_0001", "page_offset": 0, "subcategory": "sunglasses"})

    def parse_catalog_page(self, response):
        links = response.css('div[class="c-productTile__productDetails"] > a::attr(href)').extract()
        for link in links:
            link = "https://www.hartlauer.at" + link
            yield scrapy.Request(link, callback=self.parse_item, meta=response.meta)

        if len(links) != 0:
            response.meta["page_offset"] += 200
            yield scrapy.Request(
                hartlauer_url.format(
                    response.meta["search_category"], 
                    response.meta["page_offset"]
                ), 
                callback=self.parse_catalog_page, meta=response.meta,
            )

    def parse_item(self, response):
        script_tags = response.css("script[type='application/ld+json'] ::text").getall()
        for script in script_tags:
            data = json.loads(script)
            if data["@type"] != "Product":
                continue

            item = FielmannItem()
            item["name"] = data["name"]
            item["product_id"] = data["sku"]
            item["color"]  = ""
            item["images"] = json.dumps([data["image"]])
            item["brand"] = data["brand"]
            item["manufacturer"] = ""
            item["material"] = ""
            item["availability"] = str(data["offers"]["availability"]).replace("https://schema.org/", "")
            item["currency"] = data["offers"]["priceCurrency"]
            item["price"] = data["offers"]["price"]
            item["store"] = "hartlauer.at"
            item["url"] = response.url
            item["category"] = "eyewear"
            item["subcategory"] = response.meta["subcategory"]

            yield item
