import mysql.connector 
import sys
import traceback





class DBManager :


	def __init__(self,host,user,passwd,database):

		self.connection = mysql.connector.connect(host= host,user = user,
			passwd =passwd,database = database)
		self.cursor = self.connection.cursor(prepared=True)


	def err_handler(self,exc):

		print("DBManager Error :")
		print(type(exc))
		traceback.print_exc()


	def query_db(self,query,q_tuple=None,write=False,prop=False):

		result = None

		try:

			if q_tuple is not None:

				self.cursor.execute(query,q_tuple)

			else :

				self.cursor.execute(query)
			
			if write :

				self.connection.commit()

			else:

				result = self.cursor.fetchall()

		except Exception as e :

			self.err_handler(e)

			if prop :

				raise Exception

		return result






if __name__ == '__main__':
	
	example_query_select = """INSERT INTO users VALUES ('id2',
	'Smith','Will','ws@aol.com','1234notevenhashed')"""
	test = DBManager('localhost','root','toor','imovies')
	test.query_db(example_query_select)


