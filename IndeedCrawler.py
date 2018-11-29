import urllib.request
from bs4 import BeautifulSoup
from watson_developer_cloud import NaturalLanguageUnderstandingV1 as NLU
from watson_developer_cloud.natural_language_understanding_v1 import Features, EntitiesOptions, KeywordsOptions
from Functions import *


jobs = []
job_title = "software engineer"
job_location = "Pittsburgh, PA"
search_url = 'https://www.indeed.com/jobs?q=software+engineer&l=Pittsburgh%2C+PA'

page = urllib.request.urlopen(search_url, None, None)

soup = BeautifulSoup(page, 'html.parser')
nlu = NLU(
	iam_apikey='BU11gy3frJMRMKz4XQ_sPJ_HGF3p-qEr74xUlEVTWvsY',
	version='2018-03-19'
)

for job in soup.find_all('div'):
	if job.get('data-tn-component') is not None and job.get('data-tn-component') == 'organicJob':
		url = 'https://www.indeed.com' + job.a['href']
		response = nlu.analyze(
			url=url,
			features=Features(
				entities=EntitiesOptions(),
				keywords=KeywordsOptions()
			)
		).get_result()
		jobs.append(response)
		jsonprinter(response)
