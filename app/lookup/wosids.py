import json
import zeep
from utils import Lookup

###########################
## Web of Science result ##
###########################

class WosResult( Lookup ):

	def prep_meta(self, meta):
		self.source = 'wos'
		try:
			self.exid = meta['uid']
		except:
			raise ValueError('WOS result missing uid')
		self.data['source'] = self.source
		self.data['exid'] = self.exid
		self.data['wosid'] = self.exid
		try:
			self.data['title'] = meta['title'][0]['value'][0]
		except:
			raise ValueError('WOS result missing title')
		try:
			resp_srcs = meta['source']
		except:
			raise ValueError('WOS result missing source')
		for src in resp_srcs:
			if src['label'] == 'SourceTitle' and len(src['value']) != 0:
				self.data['venue_name'] = src['value'][0]
			if src['label'] == 'Issue' and len(src['value']) != 0:
				self.data['venue_issue'] = src['value'][0]
			if src['label'] == 'Volume' and len(src['value']) != 0:
				self.data['venue_volume'] = src['value'][0]
			if src['label'] == 'Pages' and len(src['value']) != 0:
				self.data['pages'] = src['value'][0]
			if src['label'] == 'Published.BiblioDate' and len(src['value']) != 0:
				self.data['date'] = src['value'][0]
			if src['label'] == 'Published.BiblioYear' and len(src['value']) != 0:
				self.data['year'] = src['value'][0]
		try:
			authors = meta['authors'][0]['value']
			self.data['author_list'] = authors
			self.data['authors'] = '; '.join(authors)
		except:
			pass
		try:
			keywords = meta['keywords'][0]['value']
			self.data['keyword_list'] = keywords
			self.data['keywords'] = ', '.join(keywords)
		except:
			pass

		for other in meta['other']:
			if src['label'] == 'Identifier.Doi' and len(other['value']) != 0:
				self.data['doi'] = other['value'][0]
			if src['label'] == 'Identifier.Issn' and len(other['value']) != 0:
				self.data['venue_issn'] = other['value'][0]

	def prep_display(self):
		self.display['short']['title'] = self.data['title']
		if self.data['venue_name']:
			self.display['short']['venue'] = self.data['venue_name']
		if self.data['year']:
			self.display['short']['date'] = self.data['year']

		self.display['details'].append(
			self.metadatum('title', self.data['title'])
			)
		if self.data['authors']:
			self.display['details'].append(
				self.metadatum('authors', self.data['authors'])
			)
		if self.data['year']:
			self.display['details'].append(
				self.metadatum('year', self.data['year'])
			)
		if self.data['date']:
			self.display['details'].append(
				self.metadatum('date', self.data['date'])
			)
		if self.data['venue_name']:
			self.display['details'].append(
				self.metadatum('journal', self.data['venue_name'])
			)
		if self.data['venue_volume']:
			self.display['details'].append(
				self.metadatum('volume', self.data['venue_volume'])
			)
		if self.data['venue_issue']:
			self.display['details'].append(
				self.metadatum('issue', self.data['venue_issue'])			)
		if self.data['pages']:
			self.display['details'].append(
				self.metadatum('pages', self.data['pages'])
			)
		if self.data['keywords']:
			self.display['details'].append(
				self.metadatum('keywords', self.data['keywords'])
			)
		self.display['details'].append(
			self.metadatum('ID', self.data['wosid'])
			)

##########################
######## Process #########
##########################

def get_details(wosidList, sid):
	### !!!!Need to handle MEDLINE: ids
	search_wsdl = 'http://search.webofknowledge.com/esti/wokmws/ws/WokSearchLite?wsdl'
	search_client = zeep.Client(wsdl=search_wsdl)

	sid_header =  { 'Cookie' : 'SID="{0}"'.format(sid) }
	search_client.transport.session.headers.update(sid_header)
	retrv_params = { 'firstRecord': 1 }
	params = { 'databaseId': 'WOS', 'queryLanguage': 'en' }
	out = []
	for i in range(0, len(wosidList), 100):
		wosChunk = wosidList[i:i+100]
		retrv_params['count'] = len(wosChunk)
		params['uid'] = wosChunk
		params['retrieveParameters'] = retrv_params
		resp = search_client.service.retrieveById( **params )
		for rec in resp['records']:
			wos_res = WosResult(rec)
			out.append(wos_res)
	return out