from os import path
import face_recognition
import time
import atexit

from PIL import Image
#from apscheduler.schedulers.background import BackgroundScheduler

#from scheduleReport import generate_report_daily, generate_report_monthly,generate_report_weekly


class Face:
    def __init__(self, app):
        self.storage = app.config["storage"]
        self.db = app.db
        self.faces = []  # storage all faces in caches array of face object
        self.known_encoding_faces = []  # faces data for recognition
        self.face_user_keys = {}
        print("called")
        self.load_all()

        # scheduler to generate and mail reports
        # scheduler = BackgroundScheduler()
        # print("Schduler running")
        #
        # scheduler.add_job(func=generate_report_daily, trigger='cron', hour=10, minute=55)
        # scheduler.add_job(func=generate_report_weekly, trigger='cron', day_of_week='mon', hour=11, minute=00)
        # # scheduler.add_job(func=generate_report_monthly, trigger='cron', day='last', hour=23, minute=00)
        # scheduler.add_job(func=generate_report_monthly, trigger='cron', day=1, hour=11, minute=5)
        # scheduler.start()

    def load_user_by_index_key(self, index_key=0):

        key_str = str(index_key)
        print (key_str)
        print("key str is : ")

        if key_str in self.face_user_keys:
            print("inside the loop")
            print (key_str)
            print(self.face_user_keys[key_str])
            return self.face_user_keys[key_str]

        return None

    def load_train_file_by_name(self, name):
        trained_storage = path.join(self.storage, 'trained')
        return path.join(trained_storage, name)

    def load_unknown_file_by_name(self, name):
        unknown_storage = path.join(self.storage, 'unknown')
        return path.join(unknown_storage, name)

    def load_all(self):

        results = self.db.query('SELECT id, user_id, filename, created FROM faces')
        print(results)

        print("just checking for load call ")

        for row in results:

            user_id = row[1]
            filename = row[2]

            face = {
                "id": row[0],
                "user_id": user_id,
                "filename": filename,
                "created": row[3]
            }
            self.faces.append(face)

            face_image = face_recognition.load_image_file(self.load_train_file_by_name(filename))
            # print("filename")
            # print (filename)
            face_locations = face_recognition.face_locations(face_image, number_of_times_to_upsample=0,model='cnn')
            # print("cnn")
            # print(face_locations[0])
            # top, right, bottom, left = face_locations[0]
            # face_image = face_image[top:bottom, left:right]
            # #pil_image = Image.fromarray(face_image)
            # pil_image=face_image
            # print(pil_image)
            # face_image_encoding = face_recognition.face_encodings(face_image)[0]
            print("yaha toh aaram se pohcha")
            face_image_encoding = face_recognition.face_encodings(face_image, known_face_locations=face_locations, num_jitters=3)[0]
            print("yaha kaise pohche !!")
            index_key = len(self.known_encoding_faces)
            self.known_encoding_faces.append(face_image_encoding)
            index_key_string = str(index_key)
            self.face_user_keys['{0}'.format(index_key_string)] = user_id
            print("check jj")

    def load_specific(self,userId):

        results = self.db.select("SELECT id, user_id, filename, created FROM faces where user_id=%s",[userId])
        print(results)

        print("shjjjjjjj ")

        #for row in results:
        if(len(results)>0):
            print("inside if specific")
            user_id = results[0][1]
            filename = results[0][2]

            face = {
                    "id": results[0][0],
                    "user_id": user_id,
                    "filename": filename,
                    "created": results[0][3]
            }

            self.faces.append(face)
            print(face)
            print ("check")
            face_image = face_recognition.load_image_file(self.load_train_file_by_name(filename))
            face_locations = face_recognition.face_locations(face_image, number_of_times_to_upsample=0,model='cnn')
            face_image_encoding = face_recognition.face_encodings(face_image,known_face_locations=face_locations,num_jitters=3)[0]

            #face_image_encoding = face_recognition.face_encodings(face_image)[0]
            index_key = len(self.known_encoding_faces)
            self.known_encoding_faces.append(face_image_encoding)
            index_key_string = str(index_key)
            self.face_user_keys['{0}'.format(index_key_string)] = user_id

    def recognize(self, unknown_filename):
        unknown_image = face_recognition.load_image_file(self.load_unknown_file_by_name(unknown_filename))
        print(unknown_image)
        print("manp checks 2 ")
        unknown_encoding_image = face_recognition.face_encodings(unknown_image)[0]
        print(self.known_encoding_faces)
        print("manp checks jj 3")
        results = face_recognition.compare_faces(self.known_encoding_faces, unknown_encoding_image, 0.5);
        results2 = face_recognition.api.face_distance(self.known_encoding_faces, unknown_encoding_image);

        print("results", results)
        print("manpreet")
        print("results2", results2)

        index_key = 0
        user_id = -1;
        prevmatch = 1.0

        for matched in results:

            if matched and results2[index_key]<prevmatch:
                user_id = self.load_user_by_index_key(index_key)
                prevmatch = results2[index_key]

            index_key = index_key + 1

        if(user_id == -1):
            return None
        return user_id
