"""

@author: Aniruddha Patil


"""

from flask import Flask,render_template,request
#,redirect,url_for
import mysql.connector
from PIL import Image
from io import BytesIO
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import random
import glob
import os
import base64

app = Flask(__name__)


def convertToImageData(data1,filename):
    with open(filename, "wb") as fh:
        imageData = fh.write(base64.decodebytes(data1))
    return imageData

def convertToBinaryData(filename):
    # Convert digital data to binary format
    with open(filename, 'rb') as file:
        binaryData = file.read()
    return binaryData



def sendEmailFunc(sender_address, receiver_address,passw, otp_):
    # Email body 
    mail_content = "Please find the verification code for getting details:" + str(otp_)
    
    #Setup the MIME
    message = MIMEMultipart()
    message['From'] = sender_address
    message['To'] = receiver_address

    message['Subject'] = 'Verification code'
    
    message.attach(MIMEText(mail_content, 'plain'))
    session = smtplib.SMTP('smtp.gmail.com', 587)
    # session.ehlo()
    session.starttls() #enable security
    session.login(sender_address,passw) #login with mail_id and password
    text = message.as_string()
    
    session.sendmail(sender_address, receiver_address, text)
    
    session.close()
        

@app.route("/")
def message():        
    return render_template('Main_Page.html')


@app.route('/next_Response1',methods=['GET','POST'])
def next_Response1():
    if request.method == 'POST':
        username = request.form.get("username")
        password = request.form.get("password")
        email = request.form.get("email")
        mobile = request.form.get("mobile")
        
        # print(str(username), str(password),str(email),int(mobile))
        # username,password,email,mobile = "Aniruddha", "abcd","abc@gmail.com","9101010101"
        try:
            if len(str(int(mobile)))!=10:
                error_message="Mobile number is Invalid!!"
                return render_template("Registration.html",error=error_message)
        except:
            error_message = "Mobile number is Invalid!!"
            return render_template("Registration.html",error=error_message)
        else:
            my_database=mysql.connector.connect(host="localhost",user="root",password="Andy21@510101")
            my_cursor=my_database.cursor()
            
            my_cursor.execute("Use project")
            try:
                sql = "INSERT INTO details(username,pass,email,mobile) VALUES(%s,%s,%s,%s)"
                val = (str(username), str(password),str(email),int(mobile))
                my_cursor.execute(sql, val)
                my_database.commit()
                
                sql = "INSERT INTO supply(username,pass,email,mobile) VALUES(%s,%s,%s,%s)"
                val = (str(username), str(password),str(email),int(mobile))
                my_cursor.execute(sql, val)
                my_database.commit()

                sql = "INSERT INTO user(username,pass,email,mobile) VALUES(%s,%s,%s,%s)"
                val = (str(username), str(password),str(email),int(mobile))
                my_cursor.execute(sql, val)
                my_database.commit()

                my_cursor.close()
                print("Record inserted successfully in database")
                
                return render_template("Main_Page.html")
            except:
                print("Already record present!")
                error_message = "Username or password or mobile number is already used!! Try with other."
                return render_template("Registration.html",error=error_message)
    else:
        return render_template("Registration.html")


@app.route('/next_Response2',methods=['GET','POST'])
def next_Response2():
    if request.method == 'POST':
        username = request.form.get("username")
        password = request.form.get("password")

        my_database=mysql.connector.connect(host="localhost",user="root",password="Andy21@510101")
        my_cursor=my_database.cursor()
        
        my_cursor.execute("Use project")
        try:
            my_cursor.execute("SELECT * FROM details where username='"+username+"' and pass='"+password+"'")
            my_result = my_cursor.fetchall()
            
            if my_result == []:
                error_message="User is not registered!!"
                return render_template("Main_Page.html",error =error_message)

            for x in my_result:
              if str(username) == x[0] and str(password) == x[1]:
                  print("Success!!")
                  otp_ = random.randint(100000, 999999)
                  print(otp_,"##")
                  sender_address = "patilaniruddha01@gmail.com"
                  #receiver_address = "patilaniruddha@kccemsr.edu.in"
                  receiver_address = x[2]

                  passw = "ddbfdvdnuhavvzsr"
                  try:
                      sendEmailFunc(sender_address,receiver_address,passw,str(otp_))
                      global OTP
                      global Pwd
                      # Uname = str(username)
                      Pwd = str(password)
                      OTP= otp_
                  except:
                      print("Error while sending an email!")    
                  return render_template('Final_Verification.html')
              else:
                  print("Incorrect username or password!")
                  error_message = "Incorrect username or password!"
            
                  return render_template("Main_Page.html",error =error_message)
        except:
            error_message = "Incorrect username or password!"
            
            return render_template("Main_Page.html",error =error_message)
    
    return render_template("Main_Page.html")
        
    
@app.route('/verification',methods=['GET','POST'])
def verification():        
    if request.method == 'POST':
        print(OTP)
        otp = request.form.get("otp")
        if int(otp)==int(OTP):
            print(OTP,"Final success")
            my_database=mysql.connector.connect(host="localhost",user="root",password="Andy21@510101")
            my_cursor=my_database.cursor()
            
            my_cursor.execute("Use project")
            try:
                my_cursor.execute("SELECT * FROM details where pass='"+str(Pwd)+"'")
                my_result = my_cursor.fetchall()
                
                print(my_result[0][0])
                return render_template("Main_Display.html", uname=my_result[0][0],email=my_result[0][2],mobile=my_result[0][3])                    
            except:
                error_message= "Result not found!"
                return render_template('Final_Verification.html',error=error_message)
        else:
            error_message= "Incorrect OTP!!"
            return render_template('Final_Verification.html',error=error_message)

    return render_template('Main_Page.html')


@app.route('/next_Response3',methods=['GET'])
def next_Response3():
    my_database=mysql.connector.connect(host="localhost",user="root",password="Andy21@510101")
    my_cursor=my_database.cursor()
            
    my_cursor.execute("Use project")
    try:
                my_cursor.execute("SELECT * FROM details where pass='"+str(Pwd)+"'")
                my_result = my_cursor.fetchall()
                
                print(my_result[0][0])
                return render_template("Main_Display.html", uname=my_result[0][0],email=my_result[0][2],mobile=my_result[0][3])                    
    except:
                error_message= "Result not found!"
                return render_template('Final_Verification.html',error=error_message)


@app.route('/next_Response4',methods=['GET'])
def next_Response4():
    return render_template('About.html')


@app.route('/next_Response5',methods=['GET'])
def next_Response5():
    return render_template('About_MDisp.html')


@app.route('/next_Response6',methods=['GET'])
def next_Response6():
    return render_template('Contact.html')


@app.route('/next_Response7',methods=['GET'])
def next_Response7():
    return render_template('Contact_MDisp.html')



@app.route('/next_Response8',methods=['GET', 'POST'])
def next_Response8():
    if request.method == 'POST':
        products = request.form.get("products")
        my_database=mysql.connector.connect(host="localhost",user="root",password="Andy21@510101")
        my_cursor=my_database.cursor()
            
        my_cursor.execute("Use project")

        my_cursor.execute("SELECT * FROM details where pass='"+str(Pwd)+"'")
        my_result = my_cursor.fetchall()
        for x in my_result:
            username = x[0]
            password = x[1]
            email = x[2]
            mobile = x[3]

        sql = "INSERT INTO supply(username,pass,email,mobile,products) VALUES(%s,%s,%s,%s,%s)"
        val = (str(username), str(password),str(email),int(mobile),str(products))
        my_cursor.execute(sql, val)
        my_database.commit()
        my_cursor.close()
        print("Record inserted successfully in database")

        my_cursor=my_database.cursor()
            
        my_cursor.execute("Use project")
        my_cursor.execute("SELECT * FROM supply where pass='"+str(Pwd)+"'")
        my_result = my_cursor.fetchall()
        try:
            print(my_result)
            new_list1 = []
            for data in my_result:
                print(data)
                new_list1.append([data[4],data[5]])
            
            print(new_list1)
        # return render_template("Supplier.html",uname=my_result[0][0], prod=my_result[0][4],srv=my_result[0][5])
            return render_template("Supplier.html", data1=new_list1, uname=my_result[0][0],email=my_result[0][2],mobile=my_result[0][3])
        except:
            error_message= "Supplier not found!"
            return render_template('Supplier.html',error=error_message)

    print(my_result[0][0])
    return render_template("Main_Display.html", uname=my_result[0][0],email=my_result[0][2],mobile=my_result[0][3])


@app.route('/next_Response9',methods=['GET', 'POST'])
def next_Response9():
    if request.method == 'POST':
        services = request.form.get("services")
        my_database=mysql.connector.connect(host="localhost",user="root",password="Andy21@510101")
        my_cursor=my_database.cursor()
            
        my_cursor.execute("Use project")

        my_cursor.execute("SELECT * FROM details where pass='"+str(Pwd)+"'")
        my_result = my_cursor.fetchall()
        for x in my_result:
            username = x[0]
            password = x[1]
            email = x[2]
            mobile = x[3]

        sql = "INSERT INTO supply(username,pass,email,mobile,services) VALUES(%s,%s,%s,%s,%s)"
        val = (str(username), str(password),str(email),int(mobile),str(services))
        my_cursor.execute(sql, val)
        my_database.commit()
        my_cursor.close()
        print("Record inserted successfully in database")

        my_cursor=my_database.cursor()
            
        my_cursor.execute("Use project")
        my_cursor.execute("SELECT * FROM supply where pass='"+str(Pwd)+"'")
        my_result = my_cursor.fetchall()
        try:
            print(my_result)
            new_list1 = []
            for data in my_result:
                print(data)
                new_list1.append([data[4],data[5]])
            
            print(new_list1)
        # return render_template("Supplier.html",uname=my_result[0][0], prod=my_result[0][4],srv=my_result[0][5])
            return render_template("Supplier.html", data1=new_list1, uname=my_result[0][0],email=my_result[0][2],mobile=my_result[0][3])
        except:
            error_message= "Supplier not found!"
            return render_template('Supplier.html',error=error_message)

    print(my_result[0][0])
    return render_template("Main_Display.html", uname=my_result[0][0],email=my_result[0][2],mobile=my_result[0][3])


@app.route('/next_Response10',methods=['GET','POST'])
def next_Response10():
    if request.method == 'POST':
        return render_template("Options.html")
    return render_template("Main_Display.html")


@app.route('/next_Response11',methods=['GET','POST'])
def next_Response11():
    if request.method == 'POST':
        services_for = request.form.get("Supplier")
        my_database=mysql.connector.connect(host="localhost",user="root",password="Andy21@510101")
        my_cursor=my_database.cursor()
        my_cursor.execute("Use project")
        my_cursor.execute("SELECT * FROM supply where pass='"+str(Pwd)+"'")
        my_result = my_cursor.fetchall()
        try:
            print(my_result)
            new_list1 = []
            for data in my_result:
                print(data)
                new_list1.append([data[4],data[5]])
            
            print(new_list1)


        # return render_template("Supplier.html",uname=my_result[0][0], prod=my_result[0][4],srv=my_result[0][5])
            return render_template("Supplier.html", data1=new_list1, uname=my_result[0][0],email=my_result[0][2],mobile=my_result[0][3])
        except:
            error_message= "Supplier not found!"
            return render_template('Options.html',error=error_message)
    
    return render_template("Options.html")

@app.route('/next_Response12',methods=['GET','POST'])
def next_Response12():
    if request.method == 'POST':
        services_for = request.form.get("Customer")
        my_database=mysql.connector.connect(host="localhost",user="root",password="Andy21@510101")
        my_cursor=my_database.cursor()
        my_cursor.execute("Use project")
        my_cursor.execute("SELECT * FROM supply where pass='"+str(Pwd)+"'")
        my_result = my_cursor.fetchall()
        try:
            print(my_result)
            new_list1 = []
            for data in my_result:
                print(data)
                new_list1.append([data[4],data[5]])
            
            print(new_list1)
            
        # return render_template("Supplier.html",uname=my_result[0][0], prod=my_result[0][4],srv=my_result[0][5])
            return render_template("Customer.html", data1=new_list1, uname=my_result[0][0],email=my_result[0][2],mobile=my_result[0][3])
        except:
            error_message= "Supplier not found!"
            return render_template('Customer.html',error=error_message)
    
    return render_template("Options.html")


@app.route('/next_Response13',methods=['GET', 'POST'])
def next_Response13():
    if request.method == 'POST':
        services = request.form.get("services")
        my_database=mysql.connector.connect(host="localhost",user="root",password="Andy21@510101")
        my_cursor=my_database.cursor()
            
        my_cursor.execute("Use project")

        my_cursor.execute("SELECT * FROM details where pass='"+str(Pwd)+"'")
        my_result = my_cursor.fetchall()
        for x in my_result:
            username = x[0]
            password = x[1]
            email = x[2]
            mobile = x[3]

        sql = "INSERT INTO user(username,pass,email,mobile,services) VALUES(%s,%s,%s,%s,%s)"
        val = (str(username), str(password),str(email),int(mobile),str(services))
        my_cursor.execute(sql, val)
        my_database.commit()
        print("Record inserted successfully in database")

        my_cursor.execute("SELECT * FROM supply where pass='"+str(Pwd)+"'")
        my_result = my_cursor.fetchall()
        try:
            print(my_result)
            new_list1 = []
            for data in my_result:
                print(data)
                new_list1.append([data[4],data[5]])
            
            print(new_list1)
            
        # return render_template("Supplier.html",uname=my_result[0][0], prod=my_result[0][4],srv=my_result[0][5])
            return render_template("Customer.html", data1=new_list1, uname=my_result[0][0],email=my_result[0][2],mobile=my_result[0][3])
        except:
            error_message= "Supplier not found!"
            return render_template('Customer.html',error=error_message)
    
    return render_template("Options.html")


@app.route('/next_Response14',methods=['GET'])
def next_Response14():
    my_database=mysql.connector.connect(host="localhost",user="root",password="Andy21@510101")
    my_cursor=my_database.cursor()
            
    my_cursor.execute("Use project")
    my_cursor.execute("SELECT products,services FROM user where pass='"+str(Pwd)+"'")
    my_result = my_cursor.fetchall()
    return render_template("Show.html", users=my_result)


@app.route('/next_Response15',methods=['GET', 'POST'])
def next_Response15():
    if request.method == 'POST':
        products = request.form.get("products")
        my_database=mysql.connector.connect(host="localhost",user="root",password="Andy21@510101")
        my_cursor=my_database.cursor()
            
        my_cursor.execute("Use project")

        my_cursor.execute("SELECT * FROM details where pass='"+str(Pwd)+"'")
        my_result = my_cursor.fetchall()
        for x in my_result:
            username = x[0]
            password = x[1]
            email = x[2]
            mobile = x[3]

        sql = "INSERT INTO user(username,pass,email,mobile,products) VALUES(%s,%s,%s,%s,%s)"
        val = (str(username), str(password),str(email),int(mobile),str(products))
        my_cursor.execute(sql, val)
        my_database.commit()
        print("Record inserted successfully in database")

        my_cursor.execute("SELECT * FROM supply where pass='"+str(Pwd)+"'")
        my_result = my_cursor.fetchall()
        try:
            print(my_result)
            new_list1 = []
            for data in my_result:
                print(data)
                new_list1.append([data[4],data[5]])
            
            print(new_list1)
            
        # return render_template("Supplier.html",uname=my_result[0][0], prod=my_result[0][4],srv=my_result[0][5])
            return render_template("Customer.html", data1=new_list1, uname=my_result[0][0],email=my_result[0][2],mobile=my_result[0][3])
        except:
            error_message= "Supplier not found!"
            return render_template('Customer.html',error=error_message)
    
    return render_template("Options.html")


if __name__=='__main__':
    app.run(host="localhost",port=5000,threaded=False)
    

