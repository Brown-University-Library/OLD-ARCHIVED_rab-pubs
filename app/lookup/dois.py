import json
import requests
import xml.etree.ElementTree as ET

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
		lookup_obj = { "display": None, "exid": None, "meta": None }
		meta = meta_tree.text
		doi = meta_tree.find('journal_article/doi_data/doi').text
		title = meta_tree.find('journal_article/titles/title').text
		pubdate = meta_tree.find('journal_issue/publication_date/year').text
		pub = meta_tree.find('journal_metadata/full_title').text
		try:
			display = "{0} {1} {2}".format(title, pub, pubdate)
		except:
			print "Could not format: " + str(doi)
			continue
		lookup_obj['display'] = display
		lookup_obj['meta'] = meta
		lookup_obj['exid'] = doi
		out.append(lookup_obj)		
	return out

def get_details(doiList):
	out = []
	for i in range(0, len(doiList), 30):
		doiChunk = doiList[i:i+30]
		lookup = request_crossref(doiChunk)
		out.extend(lookup)
	return out