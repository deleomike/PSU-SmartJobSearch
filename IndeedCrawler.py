import urllib.request
from bs4 import BeautifulSoup

job_sites = []
job_title = "software engineer"
job_location = "Pittsburgh, PA"
search_url = 'https://www.indeed.com/jobs?q=software+engineer&l=Pittsburgh%2C+PA'

page = urllib.request.urlopen(search_url, None, None)

soup = BeautifulSoup(page, 'html.parser')

for job in soup.find_all('div'):
	if job.get('data-tn-component') != None and job.get('data-tn-component') == 'organicJob':
		url = 'https://www.indeed.com' + job.a['href']
		job_sites.append(url)

for site in job_sites:
	print(site)

