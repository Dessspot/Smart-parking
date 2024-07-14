import pandas as pd
import mysql.connector
from recnum import recognum


mydb = mysql.connector.connect(
  host="192.168.31.72", # IP-адрес компьютера, где запущен MySQL сервер
  user="ali",
  password="platon1",
  database="my_db"
)
i=0
Trig=0
mycursor = mydb.cursor()
mydb.commit()
while True:
    mycursor.execute('Select is_there from flag')
    Trig = mycursor.fetchall()
    mydb.commit()
    # print(Trig)
    if Trig[0] == (1,):
        recognum(i)
        query = "UPDATE flag SET is_there = %s"
        values = ('0',)
        mycursor.execute(query, values)
        mydb.commit()
        Trig=0
        i+=1