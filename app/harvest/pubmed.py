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

param_map = {
	'title_abstract': 'Title/Abstract',
	'last_name': 'Author - Last',
	'isbn': 'ISBN',
	'mesh_terms': 'MeSH Terms',
	'affiliation': 'Affiliation',
	'full_name': 'Author - Full',
	'mesh_date': 'Date - MeSH',
	'location_id': 'Location ID',
	'publication_type': 'Publication Type',
	'sbj_personal_name': 'Subject - Personal Name',
	'all_fields': 'All Fields',
	'first_name': 'Author - First',
	'entrez_date': 'Date - Entrez',
	'title': 'Title',
	'journal': 'Journal',
	'translit_title': 'Transliterated Title',
	'investigator_full': 'Investigator - Full',
	'supplmnt_concept': 'Supplementary Concept',
	'book': 'Book',
	'editor': 'Editor',
	'issue': 'Issue',
	'ecrn_num': 'EC/RN Number',
	'text_word': 'Text Word',
	'other_term': 'Other Term',
	'grant_num': 'Grant Number',
	'completed_date': 'Date - Completion',
	'volume': 'Volume',
	'mesh_major': 'MeSH Major Topic',
	'mod_date': 'Date - Modification',
	'publication_date': 'Date - Publication',
	'publisher': 'Publisher',
	'pagination': 'Pagination',
	'mesh_subhead': 'MeSH Subheading',
	'language': 'Language',
	'investigator': 'Investigator',
	'secondary_src_id': 'Secondary Source ID',
	'pharma_action': 'Pharmacological Action',
	'filter_param': 'Filter',
	'created_date': 'Date - Create',
	'author_id': 'Author - Identifier',
	'corporate': 'Author - Corporate'
}


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