# setup email module

class MailSender:
    def __init__(self, smtp_server, username, password,port):
        self.smtp_server = smtp_server
        self.username = username
        self.password = password   
        self.port = port
    
    def sendMessage(self, sender, receiver, msg):
        from email.mime.multipart import MIMEMultipart
        from email.mime.text import MIMEText
        import smtplib, ssl
        msg['From'] = sender
        msg['To'] = receiver
        context = ssl.create_default_context()
        server = smtplib.SMTP_SSL(self.smtp_server, self.port,context)
        server.login(self.username, self.password)
        print(msg.as_string())
        server.sendmail(sender, receiver, msg.as_string())
        server.quit()


def getIp():
    import requests
    import json
    r = requests.get("https://api.myip.com/")
    jsonData=json.loads(r.text)
    ip = jsonData["ip"]
    return ip;


def dns(domain):
    import socket
    return socket.gethostbyname(domain)

    
def updateDdns(host, domain,ddnsPassword, mailSender,sender,receiver, update=False):
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText
    import requests
    print("start")
    try:        
        ip = getIp()     
        print("Found ip: "+ip)
        print("Find domain ip of domain "+host+"."+domain)
        domainIp = dns(host+"."+domain)
        print("Found domain  ip: "+domainIp)
        if ip==domainIp:
            print("IP not changed")
            msg = MIMEMultipart('alternative')
            part1 = MIMEText("Updated the DDNS of <b>[{}.{}]</br> to <b>{}</b>".format(host, domain,ip), 'html')
            msg.attach(part1)
            msg['Subject'] = "Updated DDNS[{} - Unchanged]".format(host+"."+domain)
            print("messge: "+msg.as_string())
            mailSender.sendMessage(sender, receiver, msg) 
        elif update:
            print("IP updated")
            url = "https://dynamicdns.park-your-domain.com/update?host={}&domain={}&password={}&ip={}".format(host,domain,ddnsPassword,ip)
            r = requests.get(url)
            msg = MIMEMultipart('alternative')
            part1 = MIMEText("Updated the DDNS of <b>[{}.{}]</br> to <b>{}</b>".format(host, domain,ip), 'html')
            msg.attach(part1)
            msg['Subject'] = "Updated DDNS[{} - Success]".format(host+"."+domain)
            mailSender.sendMessage(sender, receiver, msg) 
        else:
            print("IP updated but no action")
    except Exception as e:
        msg = MIMEMultipart('alternative')
        print(e)
        part1 = MIMEText("Error while updating DDNS of <b>[{}.{}]</b>{}".format(host, domain, str(e)), 'html')
        msg.attach(part1)
        msg['Subject'] = "Updated DDNS[{} - Fail]".format(host+"."+domain)
        mailSender.sendMessage(sender, receiver, msg) 
     

#import sys
#sys.path.append("C:/Users/xethhung/github/ddns-updates/")
#import ddns

port = 465 # For SSL
smtp_server = "smpt server"
username = "{smpt username}"
password = "{smpt password}"

mailSender = MailSender(smtp_server,username,password,port)

updateDdns("{host}","{domain}",'{ddns password}',mailSender,"{sender email}","{receiver email}",True)
