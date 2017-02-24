from app import db


class Users(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	rabid = db.Column(db.String(255))
	short_id = db.Column(db.String(20))

class Citations(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	rabid = db.Column(db.String(255))
	user_rabid = db.Column(db.String, db.ForeignKey('users.rabid'))
	display_string = db.Column(db.String)
	style_rabid = db.Column(db.String, db.ForeignKey('citation_styles.rabid'))
	featured = db.Column(db.Boolean)
	rank = db.Column(db.Integer)

class CitationExids(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	citation_rabid = db.Column(db.String, db.ForeignKey('citations.rabid'))
	exid = db.Column(db.String)
	domain = db.Column(db.String)

class CitationStyles(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	rabid = db.Column(db.String(255))
	template = db.Column(db.String)

class HarvestExids(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	exid = db.Column(db.String)
	event_id = db.Column(db.Integer, db.ForeignKey('harvest_events.id'))
	user_rabid = db.Column(db.String, db.ForeignKey('users.rabid'))
	source_rabid = db.Column(db.String, db.ForeignKey('harvest_sources.rabid'))
	status = db.Column(db.String)

class HarvestEvents(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	proc_rabid = db.Column(db.String, db.ForeignKey('harvest_processes.rabid'))
	event_date = db.Column(db.DateTime)
	user_initiated = db.Column(db.Boolean)
	exids = db.relationship('HarvestExids',
									backref='event', 
									lazy='dynamic')

class HarvestProcesses(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	rabid = db.Column(db.String(255))
	user_rabid = db.Column(db.String, db.ForeignKey('users.rabid'))
	source_rabid = db.Column(db.String, db.ForeignKey('harvest_sources.rabid'))
	process_data = db.Column(db.String)
	status = db.Column(db.String)
	events = db.relationship('HarvestEvents',
									backref='process', 
									lazy='dynamic')

class HarvestSources(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	rabid = db.Column(db.String(255))
	name = db.Column(db.String(255))
	params = db.Column(db.PickleType)
	processes = db.relationship('HarvestProcesses',
									backref='source', 
									lazy='dynamic')