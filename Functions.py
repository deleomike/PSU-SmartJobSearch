"""

use 'from functions import *' to use

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
def evaluate(posting, letter):
    posting_keywords = []
    posting_entities = []
    letter_keywords = []
    letter_entities = []

    for k in posting['keywords']:
        posting_keywords.append(k['text'])
    for k in letter['keywords']:
        letter_keywords.append(k['text'])
    for e in posting['entities']:
        posting_entities.append(e['text'])
    for e in letter['entities']:
        letter_entities.append(e['text'])

    result = set(posting_keywords) & set(letter_keywords)
    print(len(result), '/', len(posting_keywords) + len(letter_keywords))
