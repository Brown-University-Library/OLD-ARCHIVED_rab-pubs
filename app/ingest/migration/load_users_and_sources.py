from app import db
from app.models import Users, HarvestSources, HarvestProcesses
import uuid
import csv
import sys

vivo_base = "http://vivo.brown.edu/individual/"

wos_params = {
	'topic':'Topic',
	'title':'Title',
	'author':'Author',
	'author_ids':'Author Identifiers',
	'group_author':'Group Author',
	'editor':'Editor',
	'publication':'Publication Name',
	'doi':'DOI',
	'year':'Year Published',
	'address':'Address',
	'organizations':'Organizations-Enhanced',
	'conference':'Conference',
	'language':'Language',
	'doc_typ':'Document Type',
	'funding_agency':'Funding Agency',
	'grant_number':'Grant Number',
	'accession_number':'Accession Number',
	'pmid':'PubMed ID'
}

pubmed_params = {
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

def main(userFile):
	pubmed = HarvestSources()
	pubmed.rabid = vivo_base + uuid.uuid4().hex
	pubmed.name = "PubMed"
	pubmed.params = pubmed_params
	db.session.add(pubmed)

	wos = HarvestSources()
	wos.rabid = vivo_base + uuid.uuid4().hex
	wos.name = "Web of Science"
	wos.params = wos_params
	db.session.add(wos)

	acad = HarvestSources()
	acad.rabid = vivo_base + uuid.uuid4().hex
	acad.name = "Academic Analytics"
	acad.params = {}
	db.session.add(acad)

	db.session.commit()

	with open(userFile,'rb') as users:
		reader = csv.reader(users)
		pbmd = HarvestSources.query.filter_by(name="PubMed").first()
		web = HarvestSources.query.filter_by(name="Web of Science").first()
		acd = HarvestSources.query.filter_by(name="Academic Analytics").first()

		for row in reader:
			user = Users()
			user.rabid = row[0]
			user.short_id = row[1]
			db.session.add(user)
			
			pbmd_proc = HarvestProcesses()
			pbmd_proc.rabid = vivo_base + uuid.uuid4().hex
			pbmd_proc.user_rabid = row[0]
			pbmd_proc.source_rabid = pbmd.rabid
			pbmd_proc.process_data = "Django migration"
			pbmd_proc.status = 'i'
			db.session.add(pbmd_proc)

			web_proc = HarvestProcesses()
			web_proc.rabid = vivo_base + uuid.uuid4().hex
			web_proc.user_rabid = row[0]
			web_proc.source_rabid = web.rabid
			web_proc.process_data = "Django migration"
			web_proc.status = 'i'
			db.session.add(web_proc)

			acd_proc = HarvestProcesses()
			acd_proc.rabid = vivo_base + uuid.uuid4().hex
			acd_proc.user_rabid = row[0]
			acd_proc.source_rabid = acd.rabid
			acd_proc.process_data = "Django migration"
			acd_proc.status = 'i'
			db.session.add(acd_proc)

		db.session.commit()

if __name__ == '__main__':
	main(sys.argv[1])