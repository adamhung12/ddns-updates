# setup email module
import smtplib, ssl
def sendMessage(msg):
 mail_sender = "a@a.com"
 mail_receiver = "a@a.com"
 mail_password = ""
 sender_email = mail_sender
 receiver_email = mail_receiver
 msg['From'] = sender_email
 msg['To'] = receiver_email
 password = mail_password
 port = 465 # For SSL
 smtp_server = "smtp.zoho.com"
 context = ssl.create_default_context()
 server = smtplib.SMTP_SSL(smtp_server, port,context)
 server.login(sender_email, password)
 server.sendmail(sender_email, receiver_email, msg.as_string())
 server.quit()
 

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import requests
import json

try:
 host=""
 domain = ""
 password = ""
 
 r = requests.get("https://api.myip.com/")
 jsonData=json.loads(r.content)
 ip = jsonData["ip"]
  
 url = "https://dynamicdns.park-your-domain.com/update?host={}&domain={}&password={}&ip={}".format(host,domain,password,ip)
 r = requests.get(url)
 
 msg = MIMEMultipart('alternative')
 part1 = MIMEText("Updated the DDNS of <b>[{}.{}]</br> to <b>{}</b>".format(host, domain,ip), 'html')
 msg.attach(part1)
 msg['Subject'] = "Updated DDNS[Success]"
 sendMessage(msg) 
 
except:
 msg = MIMEMultipart('alternative')
 part1 = MIMEText("Error while updating DDNS of <b>[{}.{}]</b>".format(host, domain), 'html')
 msg.attach(part1)
 msg['Subject'] = "Updated DDNS[Fail]"
 sendMessage(msg) 
 
