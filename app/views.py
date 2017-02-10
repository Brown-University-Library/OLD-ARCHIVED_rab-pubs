import os
import datetime
import requests

from flask import render_template, jsonify
from app import app, db
from app.models import Users, HarvestExids, HarvestProcesses, HarvestSources

from app.harvest import pubmed
from app.lookup import dois, pmids, wosids
from app.utils import wos, namespaces

rest_base = app.config['REST_BASE']
app_base = app.config['APP_BASE']
hrv_base = os.path.join(rest_base, 'harvest')

wos_session = wos.Session()
wos_session.authenticate()


@app.route('/<short_id>/pending')
def pending(short_id):
	user = Users.query.filter_by(short_id=short_id).first()
	sources = HarvestSources.query.all()
	exids = HarvestExids.query.filter_by(user_rabid=user.rabid, status='p').all()
	exids_by_source = { source.rabid: []  for source in sources }
	for exid in exids:
		exids_by_source[ exid.event.process.source_rabid ].append(exid.exid)
	exid_counts_by_source = { namespaces.rabid(source.rabid): {
								'name': source.name,
								'count': len(exids_by_source[source.rabid])
								} for source in sources }
	config_map = {
		'app_base' : app_base,
		'short_id'	: short_id
		}
	return render_template('harvest.html',
							user=user,
							counts=exid_counts_by_source,
							config=config_map)

@app.route('/<short_id>/pending/<source_id>')
def lookup_pending(short_id, source_id):
	src_names = {
		'http://vivo.brown.edu/individual/70209659b6af4980b17ef39884160406': 'wos',
		'http://vivo.brown.edu/individual/c53746b63fe848bbac0a1ac0bf559b27': 'aa',
		'http://vivo.brown.edu/individual/1b404f6f24b449688bed96f0b2587d4d': 'pubmed'
	}
	src_rabid = namespaces.rabid(source_id)
	user = Users.query.filter_by(short_id=short_id).first()
	exids = HarvestExids.query.filter_by(
				user_rabid=user.rabid,
				source_rabid=src_rabid,
				status='p').all()
	if src_names[src_rabid] == 'wos':
		sid = wos_session.get_sid()
		lookups = wosids.get_details([ exid.exid for exid in exids ], sid)	
	elif src_names[src_rabid] == 'aa':
		lookups = dois.get_details([ exid.exid for exid in exids])
	elif src_names[src_rabid] == 'pubmed':
		lookups = pmids.get_details([ exid.exid for exid in exids ])
	else:
		raise ValueError("Unrecognized source")
	return jsonify([ lookup.json() for lookup in lookups ])

@app.route('/<short_id>/queries/<source>', methods=['GET'])
def list_harvest_processes(short_id, source):
	harvest_params = {
		'http://vivo.brown.edu/individual/70209659b6af4980b17ef39884160406': ['shoe'],
		'http://vivo.brown.edu/individual/c53746b63fe848bbac0a1ac0bf559b27': ['foo'],
		'http://vivo.brown.edu/individual/1b404f6f24b449688bed96f0b2587d4d'	: pubmed.params
	}
	src_rabid = namespaces.rabid(source)
	params = harvest_params[src_rabid]
	user = Users.query.filter_by(short_id=short_id).first()
	procs = HarvestProcesses.query.filter_by(
				user_rabid=user.rabid, source_rabid=src_rabid).all()
	queries = [ {'display': proc.process_data} for proc in procs ]
	return jsonify({ 'params': params, 'queries': queries })

@app.route('/<short_id>/harvest/', methods=['POST'])
def create_harvest_process(short_id):
	user = Users.query.filter_by(short_id=short_id).first()
	data = request.get_json()
	data['user'] = user.rabid
	data['class'] = 'http://vivo.brown.edu/ontology/harvest#HarvestProcess'
	resp = requests.post(hrv_base, json=data)
	if resp.status_code == 200:
		new_proc = HarvestProcesses(
			user_rabid=user.rabid,
			source_rabid="http://vivo.brown.edu/individual/1b404f6f24b449688bed96f0b2587d4d",
			status="a",
			process_data=json.dumps(data)
			)
		db.session.add(new_proc)
		db.session.commit()
		return jsonify({'id': new_proc.id})
	else:
		return jsonify({"BAD!!!": resp.body})

@app.route('/<short_id>/harvest/<proc_id>', methods=['GET'])
def get_harvest_process(short_id, proc_id):
	rabid = namespaces.rabid(proc_id)
	user = Users.query.filter_by(short_id=short_id).first()
	proc = HarvestProcesses.query.filter_by(rabid=rabid).first()

@app.route('/<short_id>/harvest/<proc_id>', methods=['PUT'])
def update_harvest_process(short_id, proc_id):
	pass

@app.route('/<short_id>/harvest/<proc_id>', methods=['DELETE'])
def delete_harvest_process(short_id, proc_id):
	pass

@app.route('/<short_id>/harvest/<proc_id>/pubmed')
def run_pubmed_harvest(short_id, proc_id):
	rabid = namespaces.rabid(proc_id)
	user = Users.query.filter_by(short_id=short_id).first()
	proc = HarvestProcesses.query.filter_by(rabid=rabid).first()
