def uriOrNamespace(strData, uriNs, prefix):
	if strData.startswith(uriNs):
		return prefix + strData[len(uriNs):]
	elif strData.startswith(prefix):
		return uriNs + strData[len(prefix):]
	else:
		raise ValueError('Unrecognized URI or namespace')

def rabid(strData):
	uri_prefix = "http://vivo.brown.edu/individual/"
	ns = "rabid-"
	return uriOrNamespace(strData, uri_prefix, ns)