import mysql.connector

database = mysql.connector.connect(
    host = "192.168.0.19", 
    user = "temporal", 
    password = "1234567",
    database = "zortekv3"
)