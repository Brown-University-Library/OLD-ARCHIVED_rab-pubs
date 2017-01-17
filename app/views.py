from flask import render_template
from app import app
from app.models import Users, HarvestExids, HarvestProcesses, HarvestSources

from app.lookup import dois, pmids

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
		source_map[ exid.event.process.source_rabid ].append(exid.exid)
	out = {}
	for source in sources:
		if source.name == 'PubMed' and len(source_map[source.rabid]) != 0:
			out['Pubmed'] = pmids.get_details(source_map[source.rabid])
		if source.name == 'Academic Analytics' and len(source_map[source.rabid]) != 0:
			out['Academic Analytics'] = dois.get_details(source_map[source.rabid])
	return render_template('pending.html',
							user=user,
							sources=out)	