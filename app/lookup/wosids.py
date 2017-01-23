import json
import zeep
from utils import Lookup

class WosResult( object ):

	def __init__(self, meta):
		self.prep(meta)

	def prep(self, meta):
		self.source = 'wos'
		try:
			self.exid = meta['uid']
		except:
			raise ValueError('WOS result missing uid')
		self.data = { 	'source': self.source,
						'exid': self.exid,
						'ids' : { 'wos' : self.exid }
					}
		try:
			self.data['title'] = meta['title'][0]['value'][0]
		except:
			raise ValueError('WOS result missing title')
		try:
			resp_srcs = meta['source']
		except:
			raise ValueError('WOS result missing source')
		self.data['venue'] = { 'pages' : {} }
		self.data['date'] = {}
		for src in resp_srcs:
			if src['label'] == 'SourceTitle' and len(src['value']) != 0:
				self.data['venue']['name'] = src['value'][0]
				self.data['venue']['abbrv'] = src['value'][0]
			if src['label'] == 'Issue' and len(src['value']) != 0:
				self.data['venue']['issue'] = src['value'][0]
			if src['label'] == 'Volume' and len(src['value']) != 0:
				self.data['venue']['volume'] = src['value'][0]
			if src['label'] == 'Pages' and len(src['value']) != 0:
				self.data['venue']['pages']['range'] = src['value'][0]
			if src['label'] == 'Published.BiblioDate' and len(src['value']) != 0:
				self.data['date']['year'] = src['value'][0]
			if src['label'] == 'Published.BiblioYear' and len(src['value']) != 0:
				self.data['date']['fulldate'] = src['value'][0] + ' ' + self.data['date']['year']

		self.data['authors'] = {}
		try:
			authors = meta['authors'][0]['value']
			self.data['authors']['list'] = authors
			self.data['authors']['string'] = ', '.join(authors)
		except:
			pass

		self.data['keywords'] = {}
		try:
			keywords = meta['keywords'][0]['value']
			self.data['keywords']['list'] = keywords
			self.data['keywords']['string'] = ', '.join(keywords)
		except:
			pass

		for other in meta['other']:
			if src['label'] == 'Identifier.Doi' and len(other['value']) != 0:
				self.data['ids']['doi'] = other['value'][0]
			if src['label'] == 'Identifier.Issn' and len(other['value']) != 0:
				self.data['venue']['issn'] = other['value'][0]

	def json(self):
		return json.dumps(self.data)

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