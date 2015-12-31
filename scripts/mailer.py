import smtplib
import os
from email.mime.text import MIMEText
from email.header import Header
import configparser
import sys
jp='iso-2022-jp'

def gmail(subject,body):
	config = configparser.ConfigParser()
	config.read(os.getenv('TT_HOME') + "/config/private.ini")
	address = config["gmail"]["address"]
	pwd = config["gmail"]["pwd"]
	print("mail send : " + address + " , " + pwd)
	print(body)
	#Gメールでメール送信
	gm=smtplib.SMTP('smtp.gmail.com',587)
	gm.ehlo()
	gm.starttls()
	gm.ehlo()
	gm.login(address,pwd)
	message=MIMEText(
	 body.encode(jp),
	 'plain',
	 jp,
	)
	message['Subject']=str(Header(subject,jp))
	message['From']=address
	message['To']=address
	gm.sendmail(
	 address,
	 [address],
	 message.as_string(),
	)
	gm.close()
