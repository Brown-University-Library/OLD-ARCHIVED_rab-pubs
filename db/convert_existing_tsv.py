"https://pymotw.com/2/sqlite3/"

import sys
import csv
import os
import json
import sqlite3

def main(tsvFile):

	rabid_base = 'http://vivo.brown.edu/individual/'

	users = set()
	citation = set()
	cite_exids = set()
	harvest_res = set()
	hrv_exids = set()
	status = set()
	bad_json = set()

	with open(tsvFile, 'rb') as infile:
		rdr = csv.reader(infile, delimiter='\t')
		next(rdr, None)

		for row in rdr:
			users.add( (rabid_base + row[1], row[1]) )
			exids= []
			if row[2] != 'NULL':
				exids.append( (row[2],'doi') )
			if row[3] != 'NULL':
				exids.append( (row[3], 'pmid') )
			if row[4] != 'NULL':
				exids.append( (row[4], 'wosid') )
			try:
				cite_data = json.loads(row[8])
				title = cite_data['citation']['title']
				date = cite_data['citation']['date']
				venue = cite_data['citation']['venue']['label']
				uri = cite_data['citation'].get('uri', 'NULL')
			except:
				bad_json.add( (row[0], row[5]) )
				title = 'NULL'
				date = 'NULL'
				venue = 'NULL'
				uri = 'NULL'
			if row[5] == 'a':
				citation.add( (row[0], rabid_base + row[1], uri) )
				for tp in exids:
					cite_exids.add( (row[0], tp[0], tp[1]) )
			else:
				harvest_res.add( (row[0], rabid_base + row[1], title, venue, date, row[5]) )
				for tp in exids:
					hrv_exids.add( (row[0], tp[0], tp[1]) )

	with open('users.csv', 'wb') as userFile:
		wrtr = csv.writer(userFile)
		wrtr.writerows(list(users))

	with open('citations.csv', 'wb') as citeFile:
		wrtr = csv.writer(citeFile)
		wrtr.writerows(list(citation))

	with open('cite_exids.csv', 'wb') as exidFile:
		wrtr = csv.writer(exidFile)
		wrtr.writerows(list(cite_exids))

	with open('harvest_records.csv', 'wb') as harvFile:
		wrtr = csv.writer(harvFile)
		wrtr.writerows(list(harvest_res))

	with open('hrv_exids.csv', 'wb') as exidFile:
		wrtr = csv.writer(exidFile)
		wrtr.writerows(list(hrv_exids))

	with open('bad_records.csv', 'wb') as badFile:
		wrtr = csv.writer(badFile)
		wrtr.writerows(list(bad_json))

if __name__ == "__main__":
	main(sys.argv[1])