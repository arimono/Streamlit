import mysql.connector

# DB
sqlHost = "localhost"
sqlUsr = "username"
sqlPsw = "password"
sqlDB = "DBname"


def mysqlConnect():
    dbCre = mysql.connector.connect(
    host=sqlHost,
    user=sqlUsr,
    password=sqlPsw,
    database=sqlDB
    )
    return dbCre
