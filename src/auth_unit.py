import mysql.connector 


mydb = mysql.connector.connect(
	host ='localhost',
	user = 'root',
	passwd = 'toor',
	database = 'imovies'
)

cursor = mydb.cursor()