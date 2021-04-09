import scrapy
#from scrapy.http import FormRequest
from ..items import BestcellphoneItem
from scrapy import Request
import re
import time
#import json
#import threading

def clean(string):
    return string.replace("\t","").replace("\n","").replace("&nbsp","").strip()

class CellPhoneSpider(scrapy.Spider):
    name = "Bestcellphone"
    #start_urls = ["https://www.ktronix.com/"]    
    #allowed_domains = ["ktronix.com","kimovil.com"]
    #start_urls = ["https://www.ktronix.com/celulares/telefonos-celulares/c/BI_101_KTRON?q=%3Arelevance%3Abrand%3ASAMSUNG#"]
    start_urls = ["https://www.ktronix.com/celulares/telefonos-celulares/c/BI_101_KTRON"] 
    
    current_antutu = "None"
    current_found_name = "None"
    current_score = "None"  
    
    '''
    def parse(self, response):
        #search = input("Please invsert the device you want to search: ")
        
        search = "Celular samsung"
        return FormRequest.from_response(response, formdata={
                "text":search
                }, callback=self.start_scraping)
    '''
    
        
    def parse(self, response):
        Links = response.css(".js-product-click-datalayer").xpath("@href").extract()
        aux = []
        for link in Links:
            if link not in aux:
                aux.append(link)
        Links = aux
        Cellphones = response.css(".js-product-click-datalayer::text").extract()        
        Cellphones = [x for x in Cellphones if "\n" not in x and "\t" not in x]
        #items["Name"] = Cellphones
        #yield items
        
        for link in Links:
            yield response.follow(link, callback= self.get_cellphone_info)
        
        nextLink = response.css(".arrow--right a").xpath("@href").get()
        if nextLink is not None:
            yield response.follow(nextLink, callback= self.parse)
            
        
    def save_items(self,Name,Price,MemoriaInterna, RAM, Nucleos, Velocidad, Resolucion, CamaraFrontal,
                   CamaraPosterior, Garantia, Bateria, ResistenciaAgua, PuntajeAntutu,
                   NombreAntutu, PuntajeK):
        items = BestcellphoneItem()
        items["Name"] = Name
        items["Price"] = Price
        items["MemoriaInterna"] = MemoriaInterna
        items["RAM"]=RAM
        items["Nucleos"]=Nucleos
        items["Velocidad"]=Velocidad
        items["Resolucion"]=Resolucion
        items["CamaraFrontal"]=CamaraFrontal
        items["CamaraPosterior"]=CamaraPosterior
        items["Garantia"]=Garantia
        items["Bateria"]=Bateria
        items["ResistenciaAgua"]=ResistenciaAgua
        items["PuntajeAntutu"] = PuntajeAntutu
        items["NombreAntutu"] = NombreAntutu
        items["PuntajeK"] = PuntajeK          
        return items
    
    def get_cellphone_info(self, response):
        #items = BestcellphoneItem()
        forward = {}
        antutu_links = "https://www.kimovil.com/en/compare-smartphones"
        trs = response.css("tr")
        name = response.css(".ktronix-title-color::text").extract()[0]
        name = clean(name)
        forward["Name"]=name
        price = response.css(".price-ktronix::text").get()
        forward["Price"]=clean(price)
        price = clean(price)
        
        for tr in trs:
            atrib = tr.css("td.attrib::text").extract()
            value = tr.css("td.text-right::text").extract()
                        
            if len(atrib)==0:
                continue
            atrib = atrib[0]
            value = value[0]
            if "Interna" in atrib:
                #items["MemoriaInterna"] = clean(value)
                forward["MemoriaInterna"] = clean(value)
            elif "RAM" in atrib:
                #items["RAM"] = clean(value)
                forward["RAM"] = clean(value)
            elif "Nucleos" in atrib:
                #items["Nucleos"] = clean(value)
                forward["Nucleos"] = clean(value)
            elif "Velocidad" in atrib:
                #items["Velocidad"] = clean(value)
                forward["Velocidad"] = clean(value)
            elif "Resolución Pantalla" in atrib:
                #items["Resolucion"] = clean(value)
                forward["Resolucion"] = clean(value)
            elif "Frontal Principal" in atrib:
                #items["CamaraFrontal"] = clean(value)
                forward["CamaraFrontal"] = clean(value)
            elif "Posterior Principal" in atrib:
                #items["CamaraPosterior"] = clean(value)
                forward["CamaraPosterior"] = clean(value)
            elif "Garantía del Fabricante" in atrib:
                #items["Garantia"] = clean(value)
                forward["Garantia"] = clean(value)
            elif "Batería" in atrib:
                #items["Bateria"] = clean(value)
                forward["Bateria"] = clean(value)
            elif "Resistencia al Agua" in atrib:
                #items["ResistenciaAgua"] = clean(value)
                forward["ResistenciaAgua"] = clean(value)
        
        expresion = r'Celular +\S+ +(\S+ +\w+).* +'
        search = re.search(expresion,name)
        #self.write_Json("empty","empty","empty")
        if search is not None:
            search = search[1].split(" ")
            yield Request(antutu_links+"/name.{}%20{}".format(search[0],search[1]), callback=self.get_movile,
                          cb_kwargs = forward)                        
        else:
            yield self.save_items(forward["Name"],forward["Price"],forward["MemoriaInterna"],forward["RAM"],forward["Nucleos"],forward["Resolucion"],
                            forward["CamaraFrontal"],forward["CamaraPosterior"],forward["Garantia"],
                            forward["Bateria"],forward["ResistenciaAgua"],"0","Not found","0")
        time.sleep(1)
        #yield items

    def get_movile (self, response, Name="", Price="", MemoriaInterna="", RAM="", Nucleos="", Velocidad="",
                    Resolucion="", CamaraFrontal="", CamaraPosterior="", Garantia="", Bateria="",
                    ResistenciaAgua=""):
        next_link = response.css("a.device-link").xpath("@href").get()
        if next_link is not None:
            forward = {}
            forward["Name"]=Name
            forward["Price"]=Price
            forward["MemoriaInterna"]=MemoriaInterna
            forward["RAM"]=RAM
            forward["Nucleos"]=Nucleos
            forward["Velocidad"]=Velocidad
            forward["Resolucion"]=Resolucion
            forward["CamaraFrontal"]=CamaraFrontal
            forward["CamaraPosterior"]=CamaraPosterior
            forward["Garantia"]=Garantia
            forward["Bateria"]=Bateria
            forward["ResistenciaAgua"]=ResistenciaAgua
            yield response.follow(next_link, callback=self.get_antutu, cb_kwargs = forward)
        else:
            yield self.save_items(Name, Price, MemoriaInterna, RAM, Nucleos, Velocidad,
                                  Resolucion, CamaraFrontal, CamaraPosterior, Garantia, Bateria,
                                  ResistenciaAgua,"0","Not found","o")
    
    def get_antutu(self, response, Name="", Price="", MemoriaInterna="", RAM="", Nucleos="", Velocidad="",
                   Resolucion="", CamaraFrontal="", CamaraPosterior="", Garantia="", Bateria="",
                   ResistenciaAgua=""):
        antutu_score = response.css("a[title*=Antutu] span.spec::text").get()
        if antutu_score is not None:
            antutu_score = clean(antutu_score)
        else:
            antutu_score = "0"
        score = response.css(".score::text").get()
        if score is not None:
            score = clean(score)
        else:
            score = "0"
        found_name = response.css("h1[id=sec-start]").get()
        if found_name is not None:
            found_name = re.search(r"</span>(.+)\n",found_name)[1].strip()
            found_name = clean(found_name)
        else:
            found_name = "Not found"
        yield self.save_items(Name,Price,MemoriaInterna,RAM,Nucleos,Velocidad,Resolucion,CamaraFrontal,
                              CamaraPosterior,Garantia,Bateria,ResistenciaAgua,antutu_score,found_name,score)
        
            
                
                
        
    '''
    def start_scraping(self, response):
        items = BestcellphoneItem()
        all_div_quotes = response.css("div.quote")
        for quote in all_div_quotes:
            title = quote.css("span.text::text").extract()
            author = quote.css("small.author::text").extract()
            ref = quote.css("span a").xpath("@href").extract()
            tags = quote.css(".tag::text").extract()
            
            items["text"] = title
            items["author"] = author
            items["tags"] = tags
            items["ref"] = ref
            
            yield items
        
        next_page = response.css("li.next a").xpath("@href").get()
        
        if next_page is not None:
            yield response.follow(next_page, callback= self.parse)
            

    def get_data(self,search,a):
        antutu_links = "https://www.kimovil.com/en/compare-smartphones"
        yield Request(antutu_links+"/name.{}%20{}".format(search[0],search[1]), callback=self.get_movile)
        
    
    def write_Json(self,antutu,score,name):
        dictionary = {}
        dictionary["antutu"] = antutu
        dictionary["score"] = score
        dictionary["name"] = name
        success = False
        count = 0
        while not success:
            try:
                file = open("current_data.json","w")
                json.dump(dictionary,file)
                file.close()
                success = True
            except:
                count += 1
                if count > 120:
                    raise Exception("Unable to write json file")
                time.sleep(0.5)
                print("Unable to write json. Retrying...({})".format(count))
                
    
    def read_Json(self):
        success = False
        count = 0
        while not success:
            try:
                file = open("current_data.json")
                data = json.load(file)
                file.close()
                if data["antutu"] != "empty" and data["score"] != "empty" and data["name"] != "empty":
                    success = True
                else:
                    count += 1
                    if count > 120:
                        raise Exception()
                    time.sleep(0.5)
                    print("Json file did not changed. Retrying... ({})".format(count))
            except:
                count += 1
                if count > 120:
                        raise Exception("Unable to read json.")
                time.sleep(0.5)
                print("Unable to read json. Retrying... ({})".format(count))
        return data
    '''