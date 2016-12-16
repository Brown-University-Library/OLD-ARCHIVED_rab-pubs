"https://pymotw.com/2/sqlite3/"

import sys
import csv
import os
import sqlite3

db_dir = os.path.abspath(os.path.dirname(__file__))

def main():
	db_filename = os.path.join(db_dir,'rabpubs.db')
	schema_filename = os.path.join(db_dir,'schema.sql')

	db_is_new = not os.path.exists(db_filename)
	
	with sqlite3.connect(db_filename) as conn:
		if db_is_new:
			print 'Creating schema'
			with open(schema_filename, 'rt') as f:
				schema = f.read()
			conn.executescript(schema)
		else:
			print "Database exists"

if __name__ == "__main__":
	main()