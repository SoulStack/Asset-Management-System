import os
import logging
import smtplib,ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import pyodbc as py
import time
import requests


def connection():
     host="10.0.175.122"
     response= os.system("ping -c 1" + host)
     while True:
          if response==0: 
                  print("up")
          else:
              server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
              server.login("assetmanagement.soul@gmail.com", "Soulsvciot01")
              server.sendmail(
                    "assetmanagement.soul@gmail.com",
                    "assetmangement.soul@gmail.com",
                    "the host {} is  down".format(host))
              server.quit()




connection()
