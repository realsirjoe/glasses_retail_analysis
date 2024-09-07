import scrapy
import json

from ..items import FielmannItem
import re
import urllib.parse


pearle_url = "https://www.pearle.at/brillen?page={0}"

class PearleSpider(scrapy.Spider):
    name = "pearle"
    allowed_domains = ["pearle.at"]

    def start_requests(self):
        yield scrapy.Request(method="GET", url="https://www.pearle.at/sonnenbrillen", callback=self.parse_brands, meta={"root_url": "https://www.pearle.at/sonnenbrillen", "subcategory": "sunglasses", "url": "https://www.pearle.at"})

        yield scrapy.Request(method="GET", url="https://www.pearle.at/brillen", callback=self.parse_brands, meta={"root_url": "https://www.pearle.at/brillen", "subcategory": "glasses", "url": "https://www.pearle.at"})

    def parse_brands(self, response):
        script_tag = response.css("script[id='__NEXT_DATA__'] ::text").get()
        data = json.loads(script_tag)
        raw_results = data["props"]["initialProps"]["pageProps"]["algoliaConfig"]["resultsState"]["rawResults"][0]

        for brand in raw_results["facets"]["filterableAttributes.brand"].keys():
            brand_url = response.meta["root_url"] + "?brand=" + urllib.parse.quote_plus(brand) + "&page={0}"

            yield scrapy.Request(method="GET", url=brand_url.format(1), callback=self.parse_catalog, meta={"subcategory": response.meta["subcategory"], "url": brand_url, "page": 1, "root_url": response.meta["root_url"]})

    def parse_catalog(self, response):
        script_tag = response.css("script[id='__NEXT_DATA__'] ::text").get()
        data = json.loads(script_tag)
        raw_results = data["props"]["initialProps"]["pageProps"]["algoliaConfig"]["resultsState"]["rawResults"][0]
        data = raw_results["hits"]
        for product in data:
            item = FielmannItem()
            name = product["masterVariant"]["name"]

            item["name"] = re.sub(" Brille$", "", name)
            item["product_id"] = product["masterVariant"]["sku"]
            item["color"] = product["filterableAttributes"]["frameColor_en"][0]

            images = []
            for image_data in product["masterVariant"]["media"]["images"]:
                images.append(image_data["url"])
            item["images"] = json.dumps(images)

            item["brand"] = product["filterableAttributes"]["brand"][0]
            item["manufacturer"] = ""
            try:
                item["material"] = product["filterableAttributes"]["frameMaterial_en"][0]
            except KeyError:
                item["material"] = ""

            if product["isOnStock"]:
                item["availability"] = "InStock"
            else:
                item["availability"] = "OutOfStock"

            for price in product["masterVariant"]["prices"][0]:
                item["currency"] = price["value"]["currencyCode"]
                tmp_price  = str(price["value"]["centAmount"]/100)
                if not item["price"] or item["price"] > tmp_price:
                    item["price"] = tmp_price

            item["store"] = "pearle.at"
            item["url"] = response.meta["root_url"] + "/" + product["slug"]["en"] + "/" + item["product_id"]
            item["category"] = "eyewear"
            item["subcategory"] = response.meta["subcategory"]

            yield item

        print(raw_results["offset"], raw_results["nbHits"])
        if raw_results["offset"] < raw_results["nbHits"]:
            response.meta["page"] += 1
            yield scrapy.Request(method="GET", url=response.meta["url"].format(response.meta["page"]), callback=self.parse_catalog, meta=response.meta)

