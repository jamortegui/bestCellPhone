# bestCellPhone

Scrapy project to determine which cellphone to buy. 
 
The main purpose of the project is to get the technical information and price from all cell phones available in a [Colombian digital store](https://www.ktronix.com/), as well as the antutu benchmark score (from [kimovile](https://www.kimovil.com/es/)) and use that data to determine the best cell phone option to buy. 

Two spiders where implemented. First is ktronix.py (spider name: Bestcellphone) which is the main spider and extracts the required data. Second is antutu.py (spider name: Antutu) which was for testing the extraction of antutu benchmark score information from kimovile site.

Lastly, analysis.py script was implemented to process the data previously collected in json files and generate the report in spanish.

