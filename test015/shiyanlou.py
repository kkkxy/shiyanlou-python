# -*- coding:utf-8 -*-
import scrapy

#获取实验楼的所有 Github 仓库列表
class ShiyanlouSpider(scrapy.Spider):
    name = 'shiyanlou-repositories'

    @property
    def start_urls(self):
        url_tmpl = ('https://github.com/shiyanlou?before=Y3Vyc29yOnYyOpK5MjAxNy0wNi0wNlQxNzozNjowMSswODowMM4FkpV7&tab=repositories','https://github.com/shiyanlou?after=Y3Vyc29yOnYyOpK5MjAxNy0wNi0wNlQxNzozNjowOCswODowMM4FkpWQ&tab=repositories','https://github.com/shiyanlou?after=Y3Vyc29yOnYyOpK5MjAxNS0wMS0yM1QxMToyNDowOCswODowMM4BxWkv&tab=repositories','https://github.com/shiyanlou?after=Y3Vyc29yOnYyOpK5MjAxNC0xMS0xOFQxNzowMDowNCswODowMM4BmZ9O&tab=repositories')
        return url_tmpl

    def parse(self, response):
        for repo in response.css('div#user-repositories-list ul li'):
            yield{
                "name": repo.xpath('.//h3/a/text()').re_first('\n\s*(.*)'), #'\n\s*(.*)' 提取转行和空格后的文本
                "update_time": repo.css('relative-time::attr(datetime)').extract_first()
                    }

#安装scrapy： pip3 install scrapy
#执行程序： scrapy runspider shiyanlou.py -o shiyanlougithub.json
