import scrapy
import json

from ..items import FielmannItem


default_data = {"payload":{"page":1,"perPage":100,"with":{"attributes":"all","advancedAttributes":"all","categories":"all","images":"all","priceRange":True,"lowestPriorPrice":True},"category":"/sonnenbrillen","includeSellableForFree":True,"where":{"attributes":[],"whitelistAttributes":[{"type":"attributes:not","key":"hideInListing","values":[67460]},{"type":"attributes:not","key":"rxComponentType","values":[17137,17158,17148,17197]},{"type":"attributes:not","key":"salesStatus","values":[37641,45893,36947,36950]}],"term":"","page":"1"}}}

class FielmannSpider(scrapy.Spider):
    name = 'fielmann'
    allowed_domains = ['fielmann.at']

    def start_requests(self):
        #data1 = default_data.copy()
        #data1["payload"]["category"] = "/sonnenbrillen"
        #yield scrapy.Request(method="POST", url="https://www.fielmann.at/api/rpc/getProductsByCategory", body=json.dumps(data1), callback=self.parse_first, meta={"subcategory": "sunglasses", "data": data1})

        data2 = default_data.copy()
        data2["payload"]["category"] = "/brillen"
        yield scrapy.Request(method="POST", url="https://www.fielmann.at/api/rpc/getProductsByCategory", body=json.dumps(data2), callback=self.parse_first, meta={"subcategory": "glasses", "data": data2})


    def parse_first(self, response):
        data = json.loads(response.body)
        for page_nr in range(data["pagination"]["last"]+1):
            print("pagenr", page_nr)
            post_data = response.meta["data"]
            print(post_data["payload"]["category"])
            post_data["payload"]["page"] = page_nr
            body = json.dumps(post_data)
            #del response.meta["data"]
            yield scrapy.Request(method="POST", url="https://www.fielmann.at/api/rpc/getProductsByCategory", body=body, callback=self.parse_glasses, meta=response.meta)

    def parse_glasses(self, response):
        data = json.loads(response.body)
        for product in data["products"]:
            item = FielmannItem()
            item["store"] = "fielmann"
            item["category"] = "eyewear"
            item["subcategory"] = response.meta["subcategory"]
            item["name"] = product["attributes"]["name"]["values"]["label"] + " " + product["attributes"]["manufacturerColorCode"]["values"]["value"]
            item["color"] = product["attributes"]["frameColor"]["values"]["label"]

            images = []
            for img in product["images"]:
                images.append(img["hash"])
            item["images"] = json.dumps(images)

            item["brand"] = product["attributes"]["brand"]["values"]["label"]
            item["material"] = product["attributes"]["sapMaterial"]["values"]["label"]

            item["availability"] = not product["isSoldOut"] 
            if item["availability"]:
                item["availability"] = "InStock"
            else:
                item["availability"] = "OutOfStock"

            item["currency"] = product["priceRange"]["min"]["currencyCode"]
            item["price"] = (product["priceRange"]["min"]["withTax"] / 100) + 49 # all prices are lowered by 49 so we add here, maybe this is honeypot

            
            item["product_id"] = product["attributes"]["productNameLong"]["values"]["label"].lower().replace(" ", "-") + "-" + product["attributes"]["manufacturerColorCode"]["values"]["value"] + "-" + product["attributes"]["frameColor"]["values"]["value"].lower().replace(" ", "-") + "-" + str(product["id"])
            item["url"] = "https://www.fielmann.at/p/" + item["product_id"]
		
            item["manufacturer"] = ""

            yield item
