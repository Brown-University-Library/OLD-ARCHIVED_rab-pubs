import json
import requests

class PubMedResult( object ):

	def __init__(self, meta):
		self.prep(meta)

	def prep(self, meta):
		self.source = 'pubmed'
		try:
			self.exid = meta['uid']
		except:
			raise ValueError('PubMedResult result missing pmid')
		self.data = { 	'source': self.source,
						'exid': self.exid,
						'ids' : { 'pmid' : self.exid }
					}
		try:
			self.data['title'] = meta['title']
		except:
			raise ValueError('CrossRef result missing title')

		self.data['date'] = {}
		try:
			self.data['date']['date'] = meta['pubdate']
		except:
			pass

		self.data['venue'] = {}
		try:
			self.data['venue']['name'] = meta['fulljournalname']
			self.data['venue']['abbrv'] = meta['source']
			self.data['venue']['issn'] = meta['issn']
			self.data['venue']['volume'] = meta['volume']
			self.data['venue']['issue'] = meta['issue']
			self.data['venue']['pages'] = meta['pages']
		except:
			pass

		self.data['authors'] = { 'list': [], 'string': ''}
		try:
			auth_list = [ auth['name'] for auth in meta['authors'] ]
			self.data['authors']['list'] = auth_list
			self.data['authors']['string'] = ', '.join(auth_list)
		except:
			pass

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