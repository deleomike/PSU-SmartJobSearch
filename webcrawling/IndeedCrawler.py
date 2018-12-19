import os
import urllib.parse
import urllib.request
import threading
from pathlib import Path
from urllib.parse import urljoin


from bs4 import BeautifulSoup
from watson_developer_cloud import NaturalLanguageUnderstandingV1 as NLU
from watson_developer_cloud.natural_language_understanding_v1 import Features, EntitiesOptions, KeywordsOptions

#TODO: Implement threading on the posting_generator
#TODO: Comment everything
#TODO: Implement pipe to send the pages

print("start")
####################################
#Author: Unknown
#Author: Mike DeLeo
#File: IndeedCrawler.py
#Summary: Crawls Indeed.com for jobs with the specified job title and location
####################################

####################################
#Beautiful Soup Doc Notes
#Find_all:
#Find:

i = 1
base_url = "https://www.indeed.com/jobs?" #Website to crawl
LIMIT = 100

####################################
#Precondition:
#Postcondition:
#Summary:
####################################
def nextPage(soup):
    print("next_page")
    next_link = soup.find("span", class_="np")
        
    if next_link is not None:
        next_url = next_link.find_parent("a")['href']
        next_page = urljoin(base_url, next_url)
        return next_page
            
    else:
        return 0

####################################
#Precondition:
#Postcondition:
#Summary:
####################################
def saveHTML(jobURL):
    global i
    print("saving")
    print(jobURL)
##    filePath = Path("jobs/IndeedJob{}.html".format(i))
##    page = urllib.request.urlopen(jobURL)
##    page_content = page.read()
##                
##    if not os.path.isdir("jobs"):
##        os.makedirs("jobs")
##        with open(filePath, "wb") as fid:
##            fid.write(page_content)
##            i += 1
##    return

####################################
#Precondition:
#Postcondition:
#Summary:
####################################
def posting_generator(job_title, job_location):
    current_thread = os.getpid()
    print("posting generator")
    print('Current Thread : ',current_thread)
    jobs = [] #Array of jobs initialized
    
    #Initialize the information for the Watson API
    searchValues = {'q':job_title,'l':job_location} #Dictionary of items for watson
    search_url = (base_url + urllib.parse.urlencode(searchValues))    #Website to crawl with search items

    #Select the first page
    next_page = urllib.request.urlopen(search_url, None, None)
    nlu = NLU(
	    iam_apikey='BU11gy3frJMRMKz4XQ_sPJ_HGF3p-qEr74xUlEVTWvsY',
	    version='2018-03-19'
    )

    while True:
    #TODO: find out what this does
            soup = BeautifulSoup(next_page, 'html.parser')

    #TODO: Find out what find_all does
            for job in soup.find_all('div'):
                    if job.get('data-tn-component') is not None and job.get('data-tn-component') == 'organicJob':
                            url = 'https://www.indeed.com' + job.a['href']
                            response = nlu.analyze(
                                    url=url,
                                    features=Features(
                                            entities=EntitiesOptions(
                                                    limit=LIMIT
                                            ),
                                            keywords=KeywordsOptions(
                                                    limit=LIMIT
                                            ),
                                    )
                            ).get_result()
                            jobs.append(response)
                            #jsonprinter(response)
                            #yield url, response
                            saveHTML(url)
            next_url = nextPage(soup)

            if next_url == 0:
                    break
            else:
                    next_page = urllib.request.urlopen(next_url, None, None)

    print("END OF PROGRAM!")

