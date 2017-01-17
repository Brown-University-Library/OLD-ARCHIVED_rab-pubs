import json
import requests

def get_details(pmidList):
	pmids = [ exid.exid for exid in source_names['PubMed'] ]
	esumm_base = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi'
	payload = { 'db': 'pubmed', 'retmode': 'json' }
	payload['id'] = ','.join(pmids)
	resp = requests.post( esumm_base, data=payload )
	data = resp.json()
	pubmed_list = list(source_names['PubMed'])
	for uid in data['result']['uids']:
		meta = data['result'][uid]
		title = meta['title']
		pubdate = meta['pubdate']
		pub = meta['source']
		try:
			article = "{0} {1} {2}".format(title, pub, pubdate)
		except:
			article = "foo"
		for n, i in enumerate(source_names['PubMed']):
			if i.exid == uid:
				pubmed_list[n] = article
	source_names['PubMed'] = pubmed_list