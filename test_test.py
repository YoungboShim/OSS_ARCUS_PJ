from flask import Flask
from flask import render_template
from flask import request
from flask import session
import MySQLdb
from arcus import *
from arcus_mc_node import ArcusMCNodeAllocator
from arcus_mc_node import EflagFilter
import datetime, time, sys
from timeit import default_timer as timer

import time

app = Flask(__name__)

@app.route('/test')
def test():
       return render_template('test.html')

@app.route('/test',methods=['POST'])
@app.route('/test/<name>',methods=['POST'])
def no_arcus():
	if request.method == 'POST':
		query = "select * from data_long where K in (select cast(K as CHAR(20)) from data)"
		#Open DB connection
		db = MySQLdb.connect("localhost","root","12345678","arcus_test")

		# arcus set-up
		timeout = 20
		client = Arcus(ArcusLocator(ArcusMCNodeAllocator(ArcusTranscoder())))
		client.connect('127.0.0.1:2181', 'test')

		#prepare cursor object
		
		cursor = db.cursor()
			
		t0 = time.time()
		for count in range(1000):
			#execute SQL query
			cursor.execute(query)
			#fetch data
			data = cursor.fetchall()
			for line in data:
				#print("iter: "+str(count)+"	Value for Key "+str(i)+": "+str(line[1]))
				pass
		no_arcus = time.time() - t0
		t0 = time.time()	
		print("DB Finish")
		for count in range(1000):
			#data = client.get(str(i))
			#print ("get_result(): "+data.get_result())
			if client.get("1").get_result()!=None:
				pass
			else:	
				#cursor.execute("SELECT * FROM data WHERE K="+str(i));
				cursor.execute(query)
				data = cursor.fetchall()	
				client.set("1", "WTF", timeout)

		with_arcus = time.time() - t0
 
		client.disconnect()
		db.close()
		return render_template('test.html', name=[str(no_arcus), str(with_arcus)])


if __name__ == '__main__':
       	app.debug = True
       	app.run(host = '0.0.0.0', port = 5001)
