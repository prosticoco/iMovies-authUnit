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
	cert_path = args.cert
	key_path = args.sk
	http_only = args.http_only

	if http_only :

		cert_path = None
		key_path = None 

	db_manager = UserDBManager(db_host,db_username,db_pwd,db_name)
	auth_server = UserDBServer('Authentication Server',ip,port,db_manager,cert_path=cert_path,key_path=key_path)
	print("Server IP : {} Server Port : {}".format(ip,port))
	auth_server.run_server()


if __name__ == '__main__':

	parser = argparse.ArgumentParser()
	parser.add_argument('--port', default=5001,help='server port')
	parser.add_argument('--ip',default='10.0.0.2',help='server ip')
	parser.add_argument('--user', default='root',help='database username')
	parser.add_argument('--host', default='localhost',help='db username host ip')
	parser.add_argument('--db', default='imovies',help='database name')
	parser.add_argument('--pwd', default='toor',help='db user password')
	parser.add_argument('--cert',default='keys/authentication-unit-cert.pem',help='server certificate path')
	parser.add_argument('--sk',default='keys/authentication-unit-key.pem',help='server private key path')
	parser.add_argument('--http_only', action= 'store_true',help='if present then the server will only run in http')
	arguments = parser.parse_args()
	main(arguments)



