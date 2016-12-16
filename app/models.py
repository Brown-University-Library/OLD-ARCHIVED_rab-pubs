from app import db


class User(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	rabid = db.Column(db.String(255))
	short_id = db.Column(db.String(20))

class Citation(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	rabid = db.Column(db.String(255))
	user_rabid = db.Column(db.String, db.ForeignKey('users.rabid'))
	display_string = db.Column(db.String)
	style_rabid = db.Column(db.String, db.ForeignKey('citation_styles.rabid'))
	featured = db.Column(db.Boolean)
	rank = db.Column(db.Integer)

class CitationStyle(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	rabid = db.Column(db.String(255))
	template = db.Column(db.String)

class HarvestRecord(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	user_rabid = db.Column(db.String, db.ForeignKey('users.rabid'))
	title = db.Column(db.String(255))
	date = db.Column(db.String)
	status = db.Column(db.String, db.ForeignKey('harvest_status.id'))

class HarvestStatus(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	status = db.Column(db.String)

class HarvestRecordExid(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	record_id = db.Column(db.String, db.ForeignKey('harvest_records.id'))
	exid = db.Column(db.String)
	domain = db.Column(db.String) 

class HarvestQuery(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	rabid = db.Column(db.String(255))
	user_rabid = db.Column(db.String, db.ForeignKey('users.rabid'))
	query_string = db.Column(db.String) 