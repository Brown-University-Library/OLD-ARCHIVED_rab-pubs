from app import db
from app.models import HarvestRecords, HarvestRecordExids, Users
from collections import defaultdict
import csv

def main():
	exid_dict = defaultdict(dict)

	with open('db/users.csv', 'rb') as userFile:
		reader = csv.reader(userFile)
		for row in reader:
			user = Users()
			user.rabid = row[0]
			user.short_id = row[1]
			db.session.add(user)
		db.session.commit()

	with open('db/hrv_exids.csv','rb') as exids:
		reader = csv.reader(exids)
		for row in reader:
			exid_dict[row[0]][row[2]] = row[1]

	with open('db/harvest_records.csv','rb') as hrecs:
		reader = csv.reader(hrecs)
		for row in reader:
			rec = HarvestRecords()
			rec.user_rabid = row[1]
			rec.title = row[2]
			rec.date = row[3]
			rec.status = row[4]
			db.session.add(rec)
			db.session.commit()
			exid_data = exid_dict[row[0]]
			for data in exid_data.items():
				ex = HarvestRecordExids()
				ex.record_id = rec.id
				ex.exid = data[1]
				ex.domain = data[0]
				db.session.add(ex)

if __name__ == '__main__':
	main()