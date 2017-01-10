"https://pymotw.com/2/sqlite3/"

import sys
import csv
import os
import json
import sqlite3

def main(tsvFile):

	rabid_base = 'http://vivo.brown.edu/individual/'

	users = set()
	citations = set()
	cite_exids = set()
	hrv_exids = set()
	bad_json = set()

	with open(tsvFile, 'rb') as infile:
		rdr = csv.reader(infile, delimiter='\t')
		next(rdr, None)

		for row in rdr:
			user = rabid_base + row[1]
			users.add( (user, row[1]) )
			exids= []
			if row[2] != 'NULL':
				exids.append( (row[2],'doi') )
			if row[3] != 'NULL':
				exids.append( (row[3], 'pmid') )
			if row[4] != 'NULL':
				exids.append( (row[4], 'wosid') )
			try:
				cite_data = json.loads(row[8])
			except:
				bad_json.add( (row[0], row[5]) )
			if row[5] == 'a':
				uri = cite_data['citation'].get('uri', 'NULL')
				citations.add( (row[0], uri, user) )
				for tp in exids:
					cite_exids.add( (row[0], uri, tp[0], tp[1]) )
			for tp in exids:
				hrv_exids.add( (row[0], tp[0], user, tp[1], row[5]) )

	with open('users.csv', 'wb') as userFile:
		wrtr = csv.writer(userFile)
		wrtr.writerows(list(users))

	with open('citations.csv', 'wb') as citeFile:
		wrtr = csv.writer(citeFile)
		wrtr.writerows(list(citations))

	with open('cite_exids.csv', 'wb') as exidFile:
		wrtr = csv.writer(exidFile)
		wrtr.writerows(list(cite_exids))

	with open('hrv_exids.csv', 'wb') as exidFile:
		wrtr = csv.writer(exidFile)
		wrtr.writerows(list(hrv_exids))

	with open('bad_records.csv', 'wb') as badFile:
		wrtr = csv.writer(badFile)
		wrtr.writerows(list(bad_json))

if __name__ == "__main__":
	main(sys.argv[1])