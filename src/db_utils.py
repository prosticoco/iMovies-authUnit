import mysql.connector 
import sys
import traceback




class DBManager :

	"""Summary

	Baseline class to connect to a mySQL database and execute 
	SQL queries
	
	Attributes:
	    connection (TYPE): connection to the DB
	    cursor (TYPE): DB Cursor to execute queries
	"""
	
	def __init__(self,host,user,passwd,database):
		"""Summary
		
		Args:
		    host (TYPE): IP address of user
		    user (TYPE): username
		    passwd (TYPE): password
		    database (TYPE): database name
		"""
		self.connection = mysql.connector.connect(host= host,user = user,
			passwd =passwd,database = database)
		self.cursor = self.connection.cursor(prepared=True)


	def err_handler(self,exc):
		"""Summary
		
		Args:
		    exc (Exception, optional): Exception to print
		"""
		print("DBManager Error :")
		print(type(exc))
		traceback.print_exc()


	def query_db(self,query,q_tuple=None,write=False,prop=False):
		"""Main method to query the database supports any kind of
		queries. Need to indicate is of type WRITE 
		
		Args:
		    query (TYPE): query parametrized or not
		    q_tuple (None, optional): tuple if query is parametrized
		    write (bool, optional): Indicates if DB is being updated
		    prop (bool, optional): Indicates if DB errors should be propagated
		
		Returns:
		    TYPE: Results from the query if READ query 
		
		Raises:
		    Exception: Exception to be propagated
		"""
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

				raise e

				
		return result






if __name__ == '__main__':
	
	example_query_select = """SELECT * FROM users"""

	example_query_prepared = """SELECT * FROM users
	 WHERE lastname = %s"""
	tuple_prepared = 'Schaller',


	example_query_insert = """INSERT INTO users VALUES (%s,%s,%s,%s,%s) """
	values_tuple = 'id42','Smith','John','johns@hotmail.ch','thispwdshouldbehashed'

	db_manager = DBManager('localhost','root','toor','imovies')
	result = db_manager.query_db(example_query_select)
	print(result)
	result = db_manager.query_db(example_query_prepared,tuple_prepared)
	print(result)
	result = db_manager.query_db(example_query_insert,values_tuple,write=True)
	print(result)
	result = db_manager.query_db(example_query_select)
	print(result)


