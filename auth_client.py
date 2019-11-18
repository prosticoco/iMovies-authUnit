import requests
import json
import argparse
import sys
import os
import traceback
import time




class Client :


	def __init__(self,ip,port,cert):


		self.ip = ip
		self.port = port
		self.cert = cert
		urlbase = 'https://' + str(ip) + ":" + str(port) + "/"
		self.url_check_user = urlbase + "check_user"
		self.url_get_info = urlbase + "get_info"
		self.url_update_info = urlbase + "update_info"
		self.url_is_admin = urlbase + "is_admin"
		self.function_dict = {'0' : self.check_user,'1' : self.get_info, '2' : self.update_info,'3' : self.is_admin}


	def run(self):

		while True :

			try :

				os.system('clear')

				print("What do you want to do ?")
				action = input("0 : Check credentials, 1 : Get info, 2 : Update info, 3 : Check if admin\n")

				function = self.function_dict.get(action,None)

				if function is None :
					print("Invalid choice")

				else :
					function()

			except KeyboardInterrupt :

				self.exit()

			except requests.exceptions.ConnectionError :

				print("Server unreachable")
				self.exit()


	def exit(self):

		print("\nGoodbye my friend\n")
		sys.exit(0)


	def is_admin(self):

		req = dict()
		req['uid'] = input("Username?\n")
		r = requests.post(self.url_is_admin,verify=self.cert,json=json.dumps(req))
		self.answer(r)


	def check_user(self):

		check = dict()
		check['uid'] = input("Username ?\n")
		check['pwd'] = input("Password ?\n")
		r = requests.post(self.url_check_user,verify=self.cert,json=json.dumps(check))
		self.answer(r)


	def answer(self,r):
		print("Answer from server:")
		try :
			print(r.json())

		except :
			print("Server unexpected answer")
		print("(Press Enter for new request)")
		i = input("")



	
	def get_info(self):

		get_info = dict()
		get_info['uid'] = input("Username?\n")
		r = requests.post(self.url_get_info,verify=self.cert,json=json.dumps(get_info))
		self.answer(r)

	
	def update_info(self):
		uid = input("Username ?\n")
		done = False
		update = dict()
		update['uid'] = uid
		update['updates'] = dict()
		while not done :

			column = input("What column to modify ? (0 if done) \n")

			if column == '0':
				done = True

			else :
				value = input("Enter new value\n")
				update['updates'][column] = value

		r = requests.post(self.url_update_info,verify=self.cert,json=json.dumps(update))
		self.answer(r)




def main(args):

	ip = args.ip
	port = args.port
	cert = args.cert
	client = Client(ip,port,cert)
	requests.packages.urllib3.disable_warnings()
	client.run()


if __name__ == '__main__':

	parser = argparse.ArgumentParser()
	parser.add_argument('--port', default=5001)
	parser.add_argument('--ip',default='10.0.0.2')
	parser.add_argument('--cert',default='keys/ca.pem')
	arguments = parser.parse_args()
	main(arguments)