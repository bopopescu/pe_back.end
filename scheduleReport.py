from flask import Flask, json, Response, request, render_template
from werkzeug.utils import secure_filename
from os import path, getcwd
from db import Database
import time
from datetime import date
import datetime
import matplotlib.pyplot as plt
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders





app = Flask(__name__)

app.config['file_allowed'] = ['image/png', 'image/jpeg', ]
app.config['storage'] = path.join(getcwd(), 'storage')
app.db = Database()

# Run the app
#@app.route('/api/generate', methods=['POST'])
def generate_report_daily():
    today = datetime.date.today()
    today = today.strftime("%y-%m-%d")
    print(today)
    total_count = app.db.select("select * from users")
    count_breakfast = app.db.select("select * from attendance1 where type='breakfast' and created= %s",[today])
    count_lunch = app.db.select("select * from attendance1 where type='lunch' and created= %s",[today])
    count_hitea = app.db.select("select * from attendance1 where type='hi-tea' and created= %s",[today])
    count_dinner = app.db.select("select * from attendance1 where type='dinner' and created= %s",[today])

    # print(count_breakfast)
    # print(count_lunch)
    # print(count_hitea)
    # print(count_dinner)

    grid_size = (4, 4)
    # Plot 1
    plt.subplot2grid(grid_size, (0, 0), rowspan=2, colspan=2)
    slices_breakfast = [len(count_breakfast), len(total_count) - len(count_breakfast)]
    labels = 'Present', 'Absent'
    plt.pie(slices_breakfast, labels=labels, autopct='%1.1f%%', shadow=True, startangle=140)
    plt.axis('equal')
    plt.title("Breakfast", y=-0.15, bbox={'facecolor': '0.8', 'pad': 3})

    # Plot 2
    plt.subplot2grid(grid_size, (0, 2), rowspan=2, colspan=2)
    slices_lunch = [len(count_lunch), len(total_count) - len(count_lunch)]
    labels = 'Present', 'Absent'
    plt.pie(slices_lunch, labels=labels, autopct='%1.1f%%', shadow=True, startangle=140)
    plt.title("Lunch", y=-0.1, bbox={'facecolor': '0.8', 'pad': 3})

    # Plot 3
    plt.subplot2grid(grid_size, (2, 0), rowspan=2, colspan=2)
    slices_hitea = [len(count_hitea), len(total_count) - len(count_hitea)]
    labels = 'Present', 'Absent'
    plt.pie(slices_hitea, labels=labels, autopct='%1.1f%%', shadow=True, startangle=140)
    plt.title("Hi-Tea", y=-0.1, bbox={'facecolor': '0.8', 'pad': 3})

    # Plot 4
    plt.subplot2grid(grid_size, (2, 2), rowspan=2, colspan=2)
    slices_dinner = [len(count_dinner), len(total_count) - len(count_dinner)]
    labels = 'Present', 'Absent'
    plt.pie(slices_dinner, labels=labels, autopct='%1.1f%%', shadow=True, startangle=140)
    plt.title("Dinner", y=-0.1, bbox={'facecolor': '0.8', 'pad': 3})

    today = today.strftime("%d/%m/%y")
    text = "Attendance report for '%s'"%str(today)+" (Total Expected Students: %i)" % len(total_count)
    plt.text(-4.8, -1.8, text, bbox=dict(facecolor='red', alpha=0.5))
    plt.tight_layout()

    created = date.today()
    created_format = created.strftime("%d/%m/%y")
    plt.savefig("/home/tushar/Desktop/%s" % created_format + "_report.png", bbox_inches='tight')

    send_mail(created_format)
    #plt.show()
    return


#@app.route('/api/generate', methods=['POST'])
def generate_report_weekly():

    today=datetime.date.today()
    date_week_ago=today-datetime.timedelta(days=7)
    today = today.strftime("%y-%m-%d")
    date_week_ago = date_week_ago.strftime("%y-%m-%d")
    print(today)
    print(date_week_ago)
    total_count = app.db.select("select * from users")
    count_breakfast = app.db.select("select * from attendance1 where type='breakfast' and created>= %s and created< %s",[date_week_ago,today])
    count_lunch = app.db.select("select * from attendance1 where type='lunch' and created>= %s and created< %s",
                                    [date_week_ago, today])
    count_hitea = app.db.select("select * from attendance1 where type='hi-tea' and created>= %s and created< %s",
                                    [date_week_ago, today])
    count_dinner = app.db.select("select * from attendance1 where type='dinner' and created>= %s and created< %s",
                                [date_week_ago, today])

    # print(count_breakfast)
    # print(count_lunch)
    # print(count_hitea)
    # print(count_dinner)

    grid_size = (4, 4)
    # Plot 1
    plt.subplot2grid(grid_size, (0, 0), rowspan=2, colspan=2)
    slices_breakfast=[len(count_breakfast),(len(total_count)*7)-len(count_breakfast)]
    labels='Present','Absent'
    plt.pie(slices_breakfast, labels=labels, autopct='%1.1f%%', shadow=True, startangle=140)
    plt.axis('equal')
    plt.title("Breakfast", y=-0.15, bbox={'facecolor': '0.8', 'pad': 3})

    # Plot 2
    plt.subplot2grid(grid_size, (0, 2), rowspan=2, colspan=2)
    slices_lunch = [len(count_lunch), (len(total_count) * 7) - len(count_lunch)]
    labels = 'Present', 'Absent'
    plt.pie(slices_lunch, labels=labels, autopct='%1.1f%%', shadow=True, startangle=140)
    plt.title("Lunch", y=-0.1, bbox={'facecolor': '0.8', 'pad': 3})

    # Plot 3
    plt.subplot2grid(grid_size, (2, 0), rowspan=2, colspan=2)
    slices_hitea = [len(count_hitea), (len(total_count) * 7) - len(count_hitea)]
    labels = 'Present', 'Absent'
    plt.pie(slices_hitea, labels=labels, autopct='%1.1f%%', shadow=True, startangle=140)
    plt.title("Hi-Tea", y=-0.1, bbox={'facecolor': '0.8', 'pad': 3})

    # Plot 4
    plt.subplot2grid(grid_size, (2, 2), rowspan=2, colspan=2)
    slices_dinner = [len(count_dinner), (len(total_count) * 7) - len(count_dinner)]
    labels = 'Present', 'Absent'
    plt.pie(slices_dinner, labels=labels, autopct='%1.1f%%', shadow=True, startangle=140)
    plt.title("Dinner", y=-0.1, bbox={'facecolor': '0.8', 'pad': 3})

    today = today.strftime("%d/%m/%y")
    date_week_ago=date_week_ago.strftime("%d/%m/%y")
    text="Attendance report from '%s'"%str(date_week_ago)+" to '%s'"%str(today)+" (Total Expected Students: %i)"%(len(total_count)*7)
    plt.text(-5.5,-1.8,text,bbox=dict(facecolor='red', alpha=0.5))
    plt.tight_layout()

    created = date.today()
    created_format = created.strftime("%d/%m/%y")
    plt.savefig("/home/tushar/Desktop/%s" % created_format + "_report.png", bbox_inches='tight')

    send_mail(created_format)
    #plt.show()
    return "Executed"

#@app.route('/api/generate', methods=['POST'])
def generate_report_monthly():

    today=datetime.date.today()
    date_month_ago=today-datetime.timedelta(days=30)
    today = today.strftime("%y-%m-%d")
    date_month_ago = date_month_ago.strftime("%y-%m-%d")

    print(today)
    print(date_month_ago)

    total_count = app.db.select("select * from users")
    count_breakfast = app.db.select("select * from attendance1 where type='breakfast' and created>= %s and created< %s",[date_month_ago,today])
    count_lunch = app.db.select("select * from attendance1 where type='lunch' and created>= %s and created< %s",
                                    [date_month_ago, today])
    count_hitea = app.db.select("select * from attendance1 where type='hi-tea' and created>= %s and created< %s",
                                    [date_month_ago, today])
    count_dinner = app.db.select("select * from attendance1 where type='dinner' and created>= %s and created< %s",
                                [date_month_ago, today])

    grid_size = (4, 4)

    # Plot 1
    plt.subplot2grid(grid_size, (0, 0), rowspan=2, colspan=2)
    slices_breakfast=[len(count_breakfast),(len(total_count)*30)-len(count_breakfast)]
    labels='Present','Absent'
    plt.pie(slices_breakfast, labels=labels, autopct='%1.1f%%', shadow=True, startangle=140)
    plt.axis('equal')
    plt.title("Breakfast", y=-0.15, bbox={'facecolor': '0.8', 'pad': 3})

    # Plot 2
    plt.subplot2grid(grid_size, (0, 2), rowspan=2, colspan=2)
    slices_lunch = [len(count_lunch), (len(total_count) * 30) - len(count_lunch)]
    labels = 'Present', 'Absent'
    plt.pie(slices_lunch, labels=labels, autopct='%1.1f%%', shadow=True, startangle=140)
    plt.title("Lunch", y=-0.1, bbox={'facecolor': '0.8', 'pad': 3})

    # Plot 3
    plt.subplot2grid(grid_size, (2, 0), rowspan=2, colspan=2)
    slices_hitea = [len(count_hitea), (len(total_count) * 30) - len(count_hitea)]
    labels = 'Present', 'Absent'
    plt.pie(slices_hitea, labels=labels, autopct='%1.1f%%', shadow=True, startangle=140)
    plt.title("Hi-Tea", y=-0.1, bbox={'facecolor': '0.8', 'pad': 3})

    # Plot 4
    plt.subplot2grid(grid_size, (2, 2), rowspan=2, colspan=2)
    slices_dinner = [len(count_dinner), (len(total_count) * 30) - len(count_dinner)]
    labels = 'Present', 'Absent'
    plt.pie(slices_dinner, labels=labels, autopct='%1.1f%%', shadow=True, startangle=140)
    plt.title("Dinner", y=-0.1, bbox={'facecolor': '0.8', 'pad': 3})

    today = today.strftime("%d/%m/%y")
    date_week_ago = date_month_ago.strftime("%d/%m/%y")
    text="Attendance report from '%s'"%str(date_month_ago)+" to '%s'"%str(today)+" (Total Expected Students: %i)"%(len(total_count)*30)
    plt.text(-5.5,-1.8,text,bbox=dict(facecolor='red', alpha=0.5))
    plt.tight_layout()

    created = date.today()
    created_format = created.strftime("%d/%m/%y")
    plt.savefig("/home/tushar/Desktop/%s" % created_format + "_report.png", bbox_inches='tight')

    send_mail(created_format)
    #plt.show()
    return "Executed"

def send_mail(created):

    fromaddr = "darokarshubham1994@gmail.com"
    toaddr = "shubahmdarokar@gmail.com,prashant.sangtani@gmail.com"

    # instance of MIMEMultipart
    msg = MIMEMultipart()

    # storing the senders email address
    msg['From'] = fromaddr

    # storing the receivers email address
    msg['To'] = toaddr

    # storing the subject
    msg['Subject'] = "Report generated on %s"%created

    # string to store the body of the mail
    body = "Please find the report generated on %s"%created

    # attach the body with the msg instance
    msg.attach(MIMEText(body, 'plain'))

    # open the file to be sent
    filename = "%s"%created+"_report.png"
    attachment = open("/home/tushar/Desktop/%s"%filename, "rb")

    # instance of MIMEBase and named as p
    p = MIMEBase('application', 'octet-stream')

    # To change the payload into encoded form
    p.set_payload((attachment).read())

    # encode into base64
    encoders.encode_base64(p)

    p.add_header('Content-Disposition', "attachment; filename= %s" % filename)

    # attach the instance 'p' to instance 'msg'
    msg.attach(p)

    # creates SMTP session
    s = smtplib.SMTP('smtp.gmail.com', 587)

    # start TLS for security
    s.starttls()

    # Authentication
    s.login(fromaddr, "Deepak123*")

    # Converts the Multipart msg into a string
    text = msg.as_string()

    # sending the mail
    s.sendmail(fromaddr, msg['To'].split(","), text)

    # terminating the session
    s.quit()
    return

