from flask import Flask
from flask import request
import mysql.connector
import json

app = Flask(__name__)

def insert_sigfoxdata(**data):
    dns={'user':'sigfox', 'host':'localhost', 'password': 'sigfoxuno', 'database':'sigfoxdata'}
    db = mysql.connector.connect(**dns)
    cursor = db.cursor()
    cursor.execute('INSERT INTO measurement VALUES (%s,%s,%s,%s,%s,%s)',(data['deviceId'],data['time'],data['temperature'],data['humid'],data['pressure'],data['distance']))
    cursor.close()
    db.commit()
    db.close()

@app.route('/')
def hello():
    return "Hello, World!"

@app.route('/receive', methods=['POST'])
def receive_data():
    #post送信されたデータを受けとる
    data = request.json
    insert_sigfoxdata(**data)
    return data['distance']

if __name__ == '__main__':
    app.run()
