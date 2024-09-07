# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import sqlite3


class IntelGlassesPipeline:
    def process_item(self, item, spider):
        return item

class SQLiteNoDupesPipeline:
	def __init__(self):
		self.con = sqlite3.connect("products.db")
		self.cur = self.con.cursor()
		self.cur.execute(
			"""
			CREATE TABLE IF NOT EXISTS product(
				name, product_id, color, images, brand, manufacturer, material, availability, currency, price, store, url, category, subcategory
			)
			"""
		)
	def process_item(self, item, spider):
		self.cur.execute(
			"""SELECT * FROM product WHERE product_id = ? AND store = ? AND category = ? AND subcategory = ?""", (item["product_id"],item["store"], item["category"], item["subcategory"])
		)
		result = self.cur.fetchone()
		if result:
 			spider.logger.info(f"item already in DB, {item['product_id']}")
		else:
			self.cur.execute(
				"""
				INSERT INTO product(name, product_id, color, images, brand, manufacturer, material, availability, currency, price, store, url, category, subcategory) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)
				""",
				(
					item["name"], item["product_id"], item["color"], 
					item["images"], item["brand"], item["manufacturer"], 
					item["material"], item["availability"], item["currency"], item["price"],
                    item["store"], item["url"], item["category"], item["subcategory"]
				)
			)
			self.con.commit()
			return item
