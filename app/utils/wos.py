import zeep
from datetime import datetime, timedelta
import threading

class Session(object):

	def __init__(self):
		self.wsdl = 'http://search.webofknowledge.com/esti/wokmws/ws/WOKMWSAuthenticate?wsdl'
		self.client = zeep.Client(wsdl=self.wsdl)
		self.last_updated = None
		self.sid = None

	def authenticate(self):
		self.sid = self.client.service.authenticate()
		self.last_updated = datetime.now()

	def close(self):
		self.client.service.closeSession()

	def get_sid(self):
		time_now = datetime.now()
		if time_now - self.last_updated < timedelta(minutes=55):
			return self.sid
		else:
			self.authenticate()
			return self.sid