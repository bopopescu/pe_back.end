import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="123",
  database="face_recognition2"
)
conn=mydb.cursor()
#conn.execute('''DROP TABLE users;''')
#conn.execute('''DROP TABLE faces;''')
conn.execute('''CREATE  TABLE IF NOT EXISTS admin_user1(
  `id` INT NOT NULL auto_increment ,
  `admin_name` VARCHAR(150) ,
  `password` BLOB ,
  PRIMARY KEY (`id`) )
          ;''')


conn.execute('''CREATE  TABLE IF NOT EXISTS users(
  `id` INT NOT NULL auto_increment ,
  `name` VARCHAR(150) NOT NULL ,
  `created` DATE ,
  PRIMARY KEY (`id`) )
          ;''')

conn.execute('''CREATE  TABLE IF NOT EXISTS faces(
  `id` INT NOT NULL auto_increment ,
`user_id` INT,
  `filename` VARCHAR(150) NOT NULL,
 `created` DATE ,
  PRIMARY KEY (`id`) )
           ;''')
conn.execute('''CREATE  TABLE IF NOT EXISTS attendance1(
  `id` INT NOT NULL auto_increment ,
`std_id` INT,
  `std_name` VARCHAR(150) ,
  `type` VARCHAR(50) ,
 `created` DATE ,
  PRIMARY KEY (`id`) )
           ;''')

conn.execute('''CREATE  TABLE IF NOT EXISTS FoodMenu(
  `id` INT NOT NULL auto_increment ,
`dish_name` VARCHAR(150),
  `protein` FLOAT ,
 `vitamin` ENUM('A','B','C','D','E') ,
 `fat` FLOAT ,
 `calories` INT ,
  `iron`  FLOAT ,
  `calcium` FLOAT ,
  `carb` FLOAT ,
  PRIMARY KEY (`id`) )
           ;''')
conn.execute('''CREATE  TABLE IF NOT EXISTS diet_info(
  `uid` INT NOT NULL auto_increment ,
uname` VARCHAR(30),
  `height` smallint(6) ,
 `weight` smallint(6) ,
 `anaemic` smallint(6) ,
 `iron` tinyint(1) ,
  `diabetic`  tinyint(1) ,
  `calcium` tinyint(1) ,
  `vitmain` tinyint(1) ,
  PRIMARY KEY (`uid`) )
           ;''')

conn.execute('''INSERT INTO FoodMenu(dish_name,protein,vitamin,fat,calories,iron,calcium,carb) VALUES('paneer',19.1,'A',26.9,100,2.16,420.0,6.1);''' )
#dummy values from here,'A',26.9,,2.16,420,6.1);''' )
conn.execute('''INSERT INTO FoodMenu(dish_name,protein,vitamin,fat,calories,iron,calcium,carb) VALUES('egg',19.1,'A',26.9,100,2.16,420,6.1);''' )
conn.execute('''INSERT INTO FoodMenu(dish_name,protein,vitamin,fat,calories,iron,calcium,carb) VALUES('mixveg',19.1,'A',26.9,100,2.16,420,6.1);''' )
conn.execute('''INSERT INTO FoodMenu(dish_name,protein,vitamin,fat,calories,iron,calcium,carb) VALUES('potato',19.1,'A',26.9,100,2.16,420,6.1);''' )
conn.execute('''INSERT INTO FoodMenu(dish_name,protein,vitamin,fat,calories,iron,calcium,carb) VALUES('ladyfinger',19.1,'A',26.9,100,2.16,420,6.1);''' )
conn.execute('''INSERT INTO FoodMenu(dish_name,protein,vitamin,fat,calories,iron,calcium,carb) VALUES('fruits',19.1,'A',26.9,100,2.16,420,6.1);''' )
conn.execute('''INSERT INTO FoodMenu(dish_name,protein,vitamin,fat,calories,iron,calcium,carb) VALUES('cucumber',19.1,'A',26.9,100,2.16,420,6.1);''' )
conn.execute('''INSERT INTO FoodMenu(dish_name,protein,vitamin,fat,calories,iron,calcium,carb) VALUES('greenvegetables',1,'A',26.9,100,2.16,420,6.1);''' )
conn.execute('''INSERT INTO FoodMenu(dish_name,protein,vitamin,fat,calories,iron,calcium,carb) VALUES('sprouts',1,'A',26.9,100,2.16,420,6.1);''' )
conn.execute('''INSERT INTO FoodMenu(dish_name,protein,vitamin,fat,calories,iron,calcium,carb) VALUES('palak',1,'A',26.9,100,2.16,420,6.1);''' )
conn.execute('''INSERT INTO FoodMenu(dish_name,protein,vitamin,fat,calories,iron,calcium,carb) VALUES('methi',1,'A',26.9,100,2.16,420,6.1);''' )
conn.execute('''INSERT INTO FoodMenu(dish_name,protein,vitamin,fat,calories,iron,calcium,carb) VALUES('curd',1,'A',26.9,100,2.16,420,6.1);''' )
conn.execute('''INSERT INTO FoodMenu(dish_name,protein,vitamin,fat,calories,iron,calcium,carb) VALUES('chicken',1,'A',26.9,100,2.16,420,6.1);''' )
conn.execute('''INSERT INTO FoodMenu(dish_name,protein,vitamin,fat,calories,iron,calcium,carb) VALUES('bread',1,'A',26.9,100,2.16,420,6.1);''' )
conn.execute('''INSERT INTO FoodMenu(dish_name,protein,vitamin,fat,calories,iron,calcium,carb) VALUES('chapati',1,'A',26.9,100,2.16,420,6.1);''' )
conn.execute('''INSERT INTO FoodMenu(dish_name,protein,vitamin,fat,calories,iron,calcium,carb) VALUES('chana',1,'A',26.9,100,2.16,420,6.1);''' )
conn.execute('''INSERT INTO FoodMenu(dish_name,protein,vitamin,fat,calories,iron,calcium,carb) VALUES('udad',1,'A',26.9,100,2.16,420,6.1);''' )
conn.execute('''INSERT INTO FoodMenu(dish_name,protein,vitamin,fat,calories,iron,calcium,carb) VALUES('moong',1,'A',26.9,100,2.16,420,6.1);''' )
conn.execute('''INSERT INTO FoodMenu(dish_name,protein,vitamin,fat,calories,iron,calcium,carb) VALUES('tuar',1,'A',26.9,100,2.16,420,6.1);''' )
conn.execute('''INSERT INTO FoodMenu(dish_name,protein,vitamin,fat,calories,iron,calcium,carb) VALUES('masoor',1,'A',26.9,100,2.16,420,6.1);''' )
conn.execute('''INSERT INTO FoodMenu(dish_name,protein,vitamin,fat,calories,iron,calcium,carb) VALUES('cauliflower',1,'A',26.9,100,2.16,420,6.1);''' )
conn.execute('''INSERT INTO FoodMenu(dish_name,protein,vitamin,fat,calories,iron,calcium,carb) VALUES('cabbage',1,'A',26.9,100,2.16,420,6.1);''' )
mydb.commit()
mydb.close()



print ("Table created successfully");
