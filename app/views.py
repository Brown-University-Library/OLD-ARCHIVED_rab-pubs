import datetime

from flask import render_template
from app import app
from app.models import Users, HarvestExids, HarvestProcesses, HarvestSources

from app.lookup import dois, pmids, wosids
from app.utils import wos

wos_session = wos.Session()
# wos_session.authenticate()


@app.route('/rabpubs/<short_id>/pending')
def pending(short_id):
	user = Users.query.filter_by(short_id=short_id).first()
	sources = HarvestSources.query.all()
	exids = HarvestExids.query.filter_by(user_rabid=user.rabid, status='p').all()
	exids_by_source = { source.rabid: []  for source in sources }
	for exid in exids:
		exids_by_source[ exid.event.process.source_rabid ].append(exid.exid)
	exid_counts_by_source = { source.rabid[33:]: {
								'name': source.name,
								'count': len(exids_by_source[source.rabid])
								} for source in sources }
	return render_template('pending.html',
							user=user,
							counts=exid_counts_by_source)

@app.route('/rabpubs/<short_id>/pending_meta')
def get_pending_metadata(short_id):
	out = {}
	for source in sources:
		if source.name == 'PubMed' and len(source_map[source.rabid]) != 0:
			out['Pubmed'] = pmids.get_details(source_map[source.rabid])
		if source.name == 'Academic Analytics' and len(source_map[source.rabid]) != 0:
			out['Academic Analytics'] = dois.get_details(source_map[source.rabid])
		if source.name == 'Web of Science' and len(source_map[source.rabid]) != 0:
			sid = wos_session.get_sid()
			print sid
			out['Web of Science'] = wosids.get_details(source_map[source.rabid], sid)
	return render_template('pending.html',
							user=user,
							sources=out)	