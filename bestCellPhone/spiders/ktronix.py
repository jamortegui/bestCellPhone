import scrapy
from ..items import BestcellphoneItem
from scrapy import Request
import re
import time


def clean(string):
    return string.replace("\t","").replace("\n","").replace("&nbsp","").strip()

class CellPhoneSpider(scrapy.Spider):
    name = "Bestcellphone"
    start_urls = ["https://www.ktronix.com/celulares/telefonos-celulares/c/BI_101_KTRON"]

    def parse(self, response):
        Links = response.css(".js-product-click-datalayer").xpath("@href").extract()
        aux = []
        for link in Links:
            if link not in aux:
                aux.append(link)
        Links = aux
        Cellphones = response.css(".js-product-click-datalayer::text").extract()
        Cellphones = [x for x in Cellphones if "\n" not in x and "\t" not in x]

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
                forward["MemoriaInterna"] = clean(value)
            elif "RAM" in atrib:
                forward["RAM"] = clean(value)
            elif "Nucleos" in atrib:
                forward["Nucleos"] = clean(value)
            elif "Velocidad" in atrib:
                forward["Velocidad"] = clean(value)
            elif "Resolución Pantalla" in atrib:
                forward["Resolucion"] = clean(value)
            elif "Frontal Principal" in atrib:
                forward["CamaraFrontal"] = clean(value)
            elif "Posterior Principal" in atrib:
                forward["CamaraPosterior"] = clean(value)
            elif "Garantía del Fabricante" in atrib:
                forward["Garantia"] = clean(value)
            elif "Batería" in atrib:
                forward["Bateria"] = clean(value)
            elif "Resistencia al Agua" in atrib:
                forward["ResistenciaAgua"] = clean(value)

        expresion = r'Celular +\S+ +(\S+ +\w+).* +'
        search = re.search(expresion,name)
        if search is not None:
            search = search[1].split(" ")
            yield Request(antutu_links+"/name.{}%20{}".format(search[0],search[1]), callback=self.get_movile,
                          cb_kwargs = forward)
        else:
            yield self.save_items(forward["Name"],forward["Price"],forward["MemoriaInterna"],forward["RAM"],forward["Nucleos"],forward["Resolucion"],
                            forward["CamaraFrontal"],forward["CamaraPosterior"],forward["Garantia"],
                            forward["Bateria"],forward["ResistenciaAgua"],"0","Not found","0")
        time.sleep(1)


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
