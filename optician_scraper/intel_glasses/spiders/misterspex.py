import scrapy
import json

from ..items import FielmannItem


class MisterspexSpider(scrapy.Spider):
    name = 'misterspex'
    allowed_domains = ['misterspex.at']
    start_urls = ['http://misterspex.at/']

    def start_requests(self):
        data1 = {"cattype":"pg","catid":"100266","sortType":"popularity-desc","page":1,"searchQuery":{"itemcategory":"GLASSES"},"popularityRanking":"general","filters":{}} 
        data1["page"] = 1
        yield scrapy.Request(method="POST", url="https://www.misterspex.at/__service/product-browse-service/api/l/getProducts", body=json.dumps(data1), callback=self.parse_catalog, meta={"subcategory": "glasses", "data": data1}, headers={"Content-Type": "application/json"})

        data2 = {"cattype":"sg","catid":"100738","sortType":"popularity-desc","page":2,"searchQuery":{"itemcategory":"SUNGLASSES"},"popularityRanking":"general","filters":{}}
        data2["page"] = 1
        yield scrapy.Request(method="POST", url="https://www.misterspex.at/__service/product-browse-service/api/l/getProducts", body=json.dumps(data2), callback=self.parse_catalog, meta={"subcategory": "sunglasses", "data": data2}, headers={"Content-Type": "application/json"})

    def parse_catalog(self, response):
        data = json.loads(response.body)
        for product in data["items"]:
            item = FielmannItem()
            item["store"] = "misterspex.at"
            item["category"] = "eyewear"
            item["subcategory"] = response.meta["subcategory"]
            item["name"] = product["productName"]
            item["product_id"] = product["sku"]
            item["color"] = product["manufacturerColor"]
            item["material"] = ""
            item["images"] = "[]"
            item["brand"] = product["brandName"]
            item["manufacturer"] = ""
            item["availability"] = product["availability"]
            if item["availability"] == "AVAILABLE":
                item["availability"] = "InStock"
            else:
                item["availability"] = "OutOfStock"
            item["currency"] = "EUR" #TODO unstable: cannot change url above to uk site or other sites
            item["price"] = product["salePrice"] 
            item["url"] = "https://www.misterspex.at" + product["productDetailPath"]

            yield item

        if len(data["items"]) != 0:
            response.meta["data"]["page"] += 1
            yield scrapy.Request(method="POST", url="https://www.misterspex.at/__service/product-browse-service/api/l/getProducts", body=json.dumps(response.meta["data"]), callback=self.parse_catalog, meta=response.meta, headers={"Content-Type": "application/json"})

