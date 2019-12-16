from impala.dbapi import connect
from impala.util import as_pandas

conn=connect(host='192.168.43.128', port=10000, user='hadoop', password='sgq199907', auth_mechanism="nosasl",
             database='default')
cursor = conn.cursor()

cursor.execute('create table customer'
               '(User_ID int, Gender varchar(2), Age varchar(10), City_Category varchar(2),'
               'Stay_In_Current_City_Years varchar(10), Marital_Status tinyint)'
               'row format delimited fields terminated by \',\' stored as textfile')
cursor.execute('load data local inpath \'/usr/hadoop/dataset/user.csv\' into table customer')

cursor.execute('create table product'
               '(Product_ID varchar(10), Product_Category_1 int, Product_Category_2 int, Product_Category_3 int)'
               'row format delimited fields terminated by \',\' stored as textfile')
cursor.execute('load data local inpath \'/usr/hadoop/dataset/product.csv\' into table product')

cursor.execute('create table purchase'
               '(User_ID int, Product_ID varchar(10), Occupation int, Purchase int, Purchase_ID int)'
               'row format delimited fields terminated by \',\' stored as textfile')
cursor.execute('load data local inpath \'/usr/hadoop/dataset/order.csv\' into table purchase')

