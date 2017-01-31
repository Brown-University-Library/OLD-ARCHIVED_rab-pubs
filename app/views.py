import datetime

from flask import render_template, jsonify
from app import app, db
from app.models import Users, HarvestExids, HarvestProcesses, HarvestSources

from app.harvest import pubmed
from app.lookup import dois, pmids, wosids
from app.utils import wos, namespaces

wos_session = wos.Session()
wos_session.authenticate()

harvest_params = {
	'rabid:1b404f6f24b449688bed96f0b2587d4d'	: pubmed.params
}

@app.route('/rabpubs/<short_id>/pending')
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
	return render_template('harvest.html',
							user=user,
							counts=exid_counts_by_source)

@app.route('/rabpubs/<short_id>/pending/<source_id>')
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

@app.route('/rabpubs/<short_id>/harvest/<source>', methods=['GET'])
def list_harvest_processes(short_id, source):
	src_rabid = namespaces.rabid(source)
	params = harvest_params[source]
	user = Users.query.filter_by(short_id=short_id).first()
	procs = HarvestProcesses.query.filter_by(
				user_rabid=user.rabid, source_rabid=src_rabid).all()
	queries = [ proc.process_data for proc in procs ]
	return jsonify({ 'new': params, 'existing': queries })

@app.route('/rabpubs/<short_id>/harvest/', methods=['POST'])
def create_harvest_process(short_id):
	user = Users.query.filter_by(short_id=short_id).first()
	data = request.get_json()
	new_proc = HarvestProcesses(
				user_rabid=user.rabid,
				source_rabid="http://vivo.brown.edu/individual/1b404f6f24b449688bed96f0b2587d4d",
				status="a",
				process_data=json.dumps(data)
				)
	db.session.add(new_proc)
	db.session.commit()
	return jsonify({'id': new_proc.id})

@app.route('/rabpubs/<short_id>/harvest/<proc_id>', methods=['GET'])
def get_harvest_process(short_id, proc_id):
	rabid = namespaces.rabid(proc_id)
	user = Users.query.filter_by(short_id=short_id).first()
	proc = HarvestProcesses.query.filter_by(rabid=rabid).first()

@app.route('/rabpubs/<short_id>/harvest/<proc_id>', methods=['PUT'])
def update_harvest_process(short_id, proc_id):
	pass

@app.route('/rabpubs/<short_id>/harvest/<proc_id>', methods=['DELETE'])
def delete_harvest_process(short_id, proc_id):
	pass

@app.route('/rabpubs/<short_id>/harvest/<proc_id>/pubmed')
def run_pubmed_harvest(short_id, proc_id):
	rabid = namespaces.rabid(proc_id)
	user = Users.query.filter_by(short_id=short_id).first()
	proc = HarvestProcesses.query.filter_by(rabid=rabid).first()