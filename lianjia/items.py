# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class LianjiaItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # pass
    address = scrapy.Field()
    sold_date = scrapy.Field()
    unit_price = scrapy.Field()
    sold_total_price = scrapy.Field()
    display_total_price = scrapy.Field()
    traffic = scrapy.Field()
    huxing = scrapy.Field()
    louceng = scrapy.Field()
    b_mianji = scrapy.Field()
    huxing_jiegou = scrapy.Field()
    t_mianji = scrapy.Field()
    jianzhu_leixing = scrapy.Field()
    chaoxiang = scrapy.Field()
    niandai = scrapy.Field()
    zhuangxiu = scrapy.Field()
    jianzhu_jiegou = scrapy.Field()
    gongnuan = scrapy.Field()
    dianti = scrapy.Field()
