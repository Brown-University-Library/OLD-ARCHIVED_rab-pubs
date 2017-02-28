from app import db
from app.models import local
import uuid
import csv
import sys

from app.utils import namespaces

def main(userFile):
	pubmed = local.HarvestSources()
	pubmed.rabid = namespaces.RABID + uuid.uuid4().hex
	pubmed.display = "PubMed"
	pubmed.rabclass = namespaces.BHARVEST + "HarvestSource"
	db.session.add(pubmed)

	wos = local.HarvestSources()
	wos.rabid = namespaces.RABID + uuid.uuid4().hex
	wos.display = "Web of Science"
	wos.rabclass = namespaces.BHARVEST + "HarvestSource"
	db.session.add(wos)

	acad = local.HarvestSources()
	acad.rabid = namespaces.RABID + uuid.uuid4().hex
	acad.display = "Academic Analytics"
	acad.rabclass = namespaces.BHARVEST + "HarvestSource"
	db.session.add(acad)

	db.session.commit()

	with open(userFile,'rb') as users:
		reader = csv.reader(users)
		pbmd = local.HarvestSources.query.filter_by(display="PubMed").first()
		web = local.HarvestSources.query.filter_by(display="Web of Science").first()
		acd = local.HarvestSources.query.filter_by(display="Academic Analytics").first()

		for row in reader:
			user = local.Users()
			user.rabid = row[0]
			user.short_id = row[1]
			db.session.add(user)
			
			pbmd_proc = local.HarvestProcesses()
			pbmd_proc.rabid = namespaces.RABID + uuid.uuid4().hex
			pbmd_proc.user_rabid = row[0]
			pbmd_proc.source_rabid = pbmd.rabid
			pbmd_proc.display = "Django migration"
			pbmd_proc.status = 'i'
			#pbmd_proc.rabclass = namespaces.BHARVEST + "DjangoMigration"
			pbmd_proc.rabclass = namespaces.BHARVEST + "PubMedSearch"
			db.session.add(pbmd_proc)

			web_proc = local.HarvestProcesses()
			web_proc.rabid = namespaces.RABID + uuid.uuid4().hex
			web_proc.user_rabid = row[0]
			web_proc.source_rabid = web.rabid
			web_proc.display = "Django migration"
			web_proc.status = 'i'
			#web_proc.rabclass = namespaces.BHARVEST + "DjangoMigration"
			web_proc.rabclass = namespaces.BHARVEST + "WebOfScienceSearch"
			db.session.add(web_proc)

			acd_proc = local.HarvestProcesses()
			acd_proc.rabid = namespaces.RABID + uuid.uuid4().hex
			acd_proc.user_rabid = row[0]
			acd_proc.source_rabid = acd.rabid
			acd_proc.display = "Django migration"
			acd_proc.status = 'i'
			#acd_proc.rabclass = namespaces.BHARVEST + "DjangoMigration"
			acd_proc.rabclass = namespaces.BHARVEST + "AcademicAnaylticsUpload"
			db.session.add(acd_proc)

		db.session.commit()

if __name__ == '__main__':
	main(sys.argv[1])
