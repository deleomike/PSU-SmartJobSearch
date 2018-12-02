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
    posting_keywords = [k['text'] for k in posting['keywords']]
    posting_entities = [k['text'] for k in letter['keywords']]
    letter_keywords = [e['text'] for e in posting['entities']]
    letter_entities = [e['text'] for e in letter['entities']]

    result = set(posting_keywords) & set(letter_keywords)
    print(len(result) / len(posting_keywords), '\t', len(result), '/', len(posting_keywords) + len(letter_keywords), result)
