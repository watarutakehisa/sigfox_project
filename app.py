from flask import Flask
from flask import request
from flask import url_for
from flask import render_template
import json

from datastore.MySQL import MySQL
dns={
    'user':'sigfox',
    'host':'localhost',
    'password': 'sigfoxuno',
    'database':'sigfoxdata'
}
db=MySQL(**dns)

app = Flask(__name__)

@app.route('/deviceIds')
def deviceId_list():
    props = {'title': 'DeviceId List', 'msg': 'DeviceId List'}
    list = db.export_alldata()
    html = render_template('deviceId_list.html', props=props, list=list)
    return html

@app.route('/test')
def test():
    sigfoxdata = db.export_alldata()
    html = render_template('index.html',sigfoxdata=sigfoxdata)
    return html

@app.route('/deviceId/<int:deviceId>')
def user(deviceId):
    props = {'title': 'User Information', 'msg': 'User Information'}
    stmt = 'SELECT * FROM measurement WHERE deviceId = ?'
    user = db.query(stmt, deviceId, prepared=True)
    html = render_template('user.html', props=props,user=user[0])
    return html

@app.route('/receive', methods=['POST'])
def receive_data():
    #post送信されたデータを受けとる
    data = request.json
    db.insert_sigfoxdata(**data)
    return data['distance']

@app.route('/hello')
def hello():
    stmt = 'SELECT * FROM measurement'
    deviceIds = db.query(stmt)
    return deviceIds[0][0]

if __name__ == '__main__':
    app.run(debug=True)
