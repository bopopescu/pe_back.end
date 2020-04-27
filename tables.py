import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="123",
  database="face_recognition2"
)
conn=mydb.cursor()



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
 `vitamin` tinyint(1),
 `fat` FLOAT ,
 `calories` INT ,
  `iron`  FLOAT ,
  `calcium` FLOAT ,
  `carb` FLOAT ,
  PRIMARY KEY (`id`) )
           ;''')

conn.execute('''CREATE  TABLE IF NOT EXISTS diet_info(
  `uid` INT NOT NULL auto_increment ,
  `uname` VARCHAR(30),
  `height` smallint(6) ,
 `weight` smallint(6) ,
 `anaemic` smallint(6) ,
 `iron` tinyint(1) ,
  `diabetic`  tinyint(1) ,
  `calcium` tinyint(1) ,
  `vitamin` tinyint(1) ,
  PRIMARY KEY (`uid`) )
           ;''')


conn.execute('''INSERT INTO FoodMenu(dish_name,protein,vitamin,fat,calories,iron,calcium,carb) VALUES('paneer',19.1,1,26.9,100,2.16,420.0,6.1);''' )
conn.execute('''INSERT INTO FoodMenu(dish_name,protein,vitamin,fat,calories,iron,calcium,carb) VALUES('egg',12.6,0,9,131,4.33,55,0);''' )
conn.execute('''INSERT INTO FoodMenu(dish_name,protein,vitamin,fat,calories,iron,calcium,carb) VALUES('mixveg',2.9,1,0.2,65,0.8,25,13);''' )
conn.execute('''INSERT INTO FoodMenu(dish_name,protein,vitamin,fat,calories,iron,calcium,carb) VALUES('potato',1.9,3,0.1,87,0.73,10,20.1);''' )
conn.execute('''INSERT INTO FoodMenu(dish_name,protein,vitamin,fat,calories,iron,calcium,carb) VALUES('ladyfinger',1.9,3,0.2,33,0.6,82,7);''' )
conn.execute('''INSERT INTO FoodMenu(dish_name,protein,vitamin,fat,calories,iron,calcium,carb) VALUES('fruits',0.3,3,0.2,52,0,0,14);''' )
conn.execute('''INSERT INTO FoodMenu(dish_name,protein,vitamin,fat,calories,iron,calcium,carb) VALUES('cucumber',0.65,3,0.11,15,0.28,16,3.63);''' )
conn.execute('''INSERT INTO FoodMenu(dish_name,protein,vitamin,fat,calories,iron,calcium,carb) VALUES('greenvegetables',2.9,1,0.4,23,2.7,99,3.6);''' )
conn.execute('''INSERT INTO FoodMenu(dish_name,protein,vitamin,fat,calories,iron,calcium,carb) VALUES('sprouts',3,3,0.2,30,3.4,95.1,6);''' )
conn.execute('''INSERT INTO FoodMenu(dish_name,protein,vitamin,fat,calories,iron,calcium,carb) VALUES('palak',2.9,3,0.4,23,2.7,99,3.6);''' )
conn.execute('''INSERT INTO FoodMenu(dish_name,protein,vitamin,fat,calories,iron,calcium,carb) VALUES('methi',23,2,6,323,33.5,176,58);''' )
conn.execute('''INSERT INTO FoodMenu(dish_name,protein,vitamin,fat,calories,iron,calcium,carb) VALUES('curd',11,1,4.3,98,0.1,83,3.4);''' )
conn.execute('''INSERT INTO FoodMenu(dish_name,protein,vitamin,fat,calories,iron,calcium,carb) VALUES('chicken',27,2,14,239,760,15,0);''' )
conn.execute('''INSERT INTO FoodMenu(dish_name,protein,vitamin,fat,calories,iron,calcium,carb) VALUES('bread',9,2,3.2,250,3.6,20,49);''' )
conn.execute('''INSERT INTO FoodMenu(dish_name,protein,vitamin,fat,calories,iron,calcium,carb) VALUES('chapati',5.84,2,1.55,170,2.03,21,32.5);''' )
conn.execute('''INSERT INTO FoodMenu(dish_name,protein,vitamin,fat,calories,iron,calcium,carb) VALUES('chana',19,2,6,364,2.2,36,61);''' )
conn.execute('''INSERT INTO FoodMenu(dish_name,protein,vitamin,fat,calories,iron,calcium,carb) VALUES('urad',25.21,2,1.64,341000,7.57,138,58.99);''' )
conn.execute('''INSERT INTO FoodMenu(dish_name,protein,vitamin,fat,calories,iron,calcium,carb) VALUES('moong',24,2,1.2,347,6.7,132,63);''' )
conn.execute('''INSERT INTO FoodMenu(dish_name,protein,vitamin,fat,calories,iron,calcium,carb) VALUES('toor',22,2,1.5,343,5.2,130,63);''' )
conn.execute('''INSERT INTO FoodMenu(dish_name,protein,vitamin,fat,calories,iron,calcium,carb) VALUES('masoor',9,2,0.4,116,3.3,19,20);''' )
conn.execute('''INSERT INTO FoodMenu(dish_name,protein,vitamin,fat,calories,iron,calcium,carb) VALUES('cauliflower',1.9,3,0.3,25,0.4,22,5);''' )
conn.execute('''INSERT INTO FoodMenu(dish_name,protein,vitamin,fat,calories,iron,calcium,carb) VALUES('cabbage',1.3,3,0.1,25,0.5,40,6);''' )
conn.execute('''INSERT INTO diet_info(uname,height,weight,anaemic,iron,diabetic,calcium,vitamin) VALUES('Tasneem',176,46,0,0,1,1,2);''')
mydb.commit()
mydb.close()



print ("Table created successfully");
