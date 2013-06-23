#!/bin_/env/python

import urllib2
import json

class XBMCTransport(object):
	def execute(self, method, args):
		pass

class XBMCJsonTransport(XBMCTransport):
	def __init__(self, url, username='xbmc', password='xbmc'):
		self.url=url
		self.username=username
		self.password=password
		self.id = 0
	def execute(self, method, *args, **kwargs):
		header = {
			'Content-Type' : 'application/json',
			'User-Agent' : 'python-xbmc'
		}
		if len(args) == 1:
			args=args[0]
		params = kwargs
		params['jsonrpc']='2.0'
		params['id']= self.id
		self.id += 1
		params['method']=method
		params['params']=args
		
		values=json.dumps(params)
		print values
		password_mgr = urllib2.HTTPPasswordMgrWithDefaultRealm()
		password_mgr.add_password(None, self.url, self.username, self.password)
		auth_handler = urllib2.HTTPBasicAuthHandler(password_mgr)
#                auth_handler = urllib2.HTTPBasicAuthHandler()
#                auth_handler.add_password(realm='XBMC',
#                           uri=self.url,
#                           user=self.username,
#                           passwd=self.password)
		opener = urllib2.build_opener(auth_handler)
		urllib2.install_opener(opener)
		#return None
		data = values
		req = urllib2.Request(self.url, data, header)
		response = urllib2.urlopen(req)
		the_page = response.read()
		return the_page

class XBMC(object):
	def __init__(self, url, username='xbmc', password='xbmc'):
		self.transport = XBMCJsonTransport(url, username, password)
		for cl in classes:
			s = "self.%s = %s(self.transport)"%(cl,cl)
			exec(s)
	def execute(self, *args, **kwargs):
		self.transport.execute(*args, **kwargs)

class XbmcNamespace(object):
	def __init__(self, xbmc):
		self.xbmc = xbmc
	def __getattr__(self, name):
		klass= self.__class__.__name__
		method=name
		xbmcmethod = "%s.%s"%(klass, method)
		def hook(*args, **kwargs):
			return self.xbmc.execute(xbmcmethod, *args, **kwargs)
		return hook

classes = ["VideoLibrary", "Application", "Player", "Input", "System", "Playlist", "Addons", "AudioLibrary", "Files", "GUI" , "JSONRPC", "PVR", "xbmc"]
for cl in classes:
	s = "class %s(XbmcNamespace): pass"%cl
	exec (s)

