"""
basically the main function until this is moved into gui
compares sets of keywords from job postings and resumes and sorts the postings by the most in-common keywords
"""

from Functions import *
from IndeedCrawler import posting_generator
from CoverLetterParser import get_letter


letter = get_letter('data/ex1.txt')

keywords = []
keywords_matched = []
urls = []
keywords_union = []
i = 0
for url, posting in posting_generator():
	response = get_evaluation(posting, letter)  # in-common keywords

	urls.append(url)
	keywords_union.append(response)
	keywords += [e['text'] for e in posting['keywords']]     # all keywords
	keywords_matched += response

	i += 1
	if i == 3:
		break

# sorts job urls and evaluations together by the length of the keyword union set :)
all_sorted = sorted(zip(urls, keywords_union), key=lambda ele: len(ele[1]), reverse=True)
print(all_sorted)

# most commonly matched keywords already in resume
common_matched = {}
for word in keywords_matched:
	if word in common_matched:
		common_matched[word] += 1
	else:
		common_matched[word] = 1
common_matched = sorted(common_matched, key=common_matched.get, reverse=True)
print('common matched keywords', common_matched)

# most common keywords in job postings
common_all = {}
for word in keywords:
	if word in common_all:
		common_all[word] += 1
	else:
		common_all[word] = 1
common_all = sorted(common_all, key=common_all.get, reverse=True)
print('common keywords', common_all)
