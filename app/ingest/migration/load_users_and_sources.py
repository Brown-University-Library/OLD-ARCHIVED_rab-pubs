from app import db, app
from app.models import local
import uuid
import csv
import sys
import os
import requests

from app.utils import namespaces

hrv_base = os.path.join(app.config['REST_BASE'], 'harvest')
headers = {	'Content-type': 'application/json',
		'Accept': 'text/plain',
		'Connection': 'close' }

def main(userFile):
	source_api = os.path.join(hrv_base, 'sources/')

	pubmed_data = dict()
	pubmed_data['label'] = ["PubMed"]
	pubmed_data['class'] = [ namespaces.BHARVEST + "Source" ]
	resp = requests.post(source_api, headers=headers, json=pubmed_data)
	if resp.status_code == 200:
		pubmed = local.HarvestSources()
		pubmed.rabid = resp.json().keys()[0]
		pubmed.display = resp.json()[pubmed.rabid]['label'][0]
		pubmed.rabclass = resp.json()[pubmed.rabid]['class'][0]
		db.session.add(pubmed)

	wos_data = dict()
	wos_data['label'] = ["Web of Science"]
	wos_data['class'] = [ namespaces.BHARVEST + "Source" ]
	resp = requests.post(source_api, headers=headers, json=wos_data)
	if resp.status_code == 200:
		wos = local.HarvestSources()
		wos.rabid = resp.json().keys()[0]
		wos.display = resp.json()[wos.rabid]['label'][0]
		wos.rabclass = resp.json()[wos.rabid]['class'][0]
		db.session.add(wos)

	acad_data = dict()
	acad_data['label'] = ["Academic Analytics"]
	acad_data['class'] = [ namespaces.BHARVEST + "Source" ]
	resp = requests.post(source_api, headers=headers, json=acad_data)
	if resp.status_code == 200:
		acad = local.HarvestSources()
		acad.rabid = resp.json().keys()[0]
		acad.display = resp.json()[acad.rabid]['label'][0]
		acad.rabclass = resp.json()[acad.rabid]['class'][0]
		db.session.add(acad)

	db.session.commit()

	with open(userFile,'rb') as users:
		reader = csv.reader(users)
		pbmd = local.HarvestSources.query.filter_by(display="PubMed").first()
		web = local.HarvestSources.query.filter_by(display="Web of Science").first()
		acd = local.HarvestSources.query.filter_by(display="Academic Analytics").first()

		process_api = os.path.join(hrv_base, 'processes/')

		for row in reader:
			user = local.Users()
			user.rabid = row[0]
			user.short_id = row[1]
			db.session.add(user)
			
			proc_data = dict()
			proc_data['label'] = ["PubMed Django Migration"]
			proc_data['class'] = [ namespaces.BHARVEST + "HarvestProcess", namespaces.BHARVEST + "PubMedSearch" ]
			proc_data['user'] = [ row[0] ]
			proc_data['source'] = [ pbmd.rabid ]
			proc_data['status'] = [ 'i' ]
			proc_data['query'] = []
			resp = requests.post(process_api, headers=headers, json=proc_data)
			if resp.status_code == 200:
				proc = local.HarvestProcesses()
				proc.rabid = resp.json().keys()[0]
				proc.display = resp.json()[proc.rabid]['label'][0]
				proc.source_rabid = resp.json()[proc.rabid]['source'][0]
				proc.user_rabid = resp.json()[proc.rabid]['user'][0]
				proc.status = resp.json()[proc.rabid]['status'][0]
				#pbmd_proc.rabclass = namespaces.BHARVEST + "DjangoMigration"
				proc.rabclass = namespaces.BHARVEST + "PubMedSearch"
				db.session.add(proc)

			proc_data = dict()
			proc_data['label'] = ["WOS Django Migration"]
			proc_data['class'] = [ namespaces.BHARVEST + "HarvestProcess", namespaces.BHARVEST + "WebOfScienceSearch" ]
			proc_data['user'] = [ row[0] ]
			proc_data['source'] = [ web.rabid ]
			proc_data['status'] = [ 'i' ]
			proc_data['query'] = []
			resp = requests.post(process_api, headers=headers, json=proc_data)
			if resp.status_code == 200:
				proc = local.HarvestProcesses()
				proc.rabid = resp.json().keys()[0]
				proc.display = resp.json()[proc.rabid]['label'][0]
				proc.source_rabid = resp.json()[proc.rabid]['source'][0]
				proc.user_rabid = resp.json()[proc.rabid]['user'][0]
				proc.status = resp.json()[proc.rabid]['status'][0]
				#pbmd_proc.rabclass = namespaces.BHARVEST + "DjangoMigration"
				proc.rabclass = namespaces.BHARVEST + "WebOfScienceSearch"
				db.session.add(proc)

			proc_data = dict()
			proc_data['label'] = ["AA Django Migration"]
			proc_data['class'] = [ namespaces.BHARVEST + "HarvestProcess", namespaces.BHARVEST + "AcademicAnalyticsUpload" ]
			proc_data['user'] = [ row[0] ]
			proc_data['source'] = [ acd.rabid ]
			proc_data['status'] = [ 'i' ]
			proc_data['query'] = []
			resp = requests.post(process_api, headers=headers, json=proc_data)
			if resp.status_code == 200:
				proc = local.HarvestProcesses()
				proc.rabid = resp.json().keys()[0]
				proc.display = resp.json()[proc.rabid]['label'][0]
				proc.source_rabid = resp.json()[proc.rabid]['source'][0]
				proc.user_rabid = resp.json()[proc.rabid]['user'][0]
				proc.status = resp.json()[proc.rabid]['status'][0]
				#pbmd_proc.rabclass = namespaces.BHARVEST + "DjangoMigration"
				proc.rabclass = namespaces.BHARVEST + "AcademicAnalyticsUpload"
				db.session.add(proc)

		db.session.commit()

if __name__ == '__main__':
	main(sys.argv[1])
