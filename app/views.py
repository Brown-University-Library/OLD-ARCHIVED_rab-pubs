from flask import render_template

from app import app
from app.models import Users, HarvestExids, HarvestProcesses, HarvestSources

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
	# procs = HarvestProcesses.query.filter_by(user_rabid=user.rabid).all()
	exids = HarvestExids.query.filter_by(user_rabid=user.rabid).all()
	return render_template('pending.html',
							user=user,
							exids=exids)	