
from flask import Flask,render_template,request
#,redirect,url_for
import mysql.connector
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import random
import glob
import os
import base64


def convertToImageData(data1,filename):
    with open(filename, "wb") as fh:
        imageData = fh.write(base64.decodebytes(data1))
    return imageData

def convertToBinaryData(filename):
    # Convert digital data to binary format
    with open(filename, 'rb') as file:
        binaryData = file.read()
    return binaryData


Pwd = "abc"
path1 = "C:\\Users\\ANIRUDDHA\\Major_Project\\BE-Major-Project/static/images/products/clutch.jpg"
my_database=mysql.connector.connect(host="localhost",user="root",password="Andy21@510101")

my_cursor=my_database.cursor()

my_cursor.execute("Use project")
my_cursor.execute("SELECT * FROM supply where pass='"+str(Pwd)+"'")
my_result = my_cursor.fetchall()
for data in my_result:
    print(data[6])

