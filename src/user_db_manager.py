from db_utils import *


class UserDBManager(DBManager):

	index = {'uid':0,'lastname':1,'firstname':2,'email':3,'pwd':4}


	def __init__(self,host,user,passwd,database,user_table_name='users'):

		DBManager.__init__(self,host,user,passwd,database)
		self.table_name = user_table_name


	def get_user_info(self,uid):

		query = """SELECT * FROM users WHERE uid = %s"""
		parameters = uid,
		results = []
		results = self.query_db(query,parameters)

		return results


	def get_user_info_dict(self,uid):

		results = self.get_user_info(uid)

		if(len(results) == 0):
			return None 

		infos = results[0]
		keys = list(self.index.keys())
		return {keys[i] : infos[i] for i in range(len(infos))}


	def exists(self,uid):
		return len(self.get_user_info(uid)) != 0


	def get_pwd_hash(self,uid):

		results = self.get_user_info(uid)

		if len(results) == 0 :

			return None 

		else :
			
			return results[0][self.index['pwd']]

	
	def update_user_info(self,uid,fieldname,value):

		query = """UPDATE users SET {} = %s WHERE uid = %s""".format(fieldname)
		parameters = value,uid,

		self.query_db(query,parameters,write=True)


	def update_admin_info(self,uid,value):

		query = """UPDATE admins SET uid = %s WHERE uid = %s"""
		parameters = value,uid,

		self.query_db(query,parameters,write=True)

	
	def is_admin(self,uid):

		query = """SELECT * FROM admins WHERE uid = %s"""
		parameters = uid,
		results = self.query_db(query,parameters)

		return len(results) != 0





if __name__ == '__main__':


	test_db = UserDBManager('localhost','root','toor','imovies')

	print(test_db.get_user_info_dict('ps'))
	






