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

@app.route('/')
def devicelist():
    props = {'title': 'ホーム', 'msg': 'Sigfoxを用いた定点の気象情報観測'}
    list = db.export_devicelist_all()
    html = render_template('devicelist.html',props=props,list=list)
    return html

@app.route('/<string:id>')
def sigfoxdata(id):
    props = {'title': id+'の観測結果', 'msg': id+'の観測結果です。'}
    sigfoxdata = db.export_sigfoxdata_where_id(id)
    html = render_template('devicepage.html',props=props,sigfoxdata=sigfoxdata)
    return html

@app.route('/form/<string:id>')
def form(id):
    props = {'title': id+'の設定', 'msg': id+'の設定'}
    list = db.export_devicelist_where_id(id)
    return render_template('form.html',props=props,list=list)

@app.route('/request_form',methods = ['POST'])
def request_form():
        datalist = request.form
        db.update_devicelist_all(**datalist)
        props = {'title': 'ホーム', 'msg': 'Sigfoxを用いた定点の気象情報観測'}

        list = db.export_devicelist_all()
        html = render_template('devicelist.html',props=props,list=list)
        return html

@app.route('/receive', methods=['POST'])
def receive_data():
    #post送信されたデータを受けとる
    data = request.json
    db.insert_sigfoxdata(**data)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=80)
