#used in 'On9SQLhelpers' to login to local host root user mysql database
import mysql.connector

SQLdb =  mysql.connector.connect(
    user = 'root',
    password = 'dwjk7158',
    host = 'localhost',
    database = 'crypto')    #connects to mysql database