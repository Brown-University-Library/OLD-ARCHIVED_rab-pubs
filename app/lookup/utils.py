
class Lookup(object):
	"""docstring for Lookup"""
	def __init__(self, meta):
		self.exid = None
		self.source = None
		self.display = {
			'short': {
				'title' : '',
				'venue'	: '',
				'date'	: ''
			},
			'details': []
		}
		self.data = {
			'exid' 			: None,
			'source'		: None,
			'type'			: None,
			'title' 		: None,
			'venue_type'	: None,
			'venue_name'	: None,
			'venue_abbrv'	: None,
			'venue_issn'	: None,
			'venue_id'		: None,
			'venue_volume'	: None,
			'venue_issue'	: None,
			'venue_isbn'	: None,
			'chapter'		: None,
			'pages'			: None,
			'date'			: None,
			'year'			: None,
			'authors'		: None,
			'author_list'	: [],
			'keywords'		: None,
			'keyword_list'	: [],
			'doi'			: None,
			'pmid'			: None,
			'wosid'			: None,
			'isbn'			: None
		}
		self.prep_meta(meta)
		self.prep_display()

	def prep_meta(self, meta):
		pass

	def prep_display(self):
		pass

	def json(self):
		return {
			'exid' : self.exid,
			'source' : self.source,
			'display' : self.display,
			'meta': self.data
		}

	def metadatum(self, key, value):
		return { 'key' : key, 'value': value }