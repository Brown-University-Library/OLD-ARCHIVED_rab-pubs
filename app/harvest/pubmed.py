import json
import requests


##########################
######## Process #########
##########################

def harvest(queryStr):
	esearch_base = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?'
	params = {	'db': 'pubmed',
				'retmode': 'json',
				'retmax': 10000,
				'term': queryStr }
	resp = requests.get( esearch_base, params=params )
	data = resp.json()
	out = data['esearchresult']['idlist']		
	return out