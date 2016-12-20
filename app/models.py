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

class CitationStyles(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	rabid = db.Column(db.String(255))
	template = db.Column(db.String)

class HarvestRecords(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	user_rabid = db.Column(db.String, db.ForeignKey('users.rabid'))
	title = db.Column(db.String(255))
	venue = db.Column(db.String)
	date = db.Column(db.String)
	status = db.Column(db.String)

class HarvestRecordExids(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	record_id = db.Column(db.String, db.ForeignKey('harvest_records.id'))
	exid = db.Column(db.String)
	domain = db.Column(db.String) 

class HarvestQueries(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	rabid = db.Column(db.String(255))
	user_rabid = db.Column(db.String, db.ForeignKey('users.rabid'))
	query_string = db.Column(db.String) 