# -*- coding: utf-8 -*-
import scrapy
from shiyanlougithub.items import GithubItem

class ShiyanlougithubSpider(scrapy.Spider):
    name = 'repositories'

    @property
    def start_urls(self):
        url_tmpl = 'http://https://github.com/shiyanlou?tab=repositories/','https://github.com/shiyanlou?after=Y3Vyc29yOnYyOpK5MjAxNy0wNi0wNlQxNzozNjoxNSswODowMM4FkpW2&tab=repositories', 'https://github.com/shiyanlou?after=Y3Vyc29yOnYyOpK5MjAxNS0wMS0yM1QxNDoxODoyMSswODowMM4By2VI&tab=repositories', 'https://github.com/shiyanlou?after=Y3Vyc29yOnYyOpK5MjAxNC0xMS0xOVQxMDoxMDoyMyswODowMM4BmcsV&tab=repositories'
        return url_tmpl

    def parse(self, response):
        for r in response.css('div#user-repositories-list ul li'):
            item = GithubItem()
            item['name'] = r.xpath('.//h3/a/text()').re_first('\n\s*(.*)'),            
            item['update_time'] = r.css('relative-time::attr(datetime)').extract_first() 
            r_url = response.urljoin(r.xpath('.//h3/a/@href').extract_first())
            request = scrapy.Request(r_url, callback=self.parse_details)
            request.meta['item'] = item
            yield request
    def parse_details(self, response):
        item = response.meta['item']
        item['commits'] = response.xpath('.//ul[@class="numbers-summary"]/li[@class="commits"]/a/span/text()').extract_first()
        item['branches'] = response.xpath('.//ul[@class="numbers-summary"]/li[2]/a/span/text()').extract_first()
        item['releases'] = response.xpath('.//ul[@class="numbers-summary"]/li[3]/a/span/text()').extract_first()
        yield item
