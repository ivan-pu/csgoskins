import smtplib
from email.mime.text import MIMEText
from email.header import Header
import requests


def getrate():
    response = requests.get("https://bravenewcoin-v1.p.rapidapi.com/convert?qty=1&from=usd&to=cny",
                            headers={
                                "X-RapidAPI-Host": "bravenewcoin-v1.p.rapidapi.com",
                                "X-RapidAPI-Key": "376c5611admsh61f53a7722dee53p14534fjsn693c2a475675"
                            }
                            )
    result = response.json()
    return result['to_quantity']


rate = "%.4f" % getrate()
print(rate)
sender = 'puyifan99@sina.com'
receivers = ['712937709@qq.com']
message = MIMEText('今日汇率' + rate, 'plain', 'utf-8')
message['From'] = Header("puyifan99@sina.com")
message['To'] = Header("You")
message['Subject'] = Header("今日汇率", 'utf-8')
mail_host = "smtp.sina.com"
mail_user = "puyifan99@sina.com"
mail_pass = "PYF686999!!"
smtpObj = smtplib.SMTP()
smtpObj.connect(mail_host, 25)  # port 25
smtpObj.login(mail_user, mail_pass)
# smtpObj.sendmail(sender, receivers, message.as_string())
print("Success")
