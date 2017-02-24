from utils import namespaces, prefixes


def RABFactory(rdfType, uri=None, local_name=None, id=None):
	for cls in RABObject.__subclasses__():
		if cls.checkRdfType(rdfType):
			return cls(uri=uri, local_name=local_name, id=id)


class RABObject(object):

	rdf_type = None

	def __init__(self, uri=None, local_name=None, id=None):
		self.uri_ns = namespaces.RABID
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


class PubMed(RABObject):

	rdf_type = [ 	namespaces.BHARVEST + "HarvestSource",
					namespaces.BHARVEST + "PubMed" ]

	def __init__(self, uri=None, local_name=None, id=None):
		self.prefix = prefixes.BHARVEST
		super(PubMed, self).__init__(uri=uri, local_name=local_name, id=id)


class WebOfScience(RABObject):

	rdf_type = [ 	namespaces.BHARVEST + "HarvestSource",
					namespaces.BHARVEST + "WebOfScience" ]

	def __init__(self, uri=None, local_name=None, id=None):
		self.prefix = prefixes.BHARVEST
		super(WebOfScience, self).__init__(uri=uri, local_name=local_name, id=id)