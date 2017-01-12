from flask import render_template

from app import app
from app.models import Users, HarvestExids, HarvestProcesses, HarvestSources

import json
import requests

@app.route('/')
@app.route('/rabpubs')
def index():
    user = {'nickname': 'Steve'}  # fake user
    return render_template('base.html',
                           title='Publictaions',
                           user=user)

@app.route('/rabpubs/<short_id>/pending')
def harvested_publications(short_id):
	user = Users.query.filter_by(short_id=short_id).first()
	sources = HarvestSources.query.all()
	exids = HarvestExids.query.filter_by(user_rabid=user.rabid).all()
	source_map = { source.rabid: []  for source in sources }
	for exid in exids:
		source_map[ exid.event.process.source_rabid ].append(exid)
	source_names = { source.name: source_map[source.rabid]
						for source in sources }
	pmids = [ exid.exid for exid in source_names['PubMed'] ]
	esumm_base = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi'
	payload = { 'db': 'pubmed', 'retmode': 'json' }
	payload['id'] = ','.join(pmids)
	resp = requests.post( esumm_base, data=payload )
	data = resp.json()
	pubmed_list = list(source_names['PubMed'])
	for uid in data['result']['uids']:
		meta = data['result'][uid]
		title = meta['title']
		pubdate = meta['pubdate']
		pub = meta['source']
		try:
			article = "{0} {1} {2}".format(title, pub, pubdate)
		except:
			article = "foo"
		for n, i in enumerate(source_names['PubMed']):
			if i.exid == uid:
				pubmed_list[n] = article
	source_names['PubMed'] = pubmed_list
	return render_template('pending.html',
							user=user,
							sources=source_names)	