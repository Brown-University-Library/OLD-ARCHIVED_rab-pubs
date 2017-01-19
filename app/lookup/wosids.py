import json
import zeep

def get_details(wosidList, sid):
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
			exid = rec['uid']
			title = rec['title'][0]['value'][0]
			for src in rec['source']:
				if src['label'] == 'SourceTitle':
					pub = src['value'][0]
				if src['label'] == 'Published.BiblioYear':
					pubdate = src['value'][0]
			try:
				display = "{0} {1} {2}".format(title, pub, pubdate)
			except:
				print "Could not format: " + str(exid)
			lookup_obj = {}
			meta = list()
			meta.extend(rec['source'])
			meta.extend(rec['authors'])
			meta.extend(rec['keywords'])
			lookup_obj['meta'] = meta
			lookup_obj['display'] = display
			lookup_obj['exid'] = exid
			out.append(lookup_obj)
	return out