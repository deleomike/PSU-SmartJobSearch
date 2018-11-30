import sys
import os
import json
from watson_developer_cloud import DiscoveryV1


discovery = DiscoveryV1(version='2017-11-07', api_key='gR4dbAo_IIcdVYAcL1VAafrQonD9FRJF-Imceur5LPXW')

pages = []

for page in pages :
    with open((os.path.join(os.getcwd(), 'data', page))) as fileinfo: 
        add_doc = discovery.add_document('68888984-5825-4b45-b2ba-febfacd1bf4e', 'e511d275-2a61-47dd-8bd1-79d0da5a1c61', file_info=fileinfo)
        print(json.dumps(add_doc, indent=2))
    