"""
*** work in progress ***
"""

from watson_developer_cloud import NaturalLanguageUnderstandingV1 as NLU
from watson_developer_cloud.natural_language_understanding_v1 import Features, EntitiesOptions, KeywordsOptions
import json
import PyPDF2


class Resume_Parser():
	def __init__(self, filename):
		self.file = open(filename, 'rb')

	def parse(self):
		self.text = self.file.read()


class Pdf_Parser(Resume_Parser):
	def __init__(self, filename):
		super().__init__(filename)

	def parse(self):
		pdfReader = PyPDF2.PdfFileReader(self.file)
		pageObj = pdfReader.getPage(0)
		text = pageObj.extractText()
		print(text)

		self.file.close()


# class odt_parser(resume_parser):
# 	def parse(self):


# class docx_parser(resume_parser):
# 	def parse(self):


if __name__ == '__main__':
	# tests resume parser class
	resume = Pdf_Parser('data/Resume.pdf')
	resume.parse()
