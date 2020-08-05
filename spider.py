import scrapy

class PlayerValue(scrapy.Spider):
	name = "players"
	start_urls = [
	'https://sofifa.com/?col=vl&sort=desc'
	]

	def parse(self, response):

		i = 0
		for row in response.xpath('/html/body/div[1]/div/div/div[1]/table/tbody//tr'):
			yield{
			'name': row.xpath('td[2]/a[1]//text()').extract(),
			'rating': row.xpath('td[4]//text()').extract(),
			'value' : row.xpath('//*[@data-col="vl"]/text()')[i].extract()
			}
			i += 1

		try:
			next_page_partial_url = response.xpath('//div[@class="pagination"]/a/@href')[1].extract()  
			next_page = 'https://sofifa.com/?col=vl&sort=desc' + '&' + next_page_partial_url
			if next_page is not None:
				next_page = response.urljoin(next_page)
				yield scrapy.Request(next_page, callback=self.parse)	
		except IndexError:
			next_page_partial_url = response.xpath('//div[@class="pagination"]/a/@href').extract_first()
			next_page = 'https://sofifa.com/?col=vl&sort=desc' + '&' + next_page_partial_url
			if next_page is not None:
				next_page = response.urljoin(next_page)
				yield scrapy.Request(next_page, callback=self.parse)
		else:
			pass
		


