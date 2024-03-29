from flask import Flask, request, Response, jsonify, make_response
from cerberus import Validator
import json
import logging
import os
import traceback
import hashlib
from user_db_manager import *
from utils import *

import logging
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)


class Endpoint :

	def __init__(self,action,name,secret_hash):

		self.action = action
		self.name = name
		self.secret_hash = secret_hash

	def __call__(self, *args):

		self.log_before_action(request)


		pwd = request.headers.get('secret',None) or None
	
		if pwd is None :
			self.log_no_password()
			return self.error_response("Need to Provide a Password in Header field 'secret'",401)
		
		if not self.check_pwd(pwd):
			self.log_auth_failed()
			return self.error_response('Wrong Password in Header',401)

		answer = self.action()

		return answer

	def log_auth_failed(self):

		log_line = "A Wrong password has been entered"
		logging.critical(log_line)

	def log_no_password(self):

		log_line = "No Password Given"
		logging.warning(log_line)

	def log_before_action(self,request):

		try : 

			log_line = ""
			log_line += str(Utils.asn1_date())
			log_line += str(request.method) + " "
			log_line += str(self.name) + " "
			log_line += str(request.remote_addr) + " "
			logging.info(log_line)
			if request.method == 'POST':
				log_line = str(json.loads(request.get_json()))
				logging.info(log_line)

		except Exception as e:

			log_line = "EXCEPTION CAUGHT "
			log_line += str(e) + " "
			log_line += str(request.remote_addr)
			logging.info(log_line)

	def check_pwd(self,pwd):

		hashed = hashlib.sha256(pwd.encode('utf-8')).hexdigest()
		return hashed == self.secret_hash

	def error_response(self,error_text,status_code):

		error_r = dict()
		error_r['description'] = error_text

		return make_response(jsonify(error_r),status_code) 



class Server :

	def __init__(self,name,ip,port,certificate=None,key=None,secret_file='keys/secret_password.txt'):

		self.app = Flask(name)
		self.port = port
		self.ip = ip
		self.certificate = certificate
		self.key = key
		sec = open(secret_file,'r')
		self.secret_hash = sec.read()
		sec.close()
		logging.basicConfig(filename='logs/server_user_db.log',level=logging.DEBUG)


	def add_url(self,endpoint=None,endpoint_name=None,handler=None,methods=None):
		self.app.add_url_rule(endpoint,endpoint_name,Endpoint(handler,endpoint_name,self.secret_hash),methods = methods)



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
		self.add_url("/is_admin","is_admin",handler=self.is_admin,methods=['POST'])


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

			return self.error_response("Invalid HTTP Request : No JSON",400),None

		json_data = r.get_json()

		if type(json_data) == dict:

			data = json_data

		else: 

			if not self.json_validator(json_data):

				return self.error_response("Invalid JSON format",400),None

			data = json.loads(json_data)


		if not validator.validate(data):

			return self.error_response("Invalid JSON Fields",400),None


		return None, data


	def hash_password(self,pwd):

		return hashlib.sha1(pwd.encode('utf-8')).hexdigest()


	

	def check_user(self):

		try :

			error,data = self.validate_request(request,validator = JSONValidators.check_user)

			if error is not None :

				return error

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

			error,data = self.validate_request(request,validator = JSONValidators.get_info)

			if error is not None :

				return error

			response_json = dict()

			if not self.user_db.exists(data['uid']):

				response_json['found'] = False
				response_json['info'] = dict()

			else :

				info = self.user_db.get_user_info_dict(data['uid'])	
				response_json['found'] = True
				response_json['info'] = info

			return make_response(jsonify(response_json),200)

		except :

			traceback.print_exc()
			return self.error_response("Server Error",400)

	
	def update_info(self):

		try :

			error,data = self.validate_request(request,validator=JSONValidators.update_info)

			if error is not None :

				return error

			response_json = dict()
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

				if self.user_db.exists(new_uid) :

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

				if column == 'uid' :
					self.user_db.update_admin_info(uid,value)

			response_json['updated'] = True
			response_json['type'] = 0
			response_json['description'] = "Info updated with success"
			return make_response(jsonify(response_json),200)

		except :

			return self.error_response("Server Error",400)


	def is_admin(self):

		try :

			error,data = self.validate_request(request,validator=JSONValidators.is_admin)

			if error is not None :

				return error

			response_json = dict()
			response_json['admin'] = self.user_db.is_admin(data['uid'])
			return make_response(jsonify(response_json),200)

		except :


			self.handle_error()
			return self.error_response("Server Error",400)

	
	def handle_error(self):

		traceback.print_exc()








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

	is_admin = Validator({
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

	



















