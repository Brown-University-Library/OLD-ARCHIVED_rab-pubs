import os
import datetime
import requests

from flask import request, render_template, jsonify
from app import app, db
from app.models import local, rab
# from app.harvest import pubmed
# from app.lookup import dois, pmids, wosids
# from app.utils import wos, namespaces

rest_base = app.config['REST_BASE']
app_base = app.config['APP_BASE']
hrv_base = os.path.join(rest_base, 'harvest')

# wos_session = wos.Session()
# wos_session.authenticate()


@app.route('/<short_id>/pending')
def pending(short_id):
	user = local.Users.query.filter_by(short_id=short_id).first()
	sources = local.HarvestSources.query.all()
	exids = local.HarvestExids.query.filter_by(
				user_rabid=user.rabid, status='p').all()
	exids_by_source = { source.rabid: []  for source in sources }
	for exid in exids:
		exids_by_source[ exid.event.process.source_rabid ].append(exid.exid)
	exid_counts_by_source = { namespaces.RABID(source.rabid).local_name: {
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
	src_rabid = namespaces.RABID + source_id
	src = local.HarvestSources.query.filter_by(rabid=src_rabid).first()
	rab_src = rab.RABFactory(src.rdf_type, uri=src.rabid)
	user = Users.query.filter_by(short_id=short_id).first()
	exids = HarvestExids.query.filter_by(
				user_rabid=user.rabid,
				source_rabid=src_rabid,
				status='p').all()
	lookups = rab_src.lookup_exids([ exid.exid for exid in exids ])
	return jsonify([ lookup.json() for lookup in lookups ])

@app.route('/<short_id>/harvest/<source>', methods=['GET'])
def list_harvest_processes(short_id, source):
	src_rabid = namespaces.RABID(source).uri
	src = HarvestSources.query.filter_by(rabid=src_rabid).first()
	user = Users.query.filter_by(short_id=short_id).first()
	if src.name == 'Web of Science':
		rabdata_api = os.path.join(hrv_base,'wos/')	
	elif src.name == 'PubMed':
		rabdata_api = os.path.join(hrv_base,'pubmed/')
	elif src.name == 'Academic Analytics':
		return jsonify({ 'params': [],'queries': [] })
	else:
		raise ValueError("Unrecognized source")
	payload = { 'user' : user.rabid }
	index_resp = requests.get( rabdata_api, params=payload )
	if index_resp.status_code == 200:
		data = index_resp.json()
		queries = []
		for d in data:
			query_rabid = d.keys()[0]
			query_id = namespaces.RABID(query_rabid).id
			retr_resp = requests.get( rabdata_api + query_id )
			if retr_resp.status_code == 200:
				retr_data = retr_resp.json()
				try:
					query_data = retr_data[ query_rabid ]
				except KeyError:
					raise
				del query_data['user']
				del query_data['class']
				query_data['rabid'] = namespaces.RABID(query_rabid).local_name
				queries.append(query_data)
			else:
				continue
	else:
		return 400
	return jsonify(
		{ 'params': src.params,'queries': queries })

@app.route('/<short_id>/harvest/<source>', methods=['POST'])
def create_harvest_process(short_id, source):
	src_rabid = namespaces.RABID(source).uri
	src = HarvestSources.query.filter_by(rabid=src_rabid).first()
	user = Users.query.filter_by(short_id=short_id).first()
	data = request.get_json()
	for k, v in data.items():
		if isinstance(v, unicode):
			data[k] = [ v ]
	for k in src.params.keys():
		if k not in data:
			data[k] = []
	data['user'] = [ user.rabid ]
	data['class']= [ namespaces.BHARVEST('HarvestProcess').uri ]
	if src.name == 'Web of Science':
		data['class'].append( namespaces.BHARVEST('WebOfScienceSearch').uri )
		rabdata_api = os.path.join(hrv_base,'wos/')	
	elif src.name == 'PubMed':
		data['class'].append( namespaces.BHARVEST('bharvest-PubMedSearch').uri )
		rabdata_api = os.path.join(hrv_base,'pubmed/')
	else:
		raise ValueError("Unrecognized source")
	resp = requests.post(rabdata_api, json=data)
	if resp.status_code == 200:
		new_proc_rabid = resp.json().keys()[0]
		new_proc = HarvestProcesses()
		new_proc.rabid = new_proc_rabid
		new_proc.user_rabid = user.rabid
		new_proc.source_rabid = src.rabid
		new_proc.status = "a"
		new_proc.process_data = resp.json()[new_proc_rabid]['label'][0]
		db.session.add(new_proc)
		db.session.commit()
		return jsonify(resp.json())
	else:
		return jsonify({"BAD!!!": resp.text})

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
