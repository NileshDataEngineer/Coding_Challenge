import mysql.connector


def connect():
    try:
        mysql_db = mysql.connector.connect(host='mysqldb', user='root', password='root', port=3306)
        return mysql_db

    except ConnectionError:
        print("Exception : Mysql Connection Failed at Connect()")