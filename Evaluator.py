"""
basically the main function until this is moved into gui
"""

from Functions import *
from IndeedCrawler import posting_generator
from CoverLetterParser import get_letter


letter = get_letter('data/brad.pdf')

for posting in posting_generator():
	evaluate(posting, letter)
