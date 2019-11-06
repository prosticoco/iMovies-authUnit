from flask import Flask, request, Response
import json
import logging
import os

import logging
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)


class Server :

	def __init__(self,name,ip,port,certificate=None,key=None):

		self.app = Flask(name)
		self.port = port
		self.ip = ip
		self.pipe = None
		self.certificate = certificate
		self.key = key


	def add_url(self,endpoint=None,endpoint_name=None,handler=None,methods=None):
		self.app.add_url_rule(endpoint,endpoint_name,handler,methods = methods)



	def run_server(self):

		if (self.certificate is not None) and (self.key is not None):
			self.app.run(host=self.ip,port=self.port,debug=False,
				ssl_context=(self.certificate,self.key))

		else:
			self.app.run(host=self.ip,port=self.port,debug=False)







class HTTPSServer(Server) :

	def __init__(self,name,ip,port,cert_path,key_path,cert_bytes):

		Server.__init__(self,name,ip,port,certificate= cert_path, key = key_path)
		self.certif_bytes = cert_bytes
		self.add_url("/","certif",handler=self.send_certificate,methods=['GET','HEAD'])

	def send_certificate(self):
		
		return self.certif_bytes



