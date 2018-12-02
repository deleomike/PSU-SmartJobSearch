import sys
import os
import json
from watson_developer_cloud import DiscoveryV1

#Active discovery instance
discovery = DiscoveryV1(
    version='2017-11-07', 
    iam_apikey='gR4dbAo_IIcdVYAcL1VAafrQonD9FRJF-Imceur5LPXW', 
    url= "https://gateway.watsonplatform.net/discovery/api"
    )


environments = discovery.list_environments()
print(environments)
environment = environments.result['environments'][1]['environment_id']

print(environment)

#init collection
collection = discovery.create_collection(
        environment_id = environment, 
       # configuration_id = environment.configuration_id, 
        name='Collection', 
        description='{collection_desc}').get_result()


data = ['1.htm','2.htm','3.htm','4.htm', '5.htm', '6.htm', '7.htm', '8.htm'] #list of names of documents
#assumes /data is the folder containing all data files
#adds each one to the watson dictionary collection
for file in data:
    with open((os.path.join(os.getcwd(), 'data', file))) as fileinfo: 
                add_doc = discovery.add_document(environment, collection.collection_id, file_info=fileinfo)
                print(json.dumps(add_doc, indent=2))
    
       
keywords = ['PLC'] #list of features extracted from resume by watson NLU       
results = {} #dictionary containing the query response each resume keyword returns
for keyword in keywords:
    response = discovery.query(keyword, filter=keyword, passages_characters=50, count=5)
    results[keyword] = response.passages #response = list[QueryPassages]
    #QueryPassages:
    #passage_text = actual response text
    #document_id = unique file identifier from the watson
    
