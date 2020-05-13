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

def predict_sample(id):
    #デフォルトがタプルなのでリストに変換して計算
    sigfoxdata = db.export_sigfoxdata_pickup_latest_where_id(id,1)
    data = sigfoxdata[0]
    tmp=list(data)
    tmp[1] = tmp[1] + 60 * 30
    predictdata = tuple(tmp)
    return predictdata

@app.route('/')
def devicelist():
    props = {'title': 'ホーム', 'msg': 'Sigfoxを用いた定点の気象情報観測'}
    list = db.export_devicelist_all()
    html = render_template('devicelist.html',props=props,list=list)
    return html

@app.route('/<string:id>')
def sigfoxdata(id):
    props = {'title': id+'の観測結果', 'msg': id+'の観測結果です。'}
    #measurementを取得
    sigfoxdata = db.export_sigfoxdata_where_id(id)
    #predictを取得
    predictdata = db.export_predictdata_where_id(id)
    html = render_template('devicepage.html',props=props,sigfoxdata=sigfoxdata, predictdata=predictdata)
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
    #このタイミングで予測
    predictdata=predict_sample(data['deviceId'])
    db.insert_predictdata(*predictdata)
    return data['distance']

if __name__ == '__main__':
    app.run(debug=True)
