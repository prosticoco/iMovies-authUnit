from db_utils import *


class UserDBManager(DBManager):

	index = {'uid':0,'lastname':1,'firstname':2,'email':3,'pwd':4}


	def __init__(self,host,user,passwd,database):

		DBManager.__init__(self,host,user,passwd,database)



	def get_user_info(self,uid):

		query = """SELECT * FROM users WHERE uid = %s"""
		parameters = uid,
		results = []

		try :

			results = self.query_db(query,parameters,prop=True)

		except Exception as e :

			print("Error fetching user information")

			raise e

		return results


	def get_pwd_hash(self,uid):

		results = self.get_user_info(uid)

		if len(results) == 0 :

			return None 

		else :
			
			return results[0][self.index['pwd']]


	def update_user_info(self,old_uid,uid,lastname,firstname,email,pwd):

		query = """UPDATE users SET uid = %s,lastname = %s,
		firstname = %s, email = %s,pwd=%s WHERE uid = %s"""
		parameters = uid,lastname,firstname,email,pwd,old_uid,

		try:

			self.query_db(query,parameters,prop=True,write=True)

		except Exception as e :

			print("Error updating user information")

			raise e






		







if __name__ == '__main__':


	test_db = UserDBManager('localhost','root','toor','imovies')

	print(test_db.get_user_info('ps'))
	






