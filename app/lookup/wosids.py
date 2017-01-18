import json
import requests
import zeep

def get_details(wosidList):
	auth_wsdl = 'http://search.webofknowledge.com/esti/wokmws/ws/WOKMWSAuthenticate?wsdl'
	search_wsdl = 'http://search.webofknowledge.com/esti/wokmws/ws/WokSearchLite?wsdl'
	auth_client = zeep.Client(wsdl=auth_wsdl)
	search_client = zeep.Client(wsdl=search_wsdl)

	session_id = auth_client.service.authenticate()
	sid =  { 'Cookie' : 'SID="{0}"'.format(session_id) }
	search_client.transport.session.headers.update(sid)

	retrv_params = {
					'firstRecord': 1,
					'count': 1
					}
	params = {
				'databaseId': 'WOS',
				'uid': 'WOS:000361759900002',
				'queryLanguage': 'en',
				'retrieveParameters': retrv_params
			}
	print search_client.service.retrieveById( **params )
	auth_client.service.closeSession()