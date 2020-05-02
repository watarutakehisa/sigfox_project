from MySQL import MySQL

dns={
    'user':'sigfox',
    'host':'localhost',
    'password': 'sigfoxuno',
    'database':'sigfoxdata'
}
db=MySQL(**dns)

db._open()
cursor=db.dbh.cursor()
cursor.execute('CREATE TABLE IF NOT EXISTS measurement(deviceId CHAR(6),time INT,temperature FLOAT,humid FLOAT,pressure INT,distance INT)')

cursor.execute('CREATE TABLE IF NOT EXISTS devicelist(deviceId CHAR(6) NOT NULL,address VARCHAR(30),PRIMARY KEY(deviceId))')

cursor.execute('ALTER TABLE measurement ADD warninglevel int AFTER distance')
cursor.execute('ALTER TABLE devicelist ADD (longitude FLOAT, latitude FLOAT(17,14), max_tempreture FLOAT(17,14), max_humid FLOAT, max_pressure INT, max_distance INT)')

#cursor.execute('ALTER TABLE devicelist MODIFY longitude double(9,6)')
#cursor.execute('ALTER TABLE devicelist MODIFY latitude double(8,6)')
cursor.close()
db.dbh.commit()
db._close()

db.insert_devicelist('759E68','point1')
db.insert_devicelist('742879','point2')
