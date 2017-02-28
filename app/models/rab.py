import os

from app import app, db
from app.utils import namespaces, prefixes, wos
from app.lookup import dois, pmids, wosids
from app.models import local

rest_base = app.config['REST_BASE']
harvest_base = os.path.join(rest_base, 'harvest')



def RABFactory(rdfType, uri=None, local_name=None, id=None):
	for cls in RABObject.__subclasses__():
		if cls.checkRdfType(rdfType):
			return cls(uri=uri, local_name=local_name, id=id)

class RABObject(object):

	rdf_type = None

	def __init__(self, uri=None, local_name=None, id=None, display=None, data=None):
		self.uri_ns = namespaces.RABID
		self.display = display
		self.data = data
		if uri:
			self.uri = uri
			self.id = uri[len(self.uri_ns):]
			self.local_name = self.prefix + self.id
		elif local_name:
			self.local_name = local_name
			self.id = local_name[len(self.prefix):]
			self.uri = self.uri_ns + self.id
		elif id:
			self.id = id
			self.uri = self.uri_ns + id
			self.local_name = self.prefix + id

	def publish(self):
		return dict(id=self.id, rabid=self.uri, ns=self.local_name,
						display=self.display, data=self.data)

	@classmethod
	def checkRdfType(cls, rdfType):
		if rdfType in cls.rdf_type:
			return True

	@classmethod
	def checkLabel(cls, label):
		if label == cls.label:
			return True


def HarvestSourceFactory(label, uri=None, local_name=None, id=None):
	for cls in HarvestSource.__subclasses__():
		if cls.checkLabel(label):
			return cls(uri=uri, local_name=local_name, id=id)

class HarvestSource(RABObject):

	rdf_type = [ namespaces.BHARVEST + "HarvestSource" ]
	label = None

	def __init__(self, uri=None, local_name=None, id=None):
		self.prefix = prefixes.BHARVEST
		self.sources_api = os.path.join(harvest_base, 'sources/')
		self.process_api = os.path.join(harvest_base, 'processes/')
		super(HarvestSource, self).__init__(uri=uri, local_name=local_name, id=id)

	def exid_lookup(self, exidList):
		pass

	def list_processes(self, user_rabid):
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


class AcademicAnalytics(HarvestSource):

	label = "Academic Analytics"

	def __init__(self, uri=None, local_name=None, id=None):
		super(AcademicAnalytics, self).__init__(uri=uri, local_name=local_name, id=id)


	def exid_lookup(self, exidList):
		return dois.get_details(exidList)

	def list_processes(self, user_rabid):
		return jsonify({ 'params': [],'queries': [] })

class PubMed(HarvestSource):

	label = "PubMed"

	def __init__(self, uri=None, local_name=None, id=None):
		super(PubMed, self).__init__(uri=uri, local_name=local_name, id=id)


	def exid_lookup(self, exidList):
		return pmids.get_details(exidList)


wos_session = wos.Session()
wos_session.authenticate()

class WebOfScience(HarvestSource):

	label = "Web of Science"

	def __init__(self, uri=None, local_name=None, id=None):
		super(WebOfScience, self).__init__(uri=uri, local_name=local_name, id=id)

	def exid_lookup(self, exidList):
		sid = wos_session.get_sid()
		return wosids.get_details(exidList, sid)



class HarvestProcess(RABObject):

	rdf_type = [ namespaces.BHARVEST + "HarvestProcess" ]

	def __init__(self, uri=None, local_name=None, id=None):
		self.rab_api = os.path.join(harvest_base, 'processes/')
		super(HarvestProcess, self).__init__(uri=uri, local_name=local_name, id=id)

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
			data = rab_obj[rabid]
			del data['class']
			del data['user']
			data['rabid'] = self.uri
			return jsonify(data)
		else:
			return 400

class WebOfScienceSearch(HarvestProcess):

	rdf_type = [	namespaces.BHARVEST + "HarvestProcess",
					namespaces.BHARVEST + "WebOfScienceSearch" ]

	def __init__(self, uri=None, local_name=None, id=None):
		self.params = 	[	'Topic','Title','Author','Author Identifiers',
							'Group Author','Editor','Publication Name',
							'DOI','Year Published','Address',
							'Organizations-Enhanced','Conference',
							'Language','Document Type','Funding Agency',
							'Grant Number','Accession Number','PubMed ID']
		super(WebOfScienceSearch, self).__init__(uri=uri, local_name=local_name, id=id)

class PubMedSearch(HarvestProcess):

	rdf_type = [	namespaces.BHARVEST + "HarvestProcess",
					namespaces.BHARVEST + "PubMedSearch" ]
	def __init__(self, uri=None, local_name=None, id=None):
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
		super(PubMedSearch, self).__init__(uri=uri, local_name=local_name, id=id)