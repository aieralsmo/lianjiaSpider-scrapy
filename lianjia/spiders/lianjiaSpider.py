# -*- coding: utf-8 -*-
import scrapy
import json
from ..items import LianjiaItem

class LianjiaSpider(scrapy.Spider):
    """爬取链家房屋成交的信息"""
    name = 'lianjiaSpider'
    allowed_domains = ['bj.lianjia.com']
    start_urls = ['https://bj.lianjia.com/chengjiao/']
    # 命令行执行命令快速保存大到文件
	# scrapy crawl lianjiaSpider -o linajia-sold-data.csv -s FEED_EXPORT_ENCODING=gbk
    def parse(self, response):

    	if response.status != 200: print("访问出错"); return
    	# print(response.status)
    	print("crawling...")
    	html = response.text

    	selector = scrapy.Selector(text=html)
    	# 定位到所有的房源
    	house_items = response.css('div.leftContent ul.listContent li')

    	# 获取详情页的url
    	for item in house_items:
    		house_url = item.css('div.info div.title a::attr(href)').extract_first()
    		#  span:last-child
    		traffic = item.css('div.info div.dealHouseInfo span.dealHouseTxt span:last-child::text').extract_first()

    		
    		yield scrapy.Request(url=house_url, callback=self.parse_detail, meta={"traffic":traffic})
    		
    	# 总页数
    	total_pages = response.css(".page-box.house-lst-page-box::attr(page-data)").extract_first()
    	# print(total_pages)
    	# print(type(total_pages))
    	total_pages = json.loads(total_pages)
    	# print(total_pages)
    	# print(type(total_pages))
    	total_pages = int(total_pages['totalPage'])
    	next_url_base = 'https://bj.lianjia.com/chengjiao/pg{}'
    	for page in range(1, total_pages+1):
    		
    		next_url = next_url_base.format(page)
    		# print('正在爬取第{}页的数据'.format(page))
    		yield scrapy.Request(url=next_url, callback=self.parse)


    def parse_detail(self, response):
    	pass

    	item = LianjiaItem()
    	# 住房交通
    	traffic = response.meta.get("traffic")
    	if traffic: 
    		traffic = traffic if traffic.find('房屋') ==-1 else "暂无数据"

    	all_info = response.css("#introduction > div.introContent > div.base > div.content > ul > li::text").extract()
    	
    	# 地理位置
    	item['address'] = response.css("body > div.house-title > div::text").extract_first().split(' ')[0]
    	# 成交日期
    	item['sold_date'] = response.css('body > div.house-title > div > span::text').extract_first()
    	# 成交单价
    	item['unit_price'] = response.css('body > section.wrapper > div.overview > div.info.fr > div.price > b::text').extract_first()+'元/平'
    	# 成交总价
    	item['sold_total_price'] = response.css('body > section.wrapper > div.overview > div.info.fr > div.price > span').xpath('string(.)').extract_first()
    	# 挂牌价格
    	item['display_total_price'] = response.css('body > section.wrapper > div.overview > div.info.fr > div.msg > span:nth-child(1)').xpath('string(.)').extract_first()


    	# 交通
    	item['traffic'] = traffic
    	# 房屋户型
    	item['huxing'] = all_info[0]
    	# 楼层
    	item['louceng'] = all_info[1]
    	# 建筑面积
    	item['b_mianji'] = all_info[2]
    	# 户型结构
    	item['huxing_jiegou'] = all_info[3]
    	# 套内面积
    	item['t_mianji'] = all_info[4]
    	# 建筑类型
    	item['jianzhu_leixing'] = all_info[5]
    	# 房屋朝向
    	item['chaoxiang'] = all_info[6]
    	# 建成年代
    	item['niandai'] = all_info[7]
    	# 装修
    	item['zhuangxiu'] = all_info[8]
    	# 建筑结构
    	item['jianzhu_jiegou'] = all_info[9]
    	# 供暖方式
    	item['gongnuan'] = all_info[10]
    	# 电梯有无
    	item['dianti'] = all_info[13]

    	yield item
