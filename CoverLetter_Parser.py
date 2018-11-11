from watson_developer_cloud import NaturalLanguageUnderstandingV1 as NLU
from watson_developer_cloud.natural_language_understanding_v1 import Features, EntitiesOptions, KeywordsOptions
import json
import PyPDF2
import docx


class CoverLetter_Parser():
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
			file = open(self.filename, 'rb')
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

if __name__ == '__main__':
	# tests resume parser class
	resume = CoverLetter_Parser('data/ex2.docx')
	text = resume.parse()
	# print(text)

	nlu = NLU(
		iam_apikey='BU11gy3frJMRMKz4XQ_sPJ_HGF3p-qEr74xUlEVTWvsY',
		version='2018-03-19'
	)

	response = json.dumps(
		nlu.analyze(
			text=text,
			features=Features(
				entities=EntitiesOptions(
					# emotion=True,
					# sentiment=True,
					limit=5),
				# keywords=KeywordsOptions(
				# 	emotion=True,
				# 	sentiment=True,
				# 	limit=2),
			)
		).get_result(), indent=2)

	# prints the text analysis from Watson nlu
	print(response)

