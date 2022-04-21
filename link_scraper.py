#spider for webscraping the House of Representative session links 
#from congress.gov into a .csv file


import scrapy


class LinkScraperSpider(scrapy.Spider):
    name = 'link_scraper'
    
    custom_settings={"FEEDS": {"session_links.csv": {"format": "csv"}}}
    
    allowed_domains = ['congress.gov']
    start_urls = ['https://www.congress.gov/roll-call-votes/']

    def parse(self, response):
        for link in response.xpath('//*[@id="content"]/div/div[2]/div[1]/ul/li/ul/li/a/@href').getall():
            yield {'Link':link}
