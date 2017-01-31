import json
import requests


# https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&retmode=json&retmax=10000&term=Sarkar%20IN%5BAuthor%5D%20AND%20Brown%5BAffiliation%5

params = [
	'Affiliation',
	'All Fields',
	'Author - Corporate',
	'Author - First',
	'Author - Full',
	'Author - Identifier',
	'Author - Last',
	'Book',
	'Date - Completion',
	'Date - Create',
	'Date - Entrez',
	'Date - MeSH',
	'Date - Modification',
	'Date - Publication',
	'EC/RN Number',
	'Editor',
	'Filter',
	'Grant Number',
	'ISBN',
	'Investigator',
	'Investigator - Full',
	'Issue',
	'Journal',
	'Language',
	'Location ID',
	'MeSH Major Topic',
	'MeSH Subheading',
	'MeSH Terms',
	'Other Term',
	'Pagination',
	'Pharmacological Action',
	'Publication Type',
	'Publisher',
	'Secondary Source ID',
	'Subject - Personal Name',
	'Supplementary Concept',
	'Text Word',
	'Title',
	'Title/Abstract',
	'Transliterated Title',
	'Volume'
	]

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