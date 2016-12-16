"https://pymotw.com/2/sqlite3/"

import sys
import csv
import os
import sqlite3

def writeSql(tableName, columnList):
	sql_template = """
				insert into {0}
				({1})
				values ({2})
				"""
	cStr = ",".join(columnList)
	qStr = ",".join(["?" for c in columnList])
	return sql_template.format(tableName, cStr, qStr)

def updateTable(cursor, tDict):
	with open(tDict["file"], 'rt') as csv_file:
		csv_reader = csv.reader(csv_file)
		seeds = [ tuple(row) for row in csv_reader ]
	sql = writeSql(tDict['table'],tDict['columns'])
	cursor.executemany(sql, seeds)

def main(dbDir, loadDir):
	db_filename = os.path.join(dbDir,'visualizations.db')
	tables = {
		"faculty": {
			"file": os.path.join(loadDir,"faculty_data.csv"),
			"table": "faculty",
			"columns": ["rabid","lastname","firstname","fullname",
						"abbrev","title","deptid"]
		},
		"departments": {
			"file": os.path.join(loadDir,"departments_data.csv"),
			"table": "departments",
			"columns": ["rabid","label","useFor"]
		},
		"coauthors": {
			"file": os.path.join(loadDir,"coauthors_data.csv"),
			"table": "coauthors",
			"columns": ["authid","coauthid","cnt"]
		},
		"authorJson": {
			"file": os.path.join(loadDir,"author_json_data.csv"),
			"table": "author_json",
			"columns": ["facid", "jsondata"]
		},
		"affiliations": {
			"file": os.path.join(loadDir,"affiliations_data.csv"),
			"table": "affiliations",
			"columns": ["facid", "deptid", "rank"]
		},
		"chordDeptViz": {
			"file": os.path.join(loadDir,"viz_chord_dept_data.csv"),
			"table": "chord_viz",
			"columns": ["rabid", "page", "legend", "matrix"]
		},
		"chordFacViz": {
			"file": os.path.join(loadDir,"viz_chord_fac_data.csv"),
			"table": "chord_viz",
			"columns": ["rabid", "page", "legend", "matrix"]
		},
		"forceDeptViz": {
			"file": os.path.join(loadDir,"viz_force_dept_data.csv"),
			"table": "force_viz",
			"columns": ["rabid", "page", "legend", "links"]
		},
		"forceFacViz": {
			"file": os.path.join(loadDir,"viz_force_fac_data.csv"),
			"table": "force_viz",
			"columns": ["rabid", "page", "legend", "links"]
		}
	} 

	with sqlite3.connect(db_filename) as conn:
			print 'DELETING DATA'

			cursor = conn.cursor()
			delete_script = """
							DELETE FROM {0}
							"""
			for tDict in tables.values():
				cursor.execute(delete_script.format(tDict['table']))
			cursor.execute("VACUUM")

			print "Seeding database"

			for tDict in tables.values():
				updateTable(cursor, tDict)

if __name__ == "__main__":
	main(sys.argv[1], sys.argv[2])