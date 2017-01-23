import json
import requests
import xml.etree.ElementTree as ET

class CrossRefResult( object ):

	def __init__(self, meta):
		self.prep(meta)

	def prep(self, meta):
		self.source = 'crossref'
		try:
			doi = meta.find('journal_article/doi_data/doi').text
			self.exid = doi
		except:
			raise ValueError('CrossRef result missing doi')
		self.data = { 	'source': self.source,
						'exid': self.exid,
						'ids' : { 'doi' : self.exid }
					}
		try:
			self.data['title'] = meta.find('journal_article/titles/title').text
		except:
			raise ValueError('CrossRef result missing title')

		self.data['date'] = {}
		try:
			self.data['date']['year'] = meta.find('journal_issue/publication_date/year').text
		except:
			pass

		self.data['venue'] = {}
		try:
			jrn_meta = meta.find('journal_metadata')
			self.data['venue']['name'] = jrn_meta.find('full_title').text
			self.data['venue']['abrv'] = jrn_meta.find('abbrev_title').text
			self.data['venue']['issn'] = jrn_meta.find('issn').text
		except:
			pass
		try:
			issue_meta = meta.find('journal_issue')
			self.data['venue']['volume'] = issue_meta.find('journal_volume/volume').text
			self.data['venue']['issue'] = issue_meta.find('issue').text
		except:
			pass

		self.data['authors'] = { 'list': [], 'string': ''}
		try:
			auth_meta = meta.findall('journal_article/contributors')
			for auth in auth_meta:
				last = auth.find('person_name/surname').text
				first = auth.find('person_name/given_name').text
				full_name = last + ', ' + first
				self.data['authors']['list'].append( full_name )
				self.data['authors']['string'] += full_name
		except:
			pass

		self.data['venue']['pages'] = {}
		try:
			pages_meta = meta.find('journal_article/pages')
			self.data['venue']['pages']['start'] = pages_meta.find('first_page').text
			self.data['venue']['pages']['end'] = pages_meta.find('last_page').text
		except:
			pass

	def json(self):
		return json.dumps(self.data)


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
		# lookup_obj = { "display": None, "exid": None, "meta": None }
		# meta = meta_tree.text
		# doi = meta_tree.find('journal_article/doi_data/doi').text
		# title = meta_tree.find('journal_article/titles/title').text
		# pubdate = meta_tree.find('journal_issue/publication_date/year').text
		# pub = meta_tree.find('journal_metadata/full_title').text
		# try:
		# 	display = "{0} {1} {2}".format(title, pub, pubdate)
		# except:
		# 	print "Could not format: " + str(doi)
		# 	continue
		# lookup_obj['display'] = display
		# lookup_obj['meta'] = meta
		# lookup_obj['exid'] = doi
		# out.append(lookup_obj)		
	return out

def get_details(doiList):
	out = []
	for i in range(0, len(doiList), 50):
		doiChunk = doiList[i:i+50]
		lookup = request_crossref(doiChunk)
		out.extend(lookup)
	return out