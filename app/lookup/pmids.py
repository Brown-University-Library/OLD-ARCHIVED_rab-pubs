import json
import requests

def get_details(pmidList):
	esumm_base = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi'
	payload = { 'db': 'pubmed', 'retmode': 'json' }
	payload['id'] = ','.join(pmidList)
	resp = requests.post( esumm_base, data=payload )
	data = resp.json()
	out = []
	for uid in data['result']['uids']:
		lookup_obj = { "display": None, "exid": None, "meta": None }
		meta = data['result'][uid]
		title = meta['title']
		pubdate = meta['pubdate']
		pub = meta['source']
		try:
			display = "{0} {1} {2}".format(title, pub, pubdate)
		except:
			print "Could not format: " + str(uid)
			continue
		lookup_obj['display'] = display
		lookup_obj['meta'] = meta
		lookup_obj['exid'] = uid
		out.append(lookup_obj)		
	return out