import zeep
import datetime
import threading

class Session(object):

	def __init__(self):
		self.wsdl = 'http://search.webofknowledge.com/esti/wokmws/ws/WOKMWSAuthenticate?wsdl'
		self.client = zeep.Client(wsdl=self.wsdl)
		self.timer = None
		self.sid = None

	def authenticate(self):
		self.sid = self.client.service.authenticate()
		self.timer = threading.Timer( 1200, self.close )
		self.timer.start()

	def close(self):
		self.client.service.closeSession()

	def get_sid(self):
		time_now = datetime.datetime.now()
		if self.timer.is_alive:
			self.timer.cancel()
			self.timer.start()
			return self.sid
		else:
			self.authenticate()
			return self.sid