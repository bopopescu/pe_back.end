from flask import Flask, json, Response, request, render_template, send_file
from werkzeug.utils import secure_filename
from os import path, getcwd
from db import Database
from face import Face
import time
from datetime import date, datetime, timedelta
import csv
import requests
from flask_cors import CORS
from cryptography.fernet import Fernet

app = Flask(__name__)
CORS(app)

app.config['file_allowed'] = ['image/png', 'image/jpeg']
app.config['storage'] = path.join(getcwd(), 'storage')
app.db = Database()
app.face = Face(app)
pass_key = "pRmgMa8T0INjEAfksaq2aafzoZXEuwKI7wDe4c1F8AY="
cipher_suite = Fernet(pass_key)

nutri_list=[]  #list of protein,vitamin,fat,calories,iron,calcium,carb values
# will only store values for one dish and no whole menu.
# its just a sample. we'll have to change it into double list or something once menu input is taken
def success_handle(output, status=200, mimetype='application/json'):
    resp = Response(output, status=status, mimetype=mimetype)

    return resp


def error_handle(error_message, status=500, mimetype='application/json'):
    return Response(json.dumps({"error": {"message": error_message}}), status=status, mimetype=mimetype)


def get_user_by_id(user_id):
    print("user id is :")
    print(user_id)
    user = {}
    results = app.db.select(
        "SELECT users.id, users.name, users.created, faces.id, faces.user_id, faces.filename,faces.created FROM users LEFT JOIN faces ON faces.user_id = users.id WHERE users.id = %s",
        [user_id])

    index = 0
    for row in results:
        face = {
            "id": row[3],
            "user_id": row[4],
            "filename": row[5],
            "created": row[6],
        }
        if index == 0:
            user = {
                "id": row[0],
                "name": row[1],
                "created": row[2],
                "faces": [],
            }
        if row[3]:
            user["faces"].append(face)
        index = index + 1

    if 'id' in user:
        return user
    return None


def delete_user_by_id(user_id):
    app.db.delete('DELETE FROM users WHERE users.id = ?', [user_id])
    # also delete all faces with user id
    app.db.delete('DELETE FROM faces WHERE faces.user_id = ?', [user_id])

#   Route for Hompage
@app.route('/', methods=['GET'])
def page_home():

    return render_template('index.html')

@app.route('/api', methods=['GET'])
def homepage():
    output = json.dumps({"api": '1.0'})
    return success_handle(output)


@app.route('/api/train', methods=['POST'])
def train():
    print("aa gaya yaha toh !!!")
    output = json.dumps({"success": True})

    if 'file' not in request.files:

        print ("Face image is required")
        return error_handle("Face image is required.")
    else:

        print("File request", request.files)
        file = request.files['file']

        if file.mimetype not in app.config['file_allowed']:

            print("File extension is not allowed")

            return error_handle("We are only allow upload file with *.png , *.jpg")
        else:

            # get name in form data
            name = request.form['name']

            print("Information of that face", name)

            print("File is allowed and will be saved in ", app.config['storage'])

            now = datetime.now()
            timestamp = datetime.timestamp(now)

            filename = secure_filename(file.filename) + str(timestamp)
            trained_storage = path.join(app.config['storage'], 'trained')
            file.save(path.join(trained_storage, filename))
            # let start save file to our storage

            # save to our sqlite database.db
            #created = int(time.time())
            created = date.today()
            created_format = created.strftime("%y-%m-%d")
            print("name is :"+name)
            print("created is ")
            print(created)
            user_id = app.db.insert('INSERT INTO users(name, created) values(%s,%s)', [name, str(created_format)])

            if user_id:

                print("User saved in data", name, user_id)
                # user has been save with user_id and now we need save faces table as well

                face_id = app.db.insert('INSERT INTO faces(user_id, filename, created) values(%s,%s,%s)',
                                        [user_id, filename, str(created_format)])

                if face_id:

                    print("cool face has been saved")
                    face_data = {"id": face_id, "filename": filename, "created": created}
                    return_output = json.dumps({"id": user_id, "name": name, "face": [face_data]})
                    print("before train")
                    app.face.load_specific(user_id)
                    print("after train")
                    #app.face = Face(app)
                    return success_handle(return_output)
                else:

                    print("An error saving face image.")

                    return error_handle("n error saving face image.")

            else:
                print("Something happend")
                return error_handle("An error inserting new user")

        print("Request is contain image")
    return success_handle(output)

@app.route('/api/diet', methods=['POST'])
def diet():

    name = request.json['name']
    height = request.json['height']
    weight = request.json['weight']
    anaemic = request.json['anaemia']
    iron = request.json['iron']
    diabetic = request.json['diabetes']
    calcium = request.json['calcium']
    vitamin = request.json['vitamin']

    user_id = app.db.insert('INSERT INTO diet_info(uname, height, weight, anaemic, iron, diabetic, calcium, vitmain) '
                            'values(%s, %s, %s, %s, %s, %s, %s, %s)',
                            [name, height, weight, anaemic, iron, diabetic, calcium, vitamin])

    output = json.dumps({"success": True, "data": user_id})
    return success_handle(output)



@app.route('/api/login', methods=['POST'])
def login():
    admin_name = request.form['admin_name']
    print("Information of that face", admin_name)

    admin_password = request.form['admin_password']
    print("Information of that face", admin_password)

    password = app.db.select('select password from admin_user1 where admin_name = %s', [admin_name])

    print("tamp")
    print(password)

    print("manp test")
    print(str(cipher_suite.decrypt( password.encode() )))

    print(str(cipher_suite.decrypt( password[0][0][2:-1].encode() ))[2:-1])
    if password == None or len(password)==0 or  str(cipher_suite.decrypt( password))!=admin_password:
       output = json.dumps({"success": False})
       return success_handle(output)


    output = json.dumps({"success": True})
    return success_handle(output)


@app.route('/api/register-login', methods=['POST'])
def registerLogin():
    admin_name = request.form['admin_name']
    print("Information of that face", admin_name)

    admin_password = request.form['admin_password']
    print("Information of that face", admin_password)

    ciphered_password = cipher_suite.encrypt(admin_password.encode())

    user_id = app.db.insert('INSERT INTO admin_user1(admin_name, password) values(%s,%s)', [admin_name, ciphered_password])

    output = json.dumps({"success": True, "data": user_id})
    return success_handle(output)

# route for user profile
@app.route('/api/menu', methods=['POST'])   #change this
def treat_menu():
    print(request.json)
    print(request.json['bread'])
    print(request.json['starter'])
    print(request.json['dal'])
    print(request.json['rice'])
    print(request.json['dessert'])
    print(request.json['gravy'])
    print(request.json['salad'])
    output = json.dumps({"success": True, "data": "hello"})
    return success_handle(output)
    #return nutrition value in output vaiable
    #define variables
    #call function find_main_ingrediants() for each item in lowercase
    #call function find_nutrition_content() for each list

def find_main_ingrediants(str):
    list=[]
    name = str.split(" ")
    if "paneer" in name:
        list.append("paneer")
    if "veg" in name or "vegetable" in name:
        list.append("mixveg")
    if "egg" in name:
        list.append("egg")
    if "potato" in name or "aloo" in name:
        list.append("potato")
    if "bhindi" in name or "ladyfinger" in name:
        list.append("bhindi")
    if "fruit" in name or "fruits" in name:
        list.append("fruits")
    if "veg" in name or "vegetable" in name:
        list.append("greenvegetables")
    if "cucumber" in name or "khira" in name:
        list.append("cucumber")
    if "sprouts" in name or "pulse" in name or "chickpea" in name:
        list.append("sprouts")
    if "palak" in name or "spinach" in name:
        list.append("spinach")
    if "methi" in name or "fenugreek" in name:
        list.append("methi")
    if "curd" in name or "dahi" in name:
        list.append("curd")
    if "bread" in name or "pao" in name:
        list.append("bread")
    if "chapathi" in name or "chapati" in name or "roti" in name or "paratha" in name:
        list.append("chapati")
    if "chana" in name and "dal" in name:
        list.append("chana")
    if "udad" in name and "dal" in name:
        list.append("udad")
    if "moong" in name and "dal" in name:
        list.append("moong")
    if "dal" in name and "moong" not in name and "masoor" not in name:
        list.append("tuar")
    if "masoor" in name and "dal" in name:
        list.append("masoor")
    if "cauliflower" in name or ("gobhi" in name and "patta" not in name):
        list.append("cauliflower")
    if "cabbage" in name or ("gobhi" in name and "patta" in name):
        list.append("cabbage")
    return list

def find_nutrition_content(list):
    global nutri_list
    nutri_list=[0,[],0,0,0,0,0]
    for i in range(0,len(list)):
        results= app.db.select('select protein,vitamin,fat,calories,iron,calcium,carb from FoodMenu where dish_name = %s', [list[i]])
        for row in results:
            nutri_list[0] += row[0]
            nutri_list[1].append(row[0])
            nutri_list[2] += row[2]
            nutri_list[3] += row[3]
            nutri_list[4] += row[4]
            nutri_list[5] += row[5]
            nutri_list[6] += row[6]
    nutri_list[0]/=len(i)
    nutri_list[2] /= len(i)
    nutri_list[3] /= len(i)
    nutri_list[4] /= len(i)
    nutri_list[5] /= len(i)
    nutri_list[6] /= len(i)
    
def suggest_food(name):
    

@app.route('/api/users/<int:user_id>', methods=['GET', 'DELETE'])
def user_profile(user_id):
    if request.method == 'GET':
        user = get_user_by_id(user_id)
        if user:
            return success_handle(json.dumps(user), 200)
        else:
            return error_handle("User not found", 404)
    if request.method == 'DELETE':
        delete_user_by_id(user_id)
        return success_handle(json.dumps({"deleted": True}))

def slot():
    """Return true if x is in the range [start, end]"""
    lunchhourstart = 12
    lunchminutestart = 30
    lunchhourend = 15
    lunchminuteend = 30

    bkfsthourstart = 0
    bkfstminutestart = 0
    bkfsthourend = 12
    bkfstminuteend = 30

    hteahourstart = 15
    hteaminutestart = 30
    hteahourend = 17
    hteaminuteend = 30

    dinnerhourstart = 18
    dinnerminutestart = 00
    dinnerhourend = 23
    dinnerminuteend = 50

    now = datetime.now()
    nowhour = now.hour
    nowminute = now.minute
    print(nowhour)
    print(nowminute)
    if((nowhour>=lunchhourstart and nowhour<=lunchhourend)):
        if(((nowhour == lunchhourstart and nowminute>=lunchminutestart) or
            (nowhour == lunchhourend and nowminute<=lunchminuteend)) or
                (nowhour>lunchhourstart and nowhour < lunchhourend )):
            return "lunch"

    if ((nowhour >= bkfsthourstart and nowhour <= bkfsthourend)):
        if (((nowhour == bkfsthourstart and nowminute >= bkfstminutestart) or (
                nowhour == bkfsthourend and nowminute <= bkfstminuteend)) or
                (nowhour > bkfsthourstart and nowhour < bkfsthourend )):
            return "breakfast"

    if ((nowhour >= hteahourstart and nowhour <= hteahourend)):
        if (((nowhour == hteahourstart and nowminute >= hteaminutestart) or (
                nowhour == hteahourend and nowminute <= hteaminuteend)) or
                (nowhour > hteahourstart  and nowhour <  hteahourend )):
            return "hi-tea"

    if ((nowhour >= dinnerhourstart and nowhour <= dinnerhourend)):
        if (((nowhour == dinnerhourstart and nowminute >= dinnerminutestart) or (
                nowhour == dinnerhourend and nowminute <= dinnerminuteend)) or
                (nowhour > dinnerhourstart  and nowhour < dinnerhourend )):
            return "dinner"

    return "not a valid time"

# router for recognize a unknown face
@app.route('/api/recognize', methods=['POST'])
def recognize():
    print("manpo checko")
    #print(request.files)
    if 'file' not in request.files:
        return error_handle("Image is required")
    else:
        file = request.files['file']
        # file extension valiate
        if file.mimetype not in app.config['file_allowed']:
            return error_handle("File extension is not allowed")
        else:

            filename = secure_filename(file.filename)
            unknown_storage = path.join(app.config["storage"], 'unknown')
            file_path = path.join(unknown_storage, filename)
            file.save(file_path)

            user_id = app.face.recognize(filename)
            today = date.today()
            # dd/mm/YY
            d1 = today.strftime("%y-%m-%d")
            print("d1 =", d1)

            if user_id:
                user = get_user_by_id(user_id)
                results = app.db.select(
                    "SELECT id, std_name, std_id, type, created FROM attendance1 WHERE std_id = %s and created = %s and type = %s",
                    [user_id, str(d1), slot()])
                flag = False
                if(len(results)!=0):
                    flag = True

                print("slot check ")
                nowSlot = slot()

                print(slot())
                if(not flag and slot()!="not a valid time"):
                    print("check shub")
                    print(user)
                    att_id = app.db.insert('INSERT INTO attendance1(std_id,std_name,type,created) values(%s,%s,%s,%s)', [user_id,user["name"],slot(),str(d1)])
                    print("attendance id is :")
                    print(att_id)


                results = app.db.select(
                    "SELECT id, std_name, std_id, type, created FROM attendance1 WHERE std_id = %s and created = %s and type = %s",
                    [user_id, str(d1), slot()])
                print(results)

                message = {"message": "Hey we found {0} matched with your face image".format(user["name"]),
                           "user": user}
                return success_handle(json.dumps({"id": user_id, "name": user["name"], "slot": nowSlot}))
            else:
                return error_handle("Sorry we can not found any people matched with your face image, try another image")

# router for recognize a unknown face
@app.route('/api/admin/daily/<from_date>/<to_date>', methods=['GET','POST'])
def report(from_date,to_date):

    year, month, day = map(int, from_date.split('-'))
    from_date = datetime(year, month, day)
    from_date=from_date.date()

    year, month, day = map(int, to_date.split('-'))
    to_date = datetime(year, month, day)
    to_date = to_date.date();
    print("tush")
    print((from_date - to_date).days +1)
    # print(to_date)
    total_count = app.db.select("select * from users")
    count_breakfast = app.db.select("select * from attendance1 where type='breakfast' and created>= %s and created<= %s",
                                    [from_date,to_date])
    count_lunch = app.db.select("select * from attendance1 where type='lunch' and created>= %s and created<= %s",
                                [from_date,to_date])
    count_hitea = app.db.select("select * from attendance1 where type='hi-tea' and created>= %s and created<= %s",
                                [from_date,to_date])
    count_dinner = app.db.select("select * from attendance1 where type='dinner' and created>= %s and created<= %s",
                                 [from_date,to_date])

    #print(set(total_count))
    #print("--------------------")
    #print(set(count_breakfast))
    days = ((from_date - to_date).days*-1) + 1
    return success_handle(json.dumps({"total": len(total_count)*days, "count_breakfast": len(count_breakfast), "count_lunch":len(count_lunch), "count_hitea":len(count_hitea), "count_dinner":len(count_dinner)}))
# Run the app


@app.route('/api/admin/weekly', methods=['POST'])
def weeklyReport():

    today=date.today()
    date_week_ago=today-timedelta(days=7)
    # today = today.strftime("%y-%m-%d")
    # date_week_ago = date_week_ago.strftime("%y-%m-%d")
    print(today)
    print(date_week_ago)
    total_count = app.db.select("select * from users")
    count_breakfast = app.db.select("select * from attendance1 where type='breakfast' and created>= %s and created<= %s",[date_week_ago,today])
    count_lunch = app.db.select("select * from attendance1 where type='lunch' and created>= %s and created<= %s",
                                    [date_week_ago, today])
    count_hitea = app.db.select("select * from attendance1 where type='hi-tea' and created>= %s and created<= %s",
                                    [date_week_ago, today])
    count_dinner = app.db.select("select * from attendance1 where type='dinner' and created>= %s and created<= %s",
                                [date_week_ago, today])

    single_breakfast={}
    for item in count_breakfast:
        if str(item[4]) in single_breakfast:
            single_breakfast[str(item[4])]+=1
        else:
            single_breakfast[str(item[4])]=1

    single_lunch = {}
    for item in count_lunch:
        if str(item[4]) in single_lunch:
            single_lunch[str(item[4])] += 1
        else:
            single_lunch[str(item[4])] = 1

    single_hitea = {}
    for item in count_hitea:
        if str(item[4]) in single_hitea:
            single_hitea[str(item[4])] += 1
        else:
            single_hitea[str(item[4])] = 1

    single_dinner = {}
    for item in count_dinner:
        if str(item[4]) in single_dinner:
            single_dinner[str(item[4])] += 1
        else:
            single_dinner[str(item[4])] = 1

    return success_handle(json.dumps({"total_count":len(total_count), "count_breakfast":len(count_breakfast),"count_lunch":len(count_lunch),
                                      "count_hitea":len(count_hitea), "count_dinner":len(count_dinner),
                                      "single_breakfast":single_breakfast, "single_lunch":single_lunch, "single_hitea":single_hitea,
                                      "single_dinner":single_dinner}))

def daterange(start_date, end_date):
    end_date=end_date+timedelta(1)
    for n in range(int ((end_date - start_date).days)):
        yield start_date + timedelta(n)

@app.route('/api/admin/presentList/<from_date>/<to_date>/<type>', methods=['GET','POST'])
def presentList(from_date,to_date,type):

    year, month, day = map(int, from_date.split('-'))
    from_date = datetime(year, month, day)
    from_date=from_date.date()

    year, month, day = map(int, to_date.split('-'))
    to_date = datetime(year, month, day)
    to_date = to_date.date();
    print("tush")
    print((from_date - to_date).days +1)
    # print(to_date)
    total_count = app.db.select("select * from users")
    if(type=='aggr'):
        # count_breakfast = app.db.select("select * from attendance1 where type='breakfast' and created>= %s and created<= %s",
        #                                 [from_date,to_date])
        # count_lunch = app.db.select("select * from attendance1 where type='lunch' and created>= %s and created<= %s",
        #                             [from_date,to_date])
        # count_hitea = app.db.select("select * from attendance1 where type='hi-tea' and created>= %s and created<= %s",
        #                             [from_date,to_date])
        # count_dinner = app.db.select("select * from attendance1 where type='dinner' and created>= %s and created<= %s",
        #                              [from_date,to_date])
        count= app.db.select("select * from attendance1 where created>= %s and created<= %s",[from_date,to_date])

        with open("/home/tushar/Desktop/presentStudents.csv", "w", newline="") as f:
            f.truncate()
            writer = csv.writer(f)
            writer.writerows(count)
            #f.close()

        path = "/home/tushar/Desktop/presentStudents.csv"
        return send_file(path, as_attachment=True)

    else:
        count=app.db.select("select * from attendance1 where type= %s and created>= %s and created<= %s",
                                        [type, from_date,to_date])
        with open("/home/tushar/Desktop/presentStudents.csv", "w", newline="") as f:
            f.truncate()
            writer = csv.writer(f)
            writer.writerows(count)
            #f.close()

        path = "/home/tushar/Desktop/presentStudents.csv"
        return send_file(path, as_attachment=True)

@app.route('/api/admin/absentList/<from_date>/<to_date>/<type>', methods=['GET','POST'])
def absentList(from_date,to_date,type):

    year, month, day = map(int, from_date.split('-'))
    from_date = datetime(year, month, day)
    from_date=from_date.date()

    year, month, day = map(int, to_date.split('-'))
    to_date = datetime(year, month, day)
    to_date = to_date.date();
    print("tush")
    print((from_date - to_date).days +1)
    # print(to_date)
    if(type=='aggr'):
        with open("/home/tushar/Desktop/absentStudents.csv", "w", newline="") as f:
            f.truncate()
            writer = csv.writer(f)
            for single_date in daterange(from_date,to_date):
                #absent_breakfast=app.db.select("select * from users,attendance1 where type='breakfast' and attendance1.created= %s and users.id not in (select attendance1.std_id from attendance1)",[single_date])
                # absent_breakfast = app.db.select(
                #     "select users.id,users.name,attendance1.type,attendance1.created from users,attendance1 where users.id=attendance1.std_id and attendance1.type = %s and users.id not in(select std_id from attendance1 where type=%s and created=%s)",[single_date])
                # absent_lunch = app.db.select(
                #     "select * from users where users.id not in (select std_id from attendance1 where type = 'lunch' and created= %s)",
                #     [single_date])
                # absent_hitea = app.db.select(
                #     "select * from users where users.id not in (select std_id from attendance1 where type = 'hi-tea' and created= %s)",
                #     [single_date])
                # absent_dinner = app.db.select(
                #     "select * from users where users.id not in (select std_id from attendance1 where type = 'dinner' and created= %s)",
                #     [single_date])
                count = app.db.select("select users.id,users.name,attendance1.type,attendance1.created from users,attendance1 where users.id=attendance1.std_id and users.id not in(select std_id from attendance1 where created=%s)",
                                      [single_date])
                writer.writerows(count)
                # writer.writerows(absent_lunch)
                # writer.writerows(absent_hitea)
                # writer.writerows(absent_dinner)
            #f.close()

        path = "/home/tushar/Desktop/absentStudents.csv"
        return send_file(path, as_attachment=True)

    else:
        with open("/home/tushar/Desktop/presentStudents.csv", "w", newline="") as f:
            f.truncate()
            writer = csv.writer(f)
            for single_date in daterange(from_date, to_date):
                count = app.db.select(
                    "select users.id,users.name,attendance1.type,attendance1.created from users,attendance1 where users.id=attendance1.std_id and attendance1.type = %s and users.id not in(select std_id from attendance1 where type=%s and created=%s)",
                    [type, type, single_date])
                writer.writerows(count)
                #f.close()

        path = "/home/tushar/Desktop/presentStudents.csv"
        return send_file(path, as_attachment=True)

app.run()
