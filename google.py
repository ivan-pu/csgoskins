# -*- coding: utf-8 -*-
import smtplib
from email.mime.text import MIMEText
from email.header import Header
import requests


def getrate():
    response = requests.get(
        "https://currency-converter5.p.rapidapi.com/currency/convert?format=json&from=USD&to=CNY&amount=1",
        headers={
            "X-RapidAPI-Host": "currency-converter5.p.rapidapi.com",
            "X-RapidAPI-Key": "376c5611admsh61f53a7722dee53p14534fjsn693c2a475675"
        }
    )
    result = response.json()
    return result['rates']['CNY']['rate']


rate = getrate()
print(rate)
# sender = 'puyifan99@gmail.com'
# receivers = ['712937709@qq.com']
# message = MIMEText("Today's convert rate from USD to CNY" + rate, 'plain', 'utf-8')
# message['From'] = Header("puyifan99@gmail.com")
# message['To'] = Header("You")
# message['Subject'] = Header("Today's convert rate from USD to CNY", 'utf-8')
# mail_host = "smtp.gmail.com"
# mail_user = "puyifan99@gmail.com"
# mail_pass = "PYF686999@@"
# smtpObj = smtplib.SMTP_SSL("smtp.gmail.com")
# smtpObj.connect("smtp.gmail.com", 465)  # port
# smtpObj.login(mail_user, mail_pass)
# smtpObj.sendmail(sender, receivers, message.as_string())
# print("Success")