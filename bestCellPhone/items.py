# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class BestcellphoneItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    
    Name = scrapy.Field()
    Price = scrapy.Field()
    '''
    atrib = scrapy.Field()
    value = scrapy.Field()
    '''
    MemoriaInterna = scrapy.Field()
    RAM = scrapy.Field()
    Nucleos = scrapy.Field()
    Velocidad = scrapy.Field()
    Resolucion = scrapy.Field()
    CamaraFrontal = scrapy.Field()
    CamaraPosterior = scrapy.Field()
    Garantia = scrapy.Field()
    Bateria = scrapy.Field()
    ResistenciaAgua = scrapy.Field()
    PuntajeAntutu = scrapy.Field()
    NombreAntutu = scrapy.Field()
    PuntajeK = scrapy.Field()
    
    
    pass
