"""
bns5273
"""


# prints the text analysis from Watson nlu
def jsonprinter(response):
	print('\nJOB:\n keywords')
	for k in response['keywords']:
		print('  ', k['text'])

	print(' entities')
	for e in response['entities']:
		print('  ', e['text'])


# evaluates the match coefficient between a job posting and a resume / cover letter
# each input is a json retrieved from the watson NLU library
# TODO: implement for entities as well
# TODO: filter out locations, software engineer
def get_evaluation(posting, letter):
	posting_keywords = [k['text'] for k in posting['keywords']]
	# posting_entities = [k['text'] for k in posting['entities']]
	letter_keywords = [e['text'] for e in letter['keywords']]
	# letter_entities = [e['text'] for e in letter['entities']]

	keywords_union = set(posting_keywords) & set(letter_keywords)
	# entities_union = set(posting_entities) & set(letter_entities)
	print(len(keywords_union), '/', len(posting_keywords), '+', len(letter_keywords), '\t', keywords_union)
	# print(len(entities_union) / len(letter_entities), '\t', len(entities_union), '/', len(posting_entities) + len(letter_entities), entities_union)
	# print()
	return keywords_union
