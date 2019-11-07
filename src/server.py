from flask import Flask, request, Response, jsonify, make_response
import json
import logging
import os
import hashlib
from user_db_manager import *

import logging
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)


class Server :

	def __init__(self,name,ip,port,certificate=None,key=None):

		self.app = Flask(name)
		self.port = port
		self.ip = ip
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


	

class UserDBServer(Server) :


	verify_fields = ['uid','pwd']


	
	def __init__(self,name,ip,port,db_manager,cert_path=None,key_path=None):

		Server.__init__(self,name,ip,port,certificate= cert_path, key = key_path)
		self.user_db = db_manager
		self.add_url("/check_user","verify_credentials",handler=self.verify_credentials,methods=['POST'])


	def error_response(self,error_text,status_code):

		error_r = dict()
		error_r['description'] = error_text

		return make_response(jsonify(error_r),status_code) 


	def json_validator(self,data):

		try :

			json.loads(data)
			return True

		except ValueError as error:

			print("Invalid json")
			return False


	def has_json(self,r):

		try :

			json_data = r.get_json()
			return True

		except Exception as e :

			print("Message has no JSON")
			return False


	def validate_request(self,r,fields=[]):

		if not self.has_json(r):

			return self.error_response("Invalid HTTP Request : No JSON",400)

		json_data = r.get_json()

		if not self.json_validator(json_data):

			return self.error_response("Invalid JSON format",400)


		data = json.loads(json_data)

		if not self.verify_json_fields(fields,data):

			return self.error_response("Invalid JSON Fields",400)


		return None


	def verify_json_fields(self,fields_list,json_data):

		for field in fields_list :

			test = json_data.get(field,None)

			if test is None :

				print("Wrong Fields in JSON")
				return False

		return True


	def hash_password(self,pwd):

		return hashlib.sha1(pwd.encode('utf-8')).hexdigest()



	def verify_credentials(self):

		error = self.validate_request(request,fields = self.verify_fields)

		if error is not None :

			return error

		data = json.loads(request.get_json())
		hashed = self.hash_password(data['pwd'])

		stored_hash = self.user_db.get_pwd_hash(data['uid'])

		response_json = dict()

		if stored_hash is None :

			response_json['valid'] = False
			response_json['type'] = 2
			response_json['description'] = "User Not Found"

		elif stored_hash != hashed :

			response_json['valid'] = False
			response_json['type'] = 1
			response_json['description'] = "Wrong Password"

		else :

			response_json['valid'] = True
			response_json['type'] = 0
			response_json['description'] = "Valid Credentials"

		return make_response(jsonify(response_json),200)

	



















