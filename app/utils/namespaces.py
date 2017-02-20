class NameSpace(object):

	def __init__(self, strData):
		if strData.startswith(self.uri_ns):
			self.uri = strData
			self.id = strData[len(self.uri_ns):]
			self.local_name = self.prefix + self.id
		elif strData.startswith(self.prefix):
			self.local_name = strData
			self.id = strData[len(self.prefix):]
			self.uri = self.uri_ns + self.id
		elif all(c not in strData for c in '/-:'):
			self.id = strData
			self.uri = self.uri_ns + self.id
			self.local_name = self.prefix + self.id
		else:
			raise ValueError('Unrecognized URI or namespace')


class RABID(NameSpace):

	def __init__(self, strData):
		self.uri_ns = "http://vivo.brown.edu/individual/"
		self.prefix = "rabid-"
		super(RABID, self).__init__(strData)


class BHARVEST(NameSpace):

	def __init__(self, strData):
		self.uri_ns = "http://vivo.brown.edu/ontology/harvest#"
		self.prefix = "bharvest-"
		super(BHARVEST, self).__init__(strData)