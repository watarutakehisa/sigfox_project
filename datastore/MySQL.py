import mysql.connector

class MySQL:
    def __init__(self, **dns):
        self.dns = dns
        self.dbh = None

    def _open(self):
        self.dbh = mysql.connector.MySQLConnection(**self.dns)

    def _close(self):
        self.dbh.close()



#     def insert_devicelist(self,deviceId,address):
#         self._open()
#         cursor=self.dbh.cursor()
#         cursor.execute('INSERT INTO devicelist VALUES (%s,%s)',(deviceId,address))
#         cursor.close()
#         self.dbh.commit()
#         self._close()

    def insert_devicelist(self,deviceId,address,latitude,longitude,a,b,c,d):
        self._open()
        cursor=self.dbh.cursor()
        cursor.execute('INSERT INTO devicelist VALUES (%s,%s,%s,%s,%s,%s,%s,%s)',(deviceId,address,latitude,longitude,a,b,c,d))
        cursor.close()
        self.dbh.commit()
        self._close()


    def export_sigfoxdata_all(self):
        self._open()
        cursor=self.dbh.cursor()
        cursor.execute('SELECT * FROM measurement')
        data=cursor.fetchall()
        cursor.close()
        self._close()
        return data

    def export_sigfoxdata_where_id(self,deviceId):
        self._open()
        cursor=self.dbh.cursor()
        cursor.execute('SELECT * FROM measurement WHERE deviceId = %s',(deviceId,))
        data=cursor.fetchall()
        cursor.close()
        self._close()
        return data

    #時刻が新しいデータをpickup個取り出す。
    def export_sigfoxdata_pickup_latest_where_id(self,id,pickup):
        self._open()
        cursor=self.dbh.cursor()
        cursor.execute('select * from (select * from measurement where deviceId = %s order by time desc limit %s) as A order by time;',(id,pickup,))
        data=cursor.fetchall()
        cursor.close()
        return data
    def export_predictdata_pickup_latest_where_id(self,id,pickup):
        self._open()
        cursor=self.dbh.cursor()
        cursor.execute('select * from (select * from predict where deviceId = %s order by time desc limit %s) as A order by time;',(id,pickup,))
        data=cursor.fetchall()
        cursor.close()
        return data

    def export_devicelist_all(self):
        self._open()
        cursor=self.dbh.cursor()
        cursor.execute('SELECT * FROM devicelist')
        data=cursor.fetchall()
        cursor.close()
        self._close()
        return data
    def export_devicelist_where_id(self,deviceId):
        self._open()
        cursor=self.dbh.cursor()
        cursor.execute('SELECT * FROM devicelist WHERE deviceId = %s',(deviceId,))
        data=cursor.fetchall()
        cursor.close()
        self._close()
        return data
    def insert_sigfoxdata(self,**sigfoxdata):
        # #まずmax_を取得
        device=self.export_devicelist_where_id(sigfoxdata['deviceId'])
        self._open()
        cursor=self.dbh.cursor()
        #とりあえず温度で作成
        if float(sigfoxdata['temperature']) > device[0][4]:
            warning = 1
        else:
            warning = 0

        cursor.execute('INSERT INTO measurement VALUES (%s,%s,%s,%s,%s,%s,%s)',(sigfoxdata['deviceId'],sigfoxdata['time'],sigfoxdata['temperature'],sigfoxdata['humid'],sigfoxdata['pressure'],sigfoxdata['distance'],warning))
        cursor.close()
        self.dbh.commit()
        self._close()
    def calc_warning_level(self,deviceId):
        measuredata = self.export_sigfoxdata_pickup_latest_where_id(deviceId,1)
        predictdata = self.export_predictdata_pickup_latest_where_id(deviceId,1)
        print(measuredata)
        if not ((not measuredata) or (not predictdata)):
            if measuredata[0][6]:
                warning='2'
            elif predictdata[0][6]:
                warning='1'
            else:
                warning='0'
        else:
            warning='4'
        return warning

    def insert_predictdata(self,*predictdata):
        device=self.export_devicelist_where_id(predictdata[0])
        self._open()
        cursor=self.dbh.cursor()

         #とりあえず温度で作成
        if float(predictdata[4]) > device[0][4]:
            warning = '1'
        else:
            warning = '0'

        cursor.execute('INSERT INTO predict VALUES (%s,%s,%s,%s,%s,%s,%s)',(predictdata[0],predictdata[1],predictdata[2],predictdata[3],predictdata[4],predictdata[5],warning))
        cursor.close()
        self.dbh.commit()
        self._close()

    def export_predictdata_where_id(self,deviceId):
        self._open()
        cursor=self.dbh.cursor()
        cursor.execute('SELECT * FROM predict WHERE deviceId = %s',(deviceId,))
        data=cursor.fetchall()
        cursor.close()
        self._close()
        return data

    def update_devicelist_all(self,**datalist):
        self._open()
        cursor=self.dbh.cursor()
        cursor.execute('UPDATE devicelist SET address = %s,longitude = %s,latitude = %s,max_tempreture = %s,max_humid = %s,max_pressure = %s,max_distance = %s WHERE deviceId = %s',(datalist['address'],datalist['longitude'],datalist['latitude'],datalist['max_tempreture'],datalist['max_humid'],datalist['max_pressure'],datalist['max_distance'],datalist['deviceId']))
        # cursor.execute('INSERT INTO measurement VALUES (%s,%s,%s,%s,%s,%s)',(sigfoxdata['deviceId'],sigfoxdata['time'],sigfoxdata['temperature'],sigfoxdata['humid'],sigfoxdata['pressure'],sigfoxdata['distance']))
        cursor.close()
        self.dbh.commit()
        self._close()
