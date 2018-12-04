import sys
import os
import json
import warnings
from watson_developer_cloud import DiscoveryV1

warnings.filterwarnings('ignore')

collectionID = '9f8cf9d5-8bae-4fa4-92b0-2ff75fc4bd14'
APIKEY = 'gR4dbAo_IIcdVYAcL1VAafrQonD9FRJF-Imceur5LPXW'
URL = "https://gateway.watsonplatform.net/discovery/api"
#Active discovery instance
discovery = DiscoveryV1(
    version='2017-11-07', 
    iam_apikey= APIKEY, 
    url= URL
    )


environments = discovery.list_environments()
environmentID = environments.result['environments'][1]['environment_id']


#init collection
try:
    collection = discovery.create_collection(
            environment_id = environmentID, 
            name='Collection', 
            description='{collection_desc}').get_result()
            
    collectionID = collection['collection_id']
except: 
    collections = discovery.list_collections(environmentID).result['collections']
    for collection in collections:
        if collection['name'] == 'Collection':
            discovery.delete_collection(environmentID,collection['collection_id'])
            #collectionID = collection['collection_id']
            
    collection = discovery.create_collection(
            environment_id = environmentID, 
            name='Collection', 
            description='{collection_desc}').get_result()
    collectionID = collection['collection_id']
    
    
    
try:
    data = ['1.htm','2.htm','3.htm','4.htm', '5.htm', '6.htm', '7.htm', '8.htm'] #list of names of documents
    #assumes /data is the folder containing all data files
    #adds each one to the watson dictionary collection
    for file in data:
        with open((os.path.join(os.getcwd(), 'data', file))) as fileinfo: 
                    add_doc = discovery.add_document(environmentID, collectionID, file=fileinfo,   file_content_type = 'text/html')
                    #print(json.dumps(add_doc, indent=2))
    
    
    with open((os.path.join(os.getcwd(), 'data', 'Resume18.pdf'))) as fileinfo: 
        add_doc = discovery.add_document(environmentID, collectionID, file=fileinfo,   file_content_type = 'application/pdf')
        docID = (add_doc.result['document_id'])
        #print('\n' + str(docID) + '\n')
    
    response = discovery.query(environmentID, collectionID, similar=True, similar_document_ids=docID, similar_fields = None, count=1)
   
    print("\nMOST SIMILAR: " + str(response.result))
   
    discovery.delete_document(environmentID, collectionID, docID)
     
     
    keywords = ['PLC'] #list of features extracted from resume by watson NLU       
    results = {} #dictionary containing the query response each resume keyword returns
    for keyword in keywords:
        response = discovery.query(environmentID,collectionID,filter=keyword,query=keyword,count=5,passages=True)
        results[keyword] = response #response = list[QueryPassages]
    
    for entity in results['PLC'].result['passages']:
        print('\n''\"...' + str(entity['passage_text']) + '...\"''\n')
        
    with open((os.path.join(os.getcwd(), 'data', 'Resume18.pdf'))) as fileinfo: 
        add_doc = discovery.add_document(environmentID, collectionID, file=fileinfo,   file_content_type = 'application/pdf')
    docID = add_doc.result['document_id']
    
    discovery.delete_collection(environmentID, collectionID)
except:
    print('\noh well\n')
