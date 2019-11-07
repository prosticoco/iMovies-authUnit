import requests
import json
import argparse
import sys


def main(args):

	ip = args.ip
	port = args.port
	urlbase = 'http://' + str(ip) + ":" + str(port) + "/"
	url_check_user = urlbase + "check_user"

	while True :

		try :

			check = dict()
			check['uid'] = input("Username ?\n")
			check['pwd'] = input("Password ?\n")
			r = requests.post(url_check_user,json=json.dumps(check))
			print(r.json())

		except KeyboardInterrupt :

			sys.exit(0)


if __name__ == '__main__':

	parser = argparse.ArgumentParser()
	parser.add_argument('--port', default=5001)
	parser.add_argument('--ip',default='127.0.0.1')
	arguments = parser.parse_args()
	main(arguments)