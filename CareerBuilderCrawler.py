import urllib.request
import watson_developer_cloud
from bs4 import BeautifulSoup
from watson_developer_cloud import NaturalLanguageUnderstandingV1 as NLU
from watson_developer_cloud.natural_language_understanding_v1 import Features, EntitiesOptions, KeywordsOptions
from Functions import *
from urllib.parse import urljoin


def posting_generator():
    jobs = []
    #job_title = "software engineer"
    #job_location = "Pittsburgh, PA"
    search_url = 'https://www.careerbuilder.com/jobs-software-engineer-in-pittsburgh,pa?keywords=Software+Engineer&location=Pittsburgh%2C+PA'
    base_url = 'https://www.careerbuilder.com'

    next_page = urllib.request.urlopen(search_url, None, None)

    nlu = NLU(
        _apikey='BU11gy3frJMRMKz4XQ_sPJ_HGF3p-qEr74xUlEVTWvsY',
	    version='2018-03-19'
	)

    def nextPage(soup):
	    print("BREAK 1")
	    next_link = soup.find("a", class_="Next Page")

	    if next_link is not None:
		    print("BREAK 2")
		    next_url = next_link.find_parent("a")['href']
		    next_page = next_url
		    return next_page

	    else:
	        print("BREAK 3")
	        return 0

    while True:
        soup = BeautifulSoup(next_page, 'html.parser')

		#next_page = nextPage(soup)
              
        for job in soup.find_all('h2'):
            if job.get('class') == 'job-title show-for-medium-up':
                url = 'https://www.careerbuilder.com' + job.a['href']
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
                yield response

        next_url = nextPage(soup)

        if next_url == 0:
            break
        else:
            next_page = urllib.request.urlopen(next_url, None, None)


    print("END OF PROGRAM!")
		
		
if __name__ == '__main__':
    posting_generator()
