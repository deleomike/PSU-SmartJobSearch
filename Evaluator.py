"""
bns5273
basically the main function until this is moved into gui
compares sets of keywords from job postings and resumes and sorts the postings by the most in-common keywords
"""

from Functions import *
from IndeedCrawler import posting_generator
from CoverLetterParser import get_letter


class Evaluator:
	def __init__(self, filename, limit):
		letter = get_letter(filename)

		self.keywords = []
		self.keywords_matched = []
		urls = []
		keywords_union = []
		i = 0
		jobTitle = "software developer"
		jobLocation = "Pittsburgh, PA"
		for url, posting in posting_generator(jobTitle, jobLocation):
			response = get_evaluation(posting, letter)  # in-common keywords

			urls.append(url)
			keywords_union.append(response)
			self.keywords += [e['text'] for e in posting['keywords']]     # all keywords
			self.keywords_matched += response

			i += 1
			if i == limit:
				break

		# sorts job urls and evaluations together by the length of the keyword union set :)
		self.all_sorted = sorted(zip(urls, keywords_union), key=lambda ele: len(ele[1]), reverse=True)
		print(self.all_sorted)

	def getAllEvaluations(self):
		return self.all_sorted

	def getCommonMatchedKeywords(self):
		# most commonly matched keywords already in resume
		common_matched = {}
		for word in self.keywords_matched:
			if word in common_matched:
				common_matched[word] += 1
			else:
				common_matched[word] = 1
		common_matched = sorted(common_matched, key=common_matched.get, reverse=True)
		print('common matched keywords', common_matched)
		return common_matched

	def getCommonAllKeywords(self):
		# most common keywords in job postings
		common_all = {}
		for word in self.keywords:
			if word in common_all:
				common_all[word] += 1
			else:
				common_all[word] = 1
		common_all = sorted(common_all, key=common_all.get, reverse=True)
		print('common keywords', common_all)
		return common_all


if __name__ == '__main__':
	evaluator = Evaluator('data/ex1.txt', 10)
	matched = evaluator.getCommonMatchedKeywords()
	all = evaluator.getCommonAllKeywords()
