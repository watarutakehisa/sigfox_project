#mysqlに必要なテーブルを作るファイル
from MySQL import MySQL

#mysqlの設定
dns={
    'user':'sigfox',
    'host':'localhost',
    'password': 'sigfoxuno',
    'database':'sigfoxdata'
}
db=MySQL(**dns)

db._open()
cursor=db.dbh.cursor()

cursor.execute('DROP TABLE IF EXISTS measurement')
cursor.execute('CREATE TABLE IF NOT EXISTS measurement(deviceId CHAR(6),time INT,temperature FLOAT,humid FLOAT,pressure INT,distance INT,warninglevel INT)')

cursor.execute('DROP TABLE IF EXISTS devicelist')
cursor.execute('CREATE TABLE IF NOT EXISTS devicelist(deviceId CHAR(6) NOT NULL,address VARCHAR(30),longitude double(9,6), latitude FLOAT(8,6), max_tempreture FLOAT, max_humid FLOAT, max_pressure INT, max_distance INT,PRIMARY KEY(deviceId))')

cursor.execute('DROP TABLE IF EXISTS predict')
cursor.execute('CREATE TABLE IF NOT EXISTS predict(deviceId CHAR(6),time INT,temperature FLOAT,humid FLOAT,pressure INT,distance INT,warninglevel INT)')

# 値を代入
cursor.execute("INSERT INTO devicelist VALUES('759E68','point1', 133.993549, 34.662863, 35.0, 80.0, 1020, 30)")
cursor.execute("INSERT INTO devicelist VALUES('742879','point2', 133.921242, 34.689664, 35.0, 80.0, 1020, 30)")

cursor.close()
db.dbh.commit()
db._close()
