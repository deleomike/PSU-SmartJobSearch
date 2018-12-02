import sys
import os
import json
from watson_developer_cloud import DiscoveryV1

#Active discovery instance
discovery = DiscoveryV1(
    version='2017-11-07', 
    api_key='gR4dbAo_IIcdVYAcL1VAafrQonD9FRJF-Imceur5LPXW', 
    url= "https://gateway.watsonplatform.net/discovery/api")

environment = discovery.create_environment(
    name="Job Files",
    description="Holds downloaded html files found by webcrawler"
).get_result()


collection = discovery.create_collection(
        environment_id='database.environment_id', 
        configuration_id='database_id', 
        name='Collection', 
        description='{collection_desc}').get_result()

#this line adds 
with open((os.path.join(os.getcwd(), '{folder name}', '{file name}'))) as fileinfo: 
        add_doc = discovery.add_document(environment.environment_id, collection.collection_id, file_info=fileinfo)
        print(json.dumps(add_doc, indent=2))


query(self, 
      environment_id, 
      collection_id, 
      filter=None, 
      query=None, 
      natural_language_query=None, 
      passages=True, aggregation=None, 
      count=10, return_fields=None, 
      offset=None, sort=None, highlight=None, 
      passages_fields=None, passages_count=None, 
      passages_characters=100, deduplicate=None, 
      deduplicate_field=None, collection_ids=None, 
      similar=None, similar_document_ids=None, 
      similar_fields=None, bias=None, 
      logging_opt_out=None, **kwargs)
