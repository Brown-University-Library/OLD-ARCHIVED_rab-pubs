from app import db
from app.models import HarvestEvents, HarvestProcesses, HarvestSources

from collections import defaultdict
import csv
import os
from datetime import datetime

curr_dir = os.path.dirname(os.path.realpath(__file__))
dataDir = os.path.join(curr_dir, 'data/')

def main():
	srcs = HarvestSources.query.all()
	src_rabids_map = { src.rabid: src.name for src in srcs }
	src_names_map = { src.name: src.rabid for src in srcs }

	procs = HarvestProcesses.query.all()
	proc_user_map = {}
	proc_src_map = {}
	for proc in procs:
		event = HarvestEvents()
		event.proc_rabid = proc.rabid
		event.event_date = datetime.now()
		event.user_initiated = False
		db.session.add(event)

		proc_user_map[proc.rabid] = proc.user_rabid
		src_name = src_rabids_map[proc.source_rabid]
		proc_src_map[proc.rabid] = src_name
	db.session.commit()

	events = HarvestEvents.query.all()
	user_event_map = defaultdict(dict)
	for event in events:
		user_rabid = proc_user_map[event.proc_rabid]
		src_name = proc_src_map[event.proc_rabid]
		user_event_map[user_rabid][src_name] = event.id

	rows = []
	with open(dataDir + 'hrv_exids.csv','rb') as exids:
		reader = csv.reader(exids)

		for row in reader:
			exid = row[0]
			event_id = user_event_map[row[1]][row[2]]
			user_rabid = row[1]
			source_rabid = src_names_map[row[2]]
			status = row[3]

			rows.append( ( exid, event_id, user_rabid, source_rabid, status) )
			
	with open(dataDir + 'wrapped_hrv_exids.csv', 'wb') as f:
		writer = csv.writer(f)
		writer.writerows(rows)

if __name__ == '__main__':
	main()