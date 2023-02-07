import scrapy
import json

class collect_player_info(scrapy.Spider):
	name='Get_Data'

	def __init__(self):
		self.page_count = 2
		self.num_page = 80 #Num of page need to get data

	def start_requests(self):
		urls = ['https://ancu.me/cho-thue-nha-tro-phong-tro-thanh-pho-ho-chi-minh/t1']
		# YOUR CODE HERE
		yield scrapy.Request(urls[0], callback=self.parse)

	def parse(self, response):
		for i in range(1,16):
			#title
			path = '/html/body/div[5]/div/div[1]/div[4]/div/ul/li['+str(i)+']'
			name = response.xpath(path).css('span.tr-title::text').get()
			#Gia
			priceAndSquare = response.xpath(path).css('div.info-item span::text').getall()
			DistrictAndCity = response.xpath(path).css('div.info-item a::text').getall()
			Date = response.xpath(path).css('div.date::text').get()
			Id = response.xpath(path).css('a.name::attr(href)').get()
			Id = Id[Id.index('-ad')+3:Id.index('.html')]
			yield {
					'Id': Id, 
					'Title': name, 
					'Price': priceAndSquare[0], 
					'Square': priceAndSquare[1], 
					'District': DistrictAndCity[0], 
					'City': DistrictAndCity[1], 
					'Date': Date
					}
		if self.page_count < self.num_page:
			next_page_url = 'https://ancu.me/cho-thue-nha-tro-phong-tro-thanh-pho-ho-chi-minh/t' + str(self.page_count)
			self.page_count += 1
			yield scrapy.Request(next_page_url, callback=self.parse) 