import argparse
from server import *
from user_db_manager import * 




def main(args):

	port = args.port
	ip = args.ip
	db_username = args.user
	db_host = args.host
	db_pwd = args.pwd
	db_name = args.db

	db_manager = UserDBManager(db_host,db_username,db_pwd,db_name)
	auth_server = UserDBServer('Authentication Server',ip,port,db_manager)
	print("Server IP : {} Server Port : {}".format(ip,port))
	auth_server.run_server()


if __name__ == '__main__':

	parser = argparse.ArgumentParser()
	parser.add_argument('--port', default=5001)
	parser.add_argument('--ip',default='127.0.0.1')
	parser.add_argument('--user', default='root')
	parser.add_argument('--host', default='localhost')
	parser.add_argument('--db', default='imovies')
	parser.add_argument('--pwd', default='toor')
	arguments = parser.parse_args()
	main(arguments)



