"""

use 'from functions import *' to use

"""


# prints the text analysis from Watson nlu
def jsonprinter(response):
    print('keywords')
    for k in response['keywords']:
        print('  ', k['text'])

    print('\nentities')
    for e in response['entities']:
        print('  ', e['text'])
