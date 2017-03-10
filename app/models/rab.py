import os
import requests

from app import app, db
from app.utils import namespaces, prefixes, wos
from app.lookup import dois, pmids, wosids
from app.models import local

rest_base = app.config['REST_BASE']
harvest_base = os.path.join(rest_base, 'harvest')


class RABObject(object):

	rdf_type = None

	def __init__(self, uri=None, id=None):
		self.uri_ns = namespaces.RABID
		self.existing = True
		self.prefix = None
		self.label = None
		self.etag = None
		if id and uri:
			self.id = id
			self.uri = uri
		elif uri and not id:
			self.uri = uri
			self.id = uri[len(self.uri_ns):]
		elif id and not uri:
			self.id = id
			self.uri = self.uri_ns + id
		else:
			self.existing = False

	def publish(self):
		return dict(id=self.id, rabid=self.uri, display=self.label, data=self.data)

	def retrieve(self):
		if self.existing:
			resp = requests.get(self.rab_api + self.id)
		else:
			return
		if resp.status_code == 200:
			self.etag = resp.headers.get('ETag')
			data = resp.json()
			rab_uri = data.keys()[0]
			assert rab_uri == self.uri
			self.load_data(data)
		else:
			self.data = dict()
			self.existing = False

	def load_data(self, data):
		self.uri = data.keys()[0]
		self.id = self.uri[len(self.uri_ns):]
		attrs = data[self.uri]
		self.label = attrs['label'][0]
		self.data = attrs
		self.existing = True

	@classmethod
	def factory(cls, data):
		uri = data.keys()[0]
		rdfType = data[uri]['class']
		##
		## Currently, RAB-REST does not return subclass data,
		## making this ineffective. Returning subclass data will
		## require Dozer modifications. Revisit if necessary
		# if cls.__subclasses__():
		# 	for klass in cls.__subclasses__():
		# 		if klass.rdf_type == rdfType:
		# 			rab_obj = klass()
		# 			rab_obj.load_data(data)
		# 			return rab_obj
		# else:
		if cls.rdf_type == rdfType:
			rab_obj = cls()
			rab_obj.load_data(data)
			return rab_obj

	@classmethod
	def list(cls, params=None):
		resp = requests.get(cls.rab_api, params=params)
		if resp.status_code == 200:
			idx = [] 
			for data in resp.json():
				new_rab = cls.factory(data)
				idx.append(new_rab)
			return idx
		else:
			raise

wos_session = wos.Session()
wos_session.authenticate()

class HarvestSource(RABObject):

	rdf_type = [ namespaces.BHARVEST + "Source" ]
	rab_api = os.path.join(harvest_base, 'sources/')

	def __init__(self, uri=None, id=None):
		self.prefix = prefixes.BHARVEST
		self.process_api = os.path.join(harvest_base, 'processes/')
		super(HarvestSource, self).__init__(uri=uri, id=id)

	def exid_lookup(self, exidList):
		if self.label == 'Academic Analytics':
			return dois.get_details(exidList)
		elif self.label == 'PubMed':
			return pmids.get_details(exidList)
		elif self.label == 'Web of Science':
			sid = wos_session.get_sid()
			return wosids.get_details(exidList, sid)

	def list_processes(self, user_rabid):
		if self.label == 'Academic Analytics':
			return jsonify({ 'params': [],'queries': [] })
		else:
			payload = { 'user' : user_rabid, 'source' : self.uri }
			index_resp = requests.get( self.process_api, params=payload )
			if index_resp.status_code == 200:
				data = index_resp.json()
				queries = []
				for d in data:
					proc = d.keys()[0]
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
	

class HarvestProcess(RABObject):

	rdf_type = [ namespaces.BHARVEST + "HarvestProcess" ]
	rab_api = os.path.join(harvest_base, 'processes/')

	def __init__(self, uri=None, id=None):
		self.prefix = prefixes.BHARVEST
		self.params = None
		super(HarvestProcess, self).__init__(uri=uri, id=id)

	def create(self, user_rabid=None, src_rabid=None, data=None):
		for k, v in data.items():
			if isinstance(v, unicode):
				data[k] = [ v ]
		for k in src.params.keys():
			if k not in data:
				data[k] = []
		data['user'] = [ user_rabid ]
		data['class']= self.rdf_type
		resp = requests.post(rabdata_api, json=data)
		if resp.status_code == 200:
			new_proc_rabid = resp.json().keys()[0]
			new_proc = local.HarvestProcesses()
			new_proc.rabid = new_proc_rabid
			new_proc.user_rabid = user_rabid
			new_proc.source_rabid = src_rabid
			new_proc.status = "a"
			new_proc.process_data = resp.json()[new_proc_rabid]['label'][0]
			db.session.add(new_proc)
			db.session.commit()
			return jsonify(resp.json())
		else:
			return jsonify({"BAD!!!": resp.text})

	def get(self):
		resp = requests.get( self.rab_api + self.id )
		if resp.status_code == 200:
			rab_obj = resp.json()
			rabid = rab_obj.keys()[0]
			assert rabid == self.uri
			self.data = rab_obj[self.uri]
		else:
			self.data = dict()

	def publish(self):
		display = self.data.get('label', '')
		return dict(id=self.id, rabid=self.uri, params=self.params, display=display, data=self.data)

class WebOfScienceSearch(HarvestProcess):

	rdf_type = [	namespaces.BHARVEST + "HarvestProcess",
					namespaces.BHARVEST + "WebOfScienceSearch" ]

	def __init__(self, uri=None, id=None):
		self.params = 	[	'Topic','Title','Author','Author Identifiers',
							'Group Author','Editor','Publication Name',
							'DOI','Year Published','Address',
							'Organizations-Enhanced','Conference',
							'Language','Document Type','Funding Agency',
							'Grant Number','Accession Number','PubMed ID']
		super(WebOfScienceSearch, self).__init__(uri=uri, id=id)

class PubMedSearch(HarvestProcess):

	rdf_type = [	namespaces.BHARVEST + "HarvestProcess",
					namespaces.BHARVEST + "PubMedSearch" ]
	def __init__(self, uri=None, id=None):
		self.params = [	'Title/Abstract','Author - Last','ISBN',
						'MeSH Terms','Affiliation','Author - Full',
						'Date - MeSH','Location ID','Publication Type',
						'Subject - Personal Name','All Fields',
						'Author - First','Date - Entrez','Title',
						'Journal','Transliterated Title',
						'Investigator - Full','Supplementary Concept',
						'Book','Editor','Issue','EC/RN Number',
						'Text Word','Other Term','Grant Number',
						'Date - Completion','Volume','MeSH Major Topic',
						'Date - Modification','Date - Publication',
						'Publisher','Pagination','MeSH Subheading',
						'Language','Investigator','Secondary Source ID',
						'Pharmacological Action','Filter',
						'Date - Create','Author - Identifier',
						'Author - Corporate']
		super(PubMedSearch, self).__init__(uri=uri, id=id)

class AcademicAnalyticsUpload(HarvestProcess):

	rdf_type = [	namespaces.BHARVEST + "HarvestProcess",
			namespaces.BHARVEST + "AcademicAnalyticsUpload" ]

	def __init__(self, uri=None, id=None):
		self.params = []
		super(AcademicAnalyticsUpload, self).__init__(uri=uri, id=id)

