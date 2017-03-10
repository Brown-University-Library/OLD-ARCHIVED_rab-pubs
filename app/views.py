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
	sources = rab.HarvestSource.list()
	exids = local.HarvestExids.query.filter_by(
						user_rabid=user.rabid, status='p').all()
	exids_by_source = { source.uri: [] for source in sources }
	for exid in exids:
		exids_by_source[ exid.event.process.source_rabid ].append(exid.exid)
	exid_counts_by_source = { source.id: {	'id': source.id,
						'name': source.label,
						'count': len(exids_by_source[source.uri])
						} for source in sources }
	config_map = {
		'app_base': app_base,
		'short_id': short_id
		}
	return render_template('harvest.html',
				user=user,
				counts=exid_counts_by_source,
				config=config_map)

@app.route('/<short_id>/pending/<source_id>')
def lookup_pending(short_id, source_id):
	src = rab.HarvestSource(id=source_id)
	src.retrieve()
	user = local.Users.query.filter_by(short_id=short_id).first()
	exids = local.HarvestExids.query.filter_by(
				user_rabid=user.rabid,
				source_rabid=src.uri,
				status='p').all()
	lookups = src.exid_lookup([ exid.exid for exid in exids ])
	return jsonify([ lookup.json() for lookup in lookups ])

@app.route('/<short_id>/harvest/<source_id>', methods=['GET'])
def list_harvest_processes(short_id, source_id):
	src = rab.HarvestSource(id=source_id)
	src.retrieve()
	user = local.Users.query.filter_by(short_id=short_id).first()
	procs = rab.HarvestProcess.list({'source': src.uri, 'user': user.rabid})
	for proc in procs:
		proc.retrieve()
	return jsonify([ proc.publish() for proc in procs ])

@app.route('/<short_id>/harvest/<source_id>', methods=['POST'])
def create_harvest_process(short_id, source_id):
	src_rabid = namespaces.RABID(source).uri
	src = HarvestSources.query.filter_by(rabid=src_rabid).first()
	user = Users.query.filter_by(short_id=short_id).first()
	data = request.get_json()
	proc = rab.HarvestProcessFactory(  )

@app.route('/<short_id>/harvest/<proc_id>', methods=['GET'])
def get_harvest_process(short_id, proc_id):
	proc = rab.HarvestProcessFactory(id=proc_id)
	proc.get()
	return jsonify(proc.publish())

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
