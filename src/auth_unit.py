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

	hello = "hello"

	if(hello):
		print(hello)

	parser = argparse.ArgumentParser()
	parser.add_argument('--port', default=5001,help='server port')
	parser.add_argument('--ip',default='127.0.0.1',help='server ip')
	parser.add_argument('--user', default='root',help='database username')
	parser.add_argument('--host', default='localhost',help='db username host ip')
	parser.add_argument('--db', default='imovies',help='database name')
	parser.add_argument('--pwd', default='toor',help='db user password')
	arguments = parser.parse_args()
	main(arguments)



