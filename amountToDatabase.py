import mysql.connector
from mysql.connector import Error
import SmsSendor
import TokenGenerator
import time
import datetime
from coinToVolume import getCoinAmount

global tokenGenerated
global check
global user_id

def registerCustomer(phoneNumber, balance):
	try:
		global tokenGenerated
		print("Connecting to Database")
		connection = mysql.connector.connect(host='localhost',database='swamp',user='swamp',password='swamp@2022')
		mysql_select_query = """SELECT * from meters"""
		cursor = connection.cursor(dictionary=True)
		cursor.execute(mysql_select_query)
		records = cursor.fetchall()
		meter=[]

		for row in records:
			id = row["id"]
			meter.append(id)
		tokenGenerated = TokenGenerator.createToken()
		mySql_insert_query = """INSERT INTO customers(id,date_created,phone_number,meter_id,token) VALUES(%s, %s, %s, %s, %s) """
		now = time.time()
		record = (tokenGenerated,datetime.datetime.fromtimestamp(now),phoneNumber,meter[0], tokenGenerated)
		cursor = connection.cursor()
		cursor.execute(mySql_insert_query, record)
		connection.commit()

		mysql_insert_query = """INSERT INTO house_hold_balances(id,date_created,balance,user_id) VALUES(%s,%s, %s, %s)"""
		record = (tokenGenerated,datetime.datetime.fromtimestamp(now),balance,tokenGenerated)
		cursor = connection.cursor(dictionary=True)
		cursor.execute(mysql_insert_query, record)
		connection.commit()
		SmsSendor.sendSms(phoneNumber, TokenGenerator.createToken())

		print(cursor.rowcount, "You,", phoneNumber, " have been successfully registered with balance :", balance)
		cursor.close()
	except mysql.connector.Error as error:
		print("Failed to insert record into table {}".format(error))



def saveTransaction(totalVolumeDispensed, amount):
	try:
		global tokenGenerated
		print("Connecting to Database")
		now = time.time()
		connection = mysql.connector.connect(host='localhost', database='swamp',user='swamp',password='swamp@2022')
		mysql_select_query = """SELECT * from meters"""
		cursor = connection.cursor(dictionary=True)
		cursor.execute(mysql_select_query)
		records = cursor.fetchall()
		meter=[]

		for row in records:
			id = row["id"]
			meter.append(id)

		mysql_insert_query = """INSERT INTO transaction_records(id,date_created,amount_paid,water_volume_collected,meter_id) VALUES(%s,%s,%s,%s,%s)"""
		record = (tokenGenerated, datetime.datetime.fromtimestamp(now),amount,totalVolumeDispensed, meter[0])
		cursor = connection.cursor(dictionary=True)
		cursor.execute(mysql_insert_query, record)
		connection.commit()
		print(cursor.rowcount, "Transaction recorded")
		cursor.close()
	except mysql.connector.Error as error:
		print("Failed to insert record into table {}".format(error))

def checkIfToken(inputEntered):
	try:
		print("Checking if token entered is valid")
		connection = mysql.connector.connect(host='localhost',database='swamp',user='swamp',password='swamp@2022')
		mysql_sql_select_query = """SELECT * from customers WHERE token=%s"""
		cursor = connection.cursor(dictionary=True)
		cursor.execute(mysql_sql_select_query,(inputEntered,))
		record = cursor.fetchall()
		cursor.close()
		user_id = []

		if(len(record) == 0):
			print("Token not found")
			#getCoinAmount(isNowAmount)
			#check = 1
		else:
			print("Token has been found")
			for row in record:
				userId = row["id"]
				user_id.append(userId)

			mysql_select_query = """SELECT * FROM house_hold_balances where user_id=%s"""
			cursor = connection.cursor(dictionary=True)
			cursor.execute(mysql_select_query,(user_id[0],))
			record = cursor.fetchall()
			balance = []

			for row in record:
				balanceAmount = row["balance"]
				balance.append(balanceAmount)
			print("Fetching off a balance:")
			getCoinAmount(balance[0])
			check = 0
			cursor.close()
			connection.close()
	except mysql.connector.Error as error:
		print("Failed to get household balance: {}".format(error))

def updateCustomer(newBalance):
	try:
		global user_id
		print("Updating a customer")
		connection = mysql.connector.connect(host='localhost',database='swamp',user='swamp',password="swamp@2022")
		cursor = connection.cursor(dictionary=True)
		mysql_update_query = """Update house_hold_balances set balance=%s where user_id = %s"""
		input_data = (newBalance,user_id[0])
		cursor.execute(mysql_update_query,input_data)
		connection.commit()
		print("HouseholdBalance updated successfully")
		mysql_update_query = """Update customers set token=%s where id=%s"""
		newtoken= TokenGenerator.createToken()
		input_data =(newToken, user_id[0])
		cursor.execute(mysql_update_query, input_data)
		connection.commit()
		print("Customer token updated successfully")
		cursor.close()
		connection.close()
	except mysql.connector.Error as error:
		print("Failed to update record to database: {}".format(error))
