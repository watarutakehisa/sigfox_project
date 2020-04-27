from flask import Flask
from flask import request
import mysql.connector
import json
#from datastore.mysql import mysql


dns={'user':'sigfox', 'host':'localhost', 'password': 'sigfoxuno', 'database':'sigfoxdata'}
db = mysql.connector.connect(**dns)

app = Flask(__name__)

# def insert_test():
#     import mysql.connector
#     config={'user':'sigfox', 'host':'localhost', 'password': 'sigfoxuno', 'database':'sigfoxdata'}
#     dbh = mysql.connector.connect(**config)
#     cursor = dbh.cursor()
#     data={
#         "deviceId":"759E68",
#         "time":"1587170397",
#         "temperature":"27.58",
#         "humid":"42.32129",
#         "pressure":"1010",
#         "distance":"431"
#         }
#         cursor.execute('INSERT INTO measurement VALUES (%s,%s,%s,%s,%s,%s)',(data['deviceId'],data['time'],data['temperature'],data['humid'],data['pressure'],data['distance']))
#         cursor.close()
#         dbh.commit()
#         dbh.close()

def insert_sigfoxdata(**data):
    #config={'user':'sigfox', 'host':'localhost', 'password': 'sigfoxuno', 'database':'sigfoxdata'}
    #dbh = mysql.connector.connect(**config)
    cursor = db.cursor()
    cursor.execute('INSERT INTO measurement VALUES (%s,%s,%s,%s,%s,%s)',(data['deviceId'],data['time'],data['temperature'],data['humid'],data['pressure'],data['distance']))
    cursor.close()
    db.commit()
    db.close()


@app.route('/')
def hello():
    return "Hello, World!"

@app.route('/Japan')
def hello2():
    return "Hello, Japan!"

@app.route('/mysql', methods=['POST'])
def mysqltest():
    #post送信されたデータを受けとる
    data = request.json
    #データベースに格納する
    insert_sigfoxdata(data)
    return param['distance']

@app.route('/receive', methods=['POST'])
def receive_data():
    #post送信されたデータを受けとる
    data = request.json
    insert_sigfoxdata(data)
    return param['distance']

if __name__ == '__main__':
    app.run()
