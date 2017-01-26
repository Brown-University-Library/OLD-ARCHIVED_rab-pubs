import json
import requests
import xml.etree.ElementTree as ET

from utils import Lookup

#############################
###### CrossRef Result ######
#############################

class CrossRefResult( Lookup ):

	def prep_meta(self, meta):
		self.source = 'crossref'
		try:
			doi = meta.find('journal_article/doi_data/doi').text
			self.exid = doi
		except:
			raise ValueError('CrossRef result missing doi')
		self.data['source'] = self.source
		self.data['exid'] = self.exid
		self.data['doi'] = self.exid
		try:
			self.data['title'] = meta.find(
				'journal_article/titles/title').text
		except:
			raise ValueError('CrossRef result missing title')
		try:
			self.data['year'] = meta.find(
				'journal_issue/publication_date/year').text
			self.data['date'] = self.data['year']
		except:
			pass
		try:
			jrn_meta = meta.find('journal_metadata')
			self.data['venue_name'] = jrn_meta.find('full_title').text
			self.data['venue_abbrv'] = jrn_meta.find('abbrev_title').text
			self.data['venue_issn'] = jrn_meta.find('issn').text
		except:
			pass
		try:
			issue_meta = meta.find('journal_issue')
			self.data['venue_volume'] = issue_meta.find(
								'journal_volume/volume').text
			self.data['venue_issue'] = issue_meta.find('issue').text
		except:
			pass
		try:
			auth_meta = meta.findall(
				'journal_article/contributors/person_name')
			for auth in auth_meta:
				last = auth.find('surname').text
				first = auth.find('given_name').text
				full_name = last + ', ' + first
				self.data['author_list'].append( full_name )
			self.data['authors'] = '; '.join(self.data['author_list'])
		except:
			pass
		try:
			pages_meta = meta.find('journal_article/pages')
			start = pages_meta.find('first_page').text
			end = pages_meta.find('last_page').text
			self.data['pages'] = start + "-" + end
		except:
			pass

	def prep_display(self):
		self.display['short']['title'] = self.data['title']
		if self.data['venue_abbrv']:
			self.display['short']['venue'] = self.data['venue_abbrv']
		elif self.data['venue_name']:
			self.display['short']['venue'] = self.data['venue_name']
		if self.data['date']:
			self.display['short']['date'] = self.data['date']

		self.display['details'].append(
			self.metadatum('title', self.data['title'])
			)
		if self.data['authors']:
			self.display['details'].append(
				self.metadatum('authors', self.data['authors'])
			)
		if self.data['date']:
			self.display['details'].append(
				self.metadatum('date', self.data['date'])
			)
		if self.data['venue_abbrv']:
			self.display['details'].append(
				self.metadatum('journal', self.data['venue_abbrv'])
			)
		elif self.data['venue_name']:
			self.display['details'].append(
				self.metadatum('journal', self.data['venue_name'])
			)
		if self.data['venue_volume']:
			self.display['details'].append(
				self.metadatum('volume', self.data['venue_volume'])
			)
		if self.data['venue_issue']:
			self.display['details'].append(
				self.metadatum('issue', self.data['venue_issue'])
			)
		if self.data['pages']:
			self.display['details'].append(
				self.metadatum('pages', self.data['pages'])
			)
		self.display['details'].append(
			self.metadatum('ID', self.data['doi'])
			)

##########################
######## Process #########
##########################

def request_crossref(doiChunk):
	crossref_base = 'https://doi.crossref.org/search/doi'
	params = { 'pid': 'steven_mccauley@brown.edu', 'format': 'unixref' }
	# https://github.com/kennethreitz/requests/issues/1186
	params['doi'] = doiChunk
	resp = requests.get( crossref_base, params=params )
	# Figure out a better way?
	tree = ET.fromstring(resp.text.encode('utf-8'))
	out = []
	for meta_tree in tree.findall('doi_record/crossref/journal'):
		crossref_result = CrossRefResult(meta_tree)
		out.append(crossref_result)	
	return out

def get_details(doiList):
	out = []
	for i in range(0, len(doiList), 50):
		doiChunk = doiList[i:i+50]
		lookup = request_crossref(doiChunk)
		out.extend(lookup)
	return out