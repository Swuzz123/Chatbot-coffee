import scrapy
import json 
from ..items import TheCoffeeHouseItem

class TheCoffeeHouseSpider(scrapy.Spider):
    name = 'thecoffeehouse'
    allowed_domains = ['thecoffeehouse.com']
    start_urls = ['https://www.thecoffeehouse.com/collections/all']
    
    # Read URLs list from file JSON
    def start_requests(self):
        with open('D://Workspace//RAG//rag-bot-coffee//output_files//the_coffee_house_all_urls.json', 'r') as f:
            urls = json.load(f)
            
        # Filter only product URLs
        product_urls = [url for url in urls if '/products/' in url]
        for url in product_urls:
            yield scrapy.Request(url=url, callback=self.parse)
            
    def parse(self, response):
        item = TheCoffeeHouseItem()
        
        # Get URLs of products
        item['url'] = response.url
        
        # Get products' title
        item['title'] = response.css('meta[property="og:title"]::attr(content)').get(default="").strip()
        
        # Get products' price
        price = response.css('meta[property="og:price:amount"]::attr(content)').get(default="").strip()
        currency = response.css('meta[property="og:price:currency"]::attr(content)').get(default="VND").strip()
        item['price'] = f"{price} {currency}" if price else None
        
        # Get images' url of products
        item['image_url'] = response.css('meta[property="og:image"]::attr(content)').get(default="").strip()
        
        # Get products' description
        description_list = response.xpath('//div[h4[@class="related_product_title"]]/p/text()').getall()
        item['description'] = " ".join([d.strip() for d in description_list if d.strip()])
        
        yield item