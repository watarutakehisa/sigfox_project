from flask import Flask
from flask import request
from flask import url_for
from flask import render_template
import json

#sigfoxdataは配列、[deviceId,time,tempreture,humid,pressure,distance]
from datastore.MySQL import MySQL
dns={
    'user':'sigfox',
    'host':'localhost',
    'password': 'sigfoxuno',
    'database':'sigfoxdata'
}
db=MySQL(**dns)

# class warn:
#     def __init__(self):
#         self.warn = 0
#         self.config_max = [0,0,0,0]
#     def calculate(self,predict,measure):
#         for config in self.config_max:
#             if self.config<measure:
#                 self.warn=2
#             elif self.config<predict:
#                 self.warn=1
#             else:
#                 self.warn=0
#     def __str__(self):
#         return self.config
#     def insert_config(self,**list):
#         self.config=list
# def calculate_warning(**warning_config,**sigfoxdata):
#     for config in warning_config:

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

@app.route('/')
def devicelist():
    props = {'title': 'ホーム', 'msg': 'Sigfoxを用いた定点の気象情報観測'}
    list = db.export_devicelist_all()
    html = render_template('devicelist.html',props=props,list=list)
    #html = render_template('devicemap.html')
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
    return render_template('form.html',props=props,id=id)

@app.route('/request_form',methods = ['POST','GET'])
def request_form():
    if request.method=='POST':
        result = request_form
        return render_template("confirm.html",result=result)

#@app.route('/config',methods=['POST','GET'])
#def config():

if __name__ == '__main__':
    app.run(debug=True)
