# -*- coding:utf-8 -*-
import scrapy

class ShiyanlouSpider(scrapy.Spider):
    name = 'shiyanlou-repositories'

    @property
    def start_urls(self):
        url_tmpl = ('https://github.com/shiyanlou?before=Y3Vyc29yOnYyOpK5MjAxNy0wNi0wNlQxNzozNjowMSswODowMM4FkpV7&tab=repositories','https://github.com/shiyanlou?after=Y3Vyc29yOnYyOpK5MjAxNy0wNi0wNlQxNzozNjowOCswODowMM4FkpWQ&tab=repositories','https://github.com/shiyanlou?after=Y3Vyc29yOnYyOpK5MjAxNS0wMS0yM1QxMToyNDowOCswODowMM4BxWkv&tab=repositories','https://github.com/shiyanlou?after=Y3Vyc29yOnYyOpK5MjAxNC0xMS0xOFQxNzowMDowNCswODowMM4BmZ9O&tab=repositories')
        return url_tmpl

    def parse(self, response):
        for repo in response.css('div#user-repositories-list ul li'):
            yield{
                "name": repo.xpath('.//h3/a/text()').re_first('\n\s*(.*)'),
                "update_time": repo.css('relative-time::attr(datetime)').extract_first()
                    }
