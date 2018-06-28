import zmail
import requests
import configparser 
import datetime

r = requests.get('http://icanhazip.com/')

mail = {
    'subject': 'MyIpAddress',  
    'content': 'My IP Address : ' + r.text
}

# Ini Config Manage
cfg = configparser.ConfigParser()
cfg.read('MyIp.ini')
lastip = cfg.get('MyIP', 'nowip')
if lastip == r.text.strip():
    cfg.set('MyIP', 'updtime', datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    cfg.write(open('MyIp.ini', 'w'))
    pass
else:
    cfg.set('MyIP', 'lastip', lastip)
    cfg.set('MyIP', 'nowip',  r.text.strip())
    cfg.set('MyIP', 'updtime', datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    cfg.write(open('MyIp.ini', 'w'))
    server = zmail.server('394043461@qq.com', '*******************')
    server.send_mail('394043461@qq.com', mail)
