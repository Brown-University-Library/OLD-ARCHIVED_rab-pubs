import utils
import lookup
import harvest

def RABFactory(rdfType, uri=None, local_name=None, id=None):
	for cls in RABObject.__subclasses__():
		if cls.checkRdfType(rdfType):
			return cls(uri=uri, local_name=local_name, id=id)


class RABObject(object):

	rdf_type = None

	def __init__(self, uri=None, local_name=None, id=None):
		self.uri_ns = utils.namespaces.RABID
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

	@classmethod
	def checkRdfType(cls, rdfType):
		if rdfType in cls.rdf_type:
			return True


class HarvestSource(RABObject):

	rdf_type = [ utils.namespaces.BHARVEST + "HarvestSource" ]

	def __init__(self, uri=None, local_name=None, id=None):
		self.prefix = utils.prefixes.BHARVEST
		super(HarvestSource, self).__init__(uri=uri, local_name=local_name, id=id)

	def exid_lookup(exidList):
		pass

class AcademicAnalytics(HarvestSource):

	rdf_type = [ 	utils.namespaces.BHARVEST + "HarvestSource",
					utils.namespaces.BHARVEST + "AcademicAnalytics" ]

	def __init__(self, uri=None, local_name=None, id=None):
		super(AcademicAnalytics, self).__init__(uri=uri, local_name=local_name, id=id)


	def exid_lookup(exidList):
		return lookup.dois.get_details(exidList)

class PubMed(HarvestSource):

	rdf_type = [ 	utils.namespaces.BHARVEST + "HarvestSource",
					utils.namespaces.BHARVEST + "PubMed" ]

	def __init__(self, uri=None, local_name=None, id=None):
		super(PubMed, self).__init__(uri=uri, local_name=local_name, id=id)


	def exid_lookup(exidList):
		return lookup.pmids.get_details(exidList)


wos_session = utils.wos.Session()
wos_session.authenticate()

class WebOfScience(RABObject):

	rdf_type = [ 	utils.namespaces.BHARVEST + "HarvestSource",
					utils.namespaces.BHARVEST + "WebOfScience" ]

	def __init__(self, uri=None, local_name=None, id=None):
		super(WebOfScience, self).__init__(uri=uri, local_name=local_name, id=id)

	def exid_lookup(exidList):
		sid = wos_session.get_sid()
		return lookup.wosids.get_details(exidList, sid)