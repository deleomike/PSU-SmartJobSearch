import scrapy

class IndeedSpider(scrapy.Spider):
	name = "indeed_spider"
	job_title = "software engineer"
	job_location = "Pittsburgh, PA"
	start_urls = ['indeed.com/jobs?q='+job_title+'&l='+job_location]
	
	def parse(self, response):
		JOB_CARD_SELECTOR = '.jobsearch-SerpJobCard.row.result.clickcard'
		for jobCard in response.css(JOB_CARD_SELECTOR):
		
			JOB_DETAILS_SELECTOR = '.jobtitle a ::attr(href)'
			details_page = response.css(JOB_DETAILS_SELECTOR).extract_first()
			
			if details_page:
				
	