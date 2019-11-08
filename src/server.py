from flask import Flask, request, Response, jsonify, make_response
from cerberus import Validator
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

	
	def __init__(self,name,ip,port,db_manager,cert_path=None,key_path=None):

		Server.__init__(self,name,ip,port,certificate= cert_path, key = key_path)
		self.user_db = db_manager
		self.add_url("/check_user","check_user",handler=self.check_user,methods=['POST'])
		self.add_url("/get_info","get_info",handler=self.get_info,methods=['POST'])
		self.add_url("/update_info","update_info",handler=self.update_info,methods=['POST'])


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


	def validate_request(self,r,validator = None):

		if not self.has_json(r):

			return self.error_response("Invalid HTTP Request : No JSON",400)

		json_data = r.get_json()

		if not self.json_validator(json_data):

			return self.error_response("Invalid JSON format",400)

		data = json.loads(json_data)

		if not validator.validate(data):

			return self.error_response("Invalid JSON Fields",400)


		return None


	def hash_password(self,pwd):

		return hashlib.sha1(pwd.encode('utf-8')).hexdigest()


	

	def check_user(self):

		try :

			error = self.validate_request(request,validator = JSONValidators.check_user)

			if error is not None :

				return error

			data = json.loads(request.get_json())
			response_json = dict()

			if not self.user_db.exists(data['uid']):

				response_json['valid'] = False
				response_json['type'] = 2
				response_json['description'] = "User Not Found"
				return make_response(jsonify(response_json),200)

			hashed = self.hash_password(data['pwd'])
			stored_hash = self.user_db.get_pwd_hash(data['uid'])

			if stored_hash != hashed :

				response_json['valid'] = False
				response_json['type'] = 1
				response_json['description'] = "Wrong Password"

			else :

				response_json['valid'] = True
				response_json['type'] = 0
				response_json['description'] = "Valid Credentials"

			return make_response(jsonify(response_json),200)

		except:

			return self.error_response("Server Error",400)


	def get_info(self):

		try :

			error = self.validate_request(request,validator = JSONValidators.get_info)

			if error is not None :

				return error

			response_json = dict()
			data = json.loads(request.get_json())

			if not self.user_db.exists(data['uid']):

				response_json['found'] = False
				response_json['info'] = dict()

			else :

				info = self.user_db.get_user_info_dict(data['uid'])	
				response_json['found'] = True
				response_json['info'] = info

			return make_response(jsonify(response_json),200)

		except :

			return self.error_response("Server Error",400)

	
	def update_info(self):

		try :

			error = self.validate_request(request,validator=JSONValidators.update_info)

			if error is not None :

				return error

			response_json = dict()
			data = json.loads(request.get_json())
			updates = data['updates']
			uid = data['uid']

			# check if user exists

			if not self.user_db.exists(uid):

				response_json['updated'] = False
				response_json['type'] = 2
				response_json['description'] = 'User Not Found'
				return make_response(jsonify(response_json),200)

			# check if asking for new id, and if so check that new id does not already exists

			new_uid = updates.get('uid',False)

			if new_uid and new_uid != uid :

				if self.user_db.exits(new_uid) :

					response_json['updated'] = False
					response_json['type'] = 1
					response_json['description'] = 'UID already taken'
					return make_response(jsonify(response_json),200)

			# check is password change, if so hash the password
			
			pwd = updates.get('pwd',False)

			if pwd :

				updates['pwd'] = self.hash_password(pwd)

			for (column,value) in updates.items() :

				self.user_db.update_user_info(uid,column,value)

			response_json['updated'] = True
			response_json['type'] = 1
			response_json['description'] = "Info updated with success"
			return make_response(jsonify(response_json),200)

		except :

			return self.error_response("Server Error",400)






class JSONValidators :

	check_user = Validator({
		"uid" : {
			"type" : "string",
			"required" : True
		},

		"pwd" : {
			"type" : "string",
			"required" : True
		}
	})

	get_info = Validator({
		"uid" : {
			"type" : "string",
			"required" : True
		}
	})

	update_info = Validator({
		"uid" : {
			"type" : "string",
			"required" : True
		},
		"updates" : {
			"type" : "dict",
			"required" : True,
			"schema" : {
				"uid" : {
					"type" : "string",
					"required" : False
				},
				"lastname" : {
					"type" : "string",
					"required" : False
				},
				"firstname" : {
					"type" : "string",
					"required" : False
				},
				"email" : {
					"type" : "string",
					"required" : False
				},
				"pwd" : {
					"type" : "string",
					"required" : False
				}
			}
		}
	})

	



















