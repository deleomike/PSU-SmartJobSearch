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
