import requests
import json
import argparse
import sys
import os




class Client :

	


	def __init__(self,ip,port):

		self.ip = ip
		self.port = port
		urlbase = 'http://' + str(ip) + ":" + str(port) + "/"
		self.url_check_user = urlbase + "check_user"
		self.url_get_info = urlbase + "get_info"
		self.url_update_info = urlbase + "update_info"
		self.function_dict = {'0' : self.check_user,'1' : self.get_info, '2' : self.update_info}


	def run(self):

		try :

			while True :

				os.system('clear')

				print("What do you want to do ?")
				action = input("0 : Check credentials, 1 : Get info, 2 : Update info\n")

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



	def check_user(self):

		check = dict()
		check['uid'] = input("Username ?\n")
		check['pwd'] = input("Password ?\n")
		r = requests.post(self.url_check_user,json=json.dumps(check))
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
		r = requests.post(self.url_get_info,json=json.dumps(get_info))
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

		r = requests.post(self.url_update_info,json=json.dumps(update))
		self.answer(r)






def main(args):

	ip = args.ip
	port = args.port
	client = Client(ip,port)
	client.run()


if __name__ == '__main__':

	parser = argparse.ArgumentParser()
	parser.add_argument('--port', default=5001)
	parser.add_argument('--ip',default='127.0.0.1')
	arguments = parser.parse_args()
	main(arguments)