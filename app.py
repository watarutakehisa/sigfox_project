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
@app.route('/test')
def test():
    sigfoxdata = db.export_sigfoxdata_all()
    html = render_template('index.html',sigfoxdata=sigfoxdata)
    return html

@app.route('/receive', methods=['POST'])
def receive_data():
    #post送信されたデータを受けとる
    data = request.json
    db.insert_sigfoxdata(**data)
    return data['distance']

@app.route('/devicelist')
def devicelist():
    props = {'title': 'Device List', 'msg': 'aaa'}
    list = db.export_devicelist_all()
    html = render_template('devicelist.html',props=props,list=list)
    return html

@app.route('/<string:id>')
def sigfoxdata(id):
    sigfoxdata = db.export_sigfoxdata_where_id(id)
    html = render_template('index.html',sigfoxdata=sigfoxdata)
    return html

if __name__ == '__main__':
    app.run(debug=True)
