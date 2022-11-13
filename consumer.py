import mysql.connector
from kafka import KafkaConsumer
import ast

try:
    mydb = mysql.connector.connect(host = 'localhost', user = 'root', password = '',database = 'ksebdb')
except mysql.connector.Error as e:
    print("MySql error",e)

mycursor = mydb.cursor()

bootstrap_server = ["localhost:9092"]

topic = "ksebtopic"

consumer = KafkaConsumer(topic, bootstrap_servers = bootstrap_server)

for i in consumer:
    print(str(i.value.decode()))
    res = ast.literal_eval(i.value.decode()) 
    
   
    userId =res.get('userid')
    unit = res.get('unit')
    print(res.get('userid'),res.get('unit'))
    sql = 'INSERT INTO `usages`(`user_id`, `unit`, `date`) VALUES (%s,%s,now())'
    data = (userId,unit)
    mycursor.execute(sql,data)
    mydb.commit()
    print("Data inserted successfully.")