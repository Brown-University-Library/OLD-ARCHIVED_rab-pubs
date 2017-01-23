import datetime
import json

from flask import render_template
from app import app
from app.models import Users, HarvestExids, HarvestProcesses, HarvestSources

from app.lookup import dois, pmids, wosids
from app.utils import wos

wos_session = wos.Session()
wos_session.authenticate()


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

@app.route('/rabpubs/<short_id>/pending/academic_analytics')
def get_pending_academic_analytics(short_id):
	src_rabid = "http://vivo.brown.edu/individual/c53746b63fe848bbac0a1ac0bf559b27"
	user = Users.query.filter_by(short_id=short_id).first()
	exids = HarvestExids.query.filter_by(
				user_rabid=user.rabid,
				source_rabid=src_rabid,
				status='p').all()
	lookups = dois.get_details([ exid.exid for exid in exids])
	display = [ lookup.json() for lookup in lookups ]
	return json.dumps(display)

@app.route('/rabpubs/<short_id>/pending/pubmed')
def get_pending_pubmed(short_id):
	src_rabid = "http://vivo.brown.edu/individual/1b404f6f24b449688bed96f0b2587d4d"
	user = Users.query.filter_by(short_id=short_id).first()
	exids = HarvestExids.query.filter_by(
				user_rabid=user.rabid,
				source_rabid=src_rabid,
				status='p').all()
	lookups = pmids.get_details([ exid.exid for exid in exids ])
	display = [ lookup.json() for lookup in lookups ]
	return json.dumps(display)

@app.route('/rabpubs/<short_id>/pending/wos')
def get_pending_wos(short_id):
	src_rabid = "http://vivo.brown.edu/individual/70209659b6af4980b17ef39884160406"
	user = Users.query.filter_by(short_id=short_id).first()
	exids = HarvestExids.query.filter_by(
				user_rabid=user.rabid,
				source_rabid=src_rabid,
				status='p').all()
	sid = wos_session.get_sid()
	lookups = wosids.get_details([ exid.exid for exid in exids ], sid)
	display = [ lookup.json() for lookup in lookups ]
	return json.dumps(display)