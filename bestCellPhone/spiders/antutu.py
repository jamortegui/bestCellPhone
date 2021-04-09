import scrapy
from scrapy.http import FormRequest
from scrapy import Request
from ..items import BestcellphoneItem
import re

class AntutuSpider(scrapy.Spider):
    name = "Antutu"
    start_urls = ["https://www.kimovil.com/en/compare-smartphones"]
    
    current_antutu = "-"
    current_found_name = "-"
    current_score = "-"
    
    def parse(self, response):
        search = "Galaxy A31".split(" ")
        yield Request(self.start_urls[0]+"/name.{}%20{}".format(search[0],search[1]), callback=self.get_movile)
            
    def get_movile (self, response):
        items = BestcellphoneItem()
        next_link = response.css("a.device-link").xpath("@href").get()
        if next_link is not None:
            yield response.follow(next_link, callback=self.get_antutu)
        else:
            self.current_antutu = "0"
            self.current_found_name = "Not found"
            self.current_score = "0"
            items["PuntajeAntutu"] = self.current_antutu
            items["NombreAntutu"] = self.current_found_name
            items["PuntajeK"] = self.current_score
            yield items
        return None
    
    def get_antutu(self, response):
        items = BestcellphoneItem()
        antutu_score = response.css("a[title*=Antutu] span.spec::text").get()
        if antutu_score is not None:
            self.current_antutu = antutu_score
        else:
            self.current_antutu = "0"
        score = response.css(".score::text").get()
        if score is not None:
            self.current_score = score
        else:
            self.current_score = "0"
        found_name = response.css("h1[id=sec-start]").get()
        if found_name is not None:
            found_name = re.search(r"</span>(.+)\n",found_name)[1].strip()
            self.current_found_name = found_name
        else:
            self.current_found_name = "Not found"
        items["PuntajeAntutu"] = self.current_antutu
        items["NombreAntutu"] = self.current_found_name
        items["PuntajeK"] = self.current_score
        yield items
        
        

