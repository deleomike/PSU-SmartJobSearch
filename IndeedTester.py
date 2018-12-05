import urllib.request
import urllib.parse
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import os
from pathlib import Path

i = 1

def posting_generator(jobTitle, jobLocation):
	jobs = []
	job_title = jobTitle
	job_location = jobLocation
	searchValues = {'q': job_title, 'l': job_location}
	base_url = 'https://www.indeed.com/jobs?'
	search_url = (base_url + urllib.parse.urlencode(searchValues))

	next_page = urllib.request.urlopen(search_url, None, None)

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


	def saveHTML(jobURL):
		global i
		filePath = Path("Jobs/IndeedJob{}.html".format(i))
		page = urllib.request.urlopen(jobURL)
		page_content = page.read()
		
		if not os.path.isdir("Jobs"):
			os.makedirs("Jobs")
		
		with open(filePath, "wb") as fid:
			fid.write(page_content)
		i += 1
			

	while True:
		soup = BeautifulSoup(next_page, 'html.parser')

		for job in soup.find_all('div'):
			if job.get('data-tn-component') is not None and job.get('data-tn-component') == 'organicJob':
				url = 'https://www.indeed.com' + job.a['href']
				print(url)
				saveHTML(url)
				
		print("BREAK 4")

		next_url = nextPage(soup)

		if next_url == 0:
			break
		else:
			next_page = urllib.request.urlopen(next_url, None, None)

	print("END OF PROGRAM!")
	
def main():
	posting_generator("Software developer", "Pittsburgh, PA")
	
	
if __name__ == '__main__':
	main()