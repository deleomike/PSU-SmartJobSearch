from Functions import *
from watson_developer_cloud import NaturalLanguageUnderstandingV1 as NLU
from watson_developer_cloud.natural_language_understanding_v1 import Features, EntitiesOptions, KeywordsOptions
import PyPDF2
import docx


class CoverLetterParser():
	def __init__(self, filename):
		self.filename = filename
		self.extention = filename.split(".")[-1]

	def parse(self):
		if self.extention == 'docx':
			doc = docx.Document(self.filename)
			fullText = []
			for para in doc.paragraphs:
				fullText.append(para.text)
			text = '\n'.join(fullText)

		elif self.extention == 'txt':
			file = open(self.filename, 'r')
			text = file.read()
			file.close()

		elif self.extention == 'pdf':
			file = open(self.filename, 'rb')
			pdfReader = PyPDF2.PdfFileReader(file)
			pageObj = pdfReader.getPage(0)
			text = pageObj.extractText()
			file.close()

		else:
			print('Invalid File Extension.')
			text = ''

		return text


def get_letter(filename):
	# tests resume parser class
	resume = CoverLetterParser(filename)
	text = resume.parse()

	nlu = NLU(
		iam_apikey='BU11gy3frJMRMKz4XQ_sPJ_HGF3p-qEr74xUlEVTWvsY',
		version='2018-03-19'
	)

	response = nlu.analyze(
        language='en',
		text=text,
		features=Features(
			entities=EntitiesOptions(
				limit=1000
			),
			keywords=KeywordsOptions(
				limit=1000
			),
		)
	).get_result()

	# prints the text analysis from Watson nlu
	# jsonprinter(response)
	return response


