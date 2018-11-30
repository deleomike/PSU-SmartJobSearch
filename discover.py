import sys
import os
import json
from watson_developer_cloud import DiscoveryV1

#Active discovery instance
discovery = DiscoveryV1(version='2017-11-07', api_key='gR4dbAo_IIcdVYAcL1VAafrQonD9FRJF-Imceur5LPXW')

#pages refers to webpages
#this method of uploading data into watson discover is through local files
#html is acceptable, so we can just download the HTML file at every URL as we crawl
#as we download, name the files by an incrementing number and append that name into the pages list
pages = []


for page in pages :
    with open((os.path.join(os.getcwd(), 'data', page))) as fileinfo: 
        add_doc = discovery.add_document('68888984-5825-4b45-b2ba-febfacd1bf4e', 'e511d275-2a61-47dd-8bd1-79d0da5a1c61', file_info=fileinfo)
        print(json.dumps(add_doc, indent=2))
#this code was originally from IBM's page and it was totally broken but i fixed it because i am smarter than IBM obviously
