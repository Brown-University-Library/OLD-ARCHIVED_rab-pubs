import os
import datetime
import requests

from flask import request, render_template, jsonify
from app import app, db
from app.models import local, rab
# from app.harvest import pubmed
# from app.lookup import dois, pmids, wosids
from app.utils import wos, namespaces

app_base = app.config['APP_BASE']

# wos_session = wos.Session()
# wos_session.authenticate()


@app.route('/<short_id>/pending')
def pending(short_id):
	user = local.Users.query.filter_by(short_id=short_id).first()
	sources = [ rab.HarvestSourceFactory(src.display, uri=src.rabid) 
					for src in local.HarvestSources.query.all() ]
	exids = local.HarvestExids.query.filter_by(
				user_rabid=user.rabid, status='p').all()
	exids_by_source = { source.uri: []  for source in sources }
	for exid in exids:
		exids_by_source[ exid.event.process.source_rabid ].append(exid.exid)
	exid_counts_by_source = { source.local_name: {
								'name': source.label,
								'count': len(exids_by_source[source.uri])
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
	src_rabid = namespaces.RABID + source_id
	src = local.HarvestSources.query.filter_by(rabid=src_rabid).first()
	rab_src = rab.HarvestSourceFactory(src.display, uri=src.rabid)
	user = Users.query.filter_by(short_id=short_id).first()
	exids = HarvestExids.query.filter_by(
				user_rabid=user.rabid,
				source_rabid=src_rabid,
				status='p').all()
	lookups = rab_src.lookup_exids([ exid.exid for exid in exids ])
	return jsonify([ lookup.json() for lookup in lookups ])

@app.route('/<short_id>/harvest/<source_id>', methods=['GET'])
def list_harvest_processes(short_id, source_id):
	src_rabid = namespaces.RABID + source_id
	src = HarvestSources.query.filter_by(rabid=src_rabid).first()
	rab_src = rab.HarvestSourceFactory(src.display, uri=src.rabid)
	user = Users.query.filter_by(short_id=short_id).first()
	procs = HarvestProcesses.query.filter_by(source_rabid=src_rabid, user_rabid=user.rabid)
	return jsonify([ { proc.rabid: proc.display } for proc in procs ])

@app.route('/<short_id>/harvest/<source_id>', methods=['POST'])
def create_harvest_process(short_id, source_id):
	src_rabid = namespaces.RABID(source).uri
	src = HarvestSources.query.filter_by(rabid=src_rabid).first()
	user = Users.query.filter_by(short_id=short_id).first()
	data = request.get_json()
	proc = rab.HarvestProcessFactory(  )

@app.route('/<short_id>/harvest/<source>/<proc_id>', methods=['GET'])
def get_harvest_process(short_id, source, proc_id):
	proc_id = namespaces.RABID(proc_id).id
	src_rabid = namespaces.RABID(source).uri
	src = HarvestSources.query.filter_by(rabid=src_rabid).first()
	if src.name == 'Web of Science':
		rabdata_api = os.path.join(hrv_base,'wos/')	
	elif src.name == 'PubMed':
		rabdata_api = os.path.join(hrv_base,'pubmed/')
	else:
		raise ValueError("Unrecognized source")
	resp = requests.get( rabdata_api + proc_id )
	if resp.status_code == 200:
		rab_obj = resp.json()
		rabid = rab_obj.keys()[0]
		data = rab_obj[rabid]
		del data['class']
		del data['user']
		data['rabid'] = namespaces.RABID(rabid).local_name
		return jsonify(data)
	else:
		return 400

@app.route('/<short_id>/harvest/<proc_id>', methods=['PUT'])
def update_harvest_process(short_id, proc_id):
	pass

@app.route('/<short_id>/harvest/<proc_id>', methods=['DELETE'])
def delete_harvest_process(short_id, proc_id):
	pass

@app.route('/<short_id>/harvest/<proc_id>/pubmed')
def run_pubmed_harvest(short_id, proc_id):
	rabid = namespaces.RABID(proc_id)
	user = Users.query.filter_by(short_id=short_id).first()
	proc = HarvestProcesses.query.filter_by(rabid=rabid).first()
