import mysql.connector

class MySQL:
    def __init__(self, **dns):
        self.dns = dns
        self.dbh = None

    def _open(self):
        self.dbh = mysql.connector.MySQLConnection(**self.dns)

    def _close(self):
        self.dbh.close()

    def insert_sigfoxdata(self,**sigfoxdata):
        self._open()
        cursor=self.dbh.cursor()
        cursor.execute('INSERT INTO measurement VALUES (%s,%s,%s,%s,%s,%s)',(sigfoxdata['deviceId'],sigfoxdata['time'],sigfoxdata['temperature'],sigfoxdata['humid'],sigfoxdata['pressure'],sigfoxdata['distance']))
        cursor.close()
        self.dbh.commit()
        self._close()

    def export_alldata(self):
        self._open()
        cursor=self.dbh.cursor()
        cursor.execute('SELECT * FROM measurement')
        data=cursor.fetchall()
        cursor.close()
        self._close()
        return data

    def export_id_data(self,deviceId):
        self._open()
        cursor=self.dbh.cursor()
        cursor.execute('SELECT * FROM measurement WHERE deviceId %s',deviceId)
        data=cursor.fetchall()
        cursor.close()
        self._close()
        return data
