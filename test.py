import json

from datastore.MySQL import MySQL
dns={
    'user':'sigfox',
    'host':'localhost',
    'password': 'sigfoxuno',
    'database':'sigfoxdata'
}
db=MySQL(**dns)

data={
    "deviceId":"742879",
  	"time":"1588839287",
  	"temperature":"28.12",
  	"humid":"31.480469",
  	"pressure":"1016",
  	"distance":"187"
}
db.insert_sigfoxdata(**data)
