import json
import requests

from utils import Lookup

#############################
####### PubMed Result #######
#############################

class PubMedResult( Lookup ):

	def __init__(self, meta):
		self.prep(meta)

	def prep(self, meta):
		self.source = 'pubmed'
		try:
			self.exid = meta['uid']
		except:
			raise ValueError('PubMedResult result missing pmid')
		self.data['source'] = self.source
		self.data['exid'] = self.exid
		self.data['pmid'] = self.exid
		try:
			self.data['title'] = meta['title']
		except:
			raise ValueError('CrossRef result missing title')
		try:
			self.data['date'] = meta['pubdate']
			self.data['year'] = meta['pubdate']
		except:
			pass
		try:
			self.data['venue_name'] = meta['fulljournalname']
			self.data['venue_abbrv'] = meta['source']
			self.data['venue_issn'] = meta['issn']
			self.data['venue_volume'] = meta['volume']
			self.data['venue_issue'] = meta['issue']
			self.data['pages'] = meta['pages']
		except:
			pass
		try:
			auth_list = [ auth['name'] for auth in meta['authors'] ]
			self.data['author_list'] = auth_list
			self.data['authors'] = ', '.join(auth_list)
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

		self.display['details'].append({'title': self.data['title']})
		if self.data['authors']:
			self.display['details'].append(
				{'authors': self.data['authors']}
			)
		if self.data['date']:
			self.display['details'].append(
				{'date': self.data['date']}
			)
		if self.data['venue_abbrv']:
			self.display['details'].append(
				{'journal': self.data['venue_abbrv']}
			)
		elif self.data['venue_name']:
			self.display['details'].append(
				{'journal': self.data['venue_name']}
			)
		if self.data['venue_volume']:
			self.display['details'].append(
				{'volume': self.data['venue_volume']}
			)
		if self.data['venue_issue']:
			self.display['details'].append(
				{'issue': self.data['venue_issue']}
			)
		if self.data['pages']:
			self.display['details'].append(
				{'pages': self.data['pages']}
			)
		self.display['details'].append({'ID': self.data['pmid']})

##########################
######## Process #########
##########################

def get_details(pmidList):
	esumm_base = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi'
	payload = { 'db': 'pubmed', 'retmode': 'json' }
	payload['id'] = ','.join(pmidList)
	resp = requests.post( esumm_base, data=payload )
	data = resp.json()
	out = []
	for uid in data['result']['uids']:
		meta = data['result'][uid]
		pubmed_result = PubMedResult(meta)
		out.append(pubmed_result)		
	return out