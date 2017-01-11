from app import db
from app.models import Users, HarvestSources, HarvestProcesses
import uuid
import csv
import os

vivo_base = "http://vivo.brown.edu/individual/"
curr_dir = os.path.dirname(os.path.realpath(__file__))
dataDir = os.path.join(curr_dir, 'data/')

def main():
	pubmed = HarvestSources()
	pubmed.rabid = vivo_base + uuid.uuid4().hex
	pubmed.name = "PubMed"
	db.session.add(pubmed)

	wos = HarvestSources()
	wos.rabid = vivo_base + uuid.uuid4().hex
	wos.name = "Web of Science"
	db.session.add(wos)

	acad = HarvestSources()
	acad.rabid = vivo_base + uuid.uuid4().hex
	acad.name = "Academic Analytics"
	db.session.add(acad)

	db.session.commit()

	with open(dataDir + 'users.csv','rb') as users:
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
	main()