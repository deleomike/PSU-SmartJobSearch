import urllib.request
import watson_developer_cloud
from bs4 import BeautifulSoup
from watson_developer_cloud import NaturalLanguageUnderstandingV1 as NLU
from watson_developer_cloud.natural_language_understanding_v1 import Features, EntitiesOptions, KeywordsOptions
from urllib.parse import urljoin


def posting_generator():
	jobs = []
	job_title = "software engineer"
	job_location = "Pittsburgh, PA"
	search_url = 'https://www.indeed.com/jobs?q=software+engineer&l=Pittsburgh%2C+PA'
	base_url = 'https://www.indeed.com'

	next_page = urllib.request.urlopen(search_url, None, None)

	nlu = NLU(
		iam_apikey='BU11gy3frJMRMKz4XQ_sPJ_HGF3p-qEr74xUlEVTWvsY',
		version='2018-03-19'
	)

	def nextPage(soup):
		print("BREAK 1")
		next_link = soup.find("span", class_="np")

		if next_link is not None:
			print("BREAK 2")
			next_url = next_link.find_parent("a")['href']
			next_page = urljoin(base_url, next_url)
			return next_page

		else:
			print("BREAK 3")
			return 0

	while True:
		soup = BeautifulSoup(next_page, 'html.parser')

		for job in soup.find_all('div'):
			if job.get('data-tn-component') is not None and job.get('data-tn-component') == 'organicJob':
				url = 'https://www.indeed.com' + job.a['href']
				response = nlu.analyze(
					url=url,
					features=Features(
						entities=EntitiesOptions(
							limit=1000
						),
						keywords=KeywordsOptions(
							limit=1000
						),
					)
				).get_result()
				jobs.append(response)
				# jsonprinter(response)
				yield url, response

		next_url = nextPage(soup)

		if next_url == 0:
			break
		else:
			next_page = urllib.request.urlopen(next_url, None, None)

	print("END OF PROGRAM!")
		
		
if __name__ == '__main__':
	posting_generator()
