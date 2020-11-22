# -*- coding: utf-8 -*-
import json
Server = None
try:
    Server = json.load(open('./ipconfig.json'))
except:
    print 'Error while reading ipconfig'
print 'Server:',Server

tmp = raw_input('\nChange Server to: (Default=1) \n\t(1):127.0.0.1:8080 \n\t(2):djokelab.ddns.net:8080 \n\t(3):140.118.155.77:8080 \n')
if(tmp == '2'):
    Server = {'IP':"http://djokelab.ddns.net:8080"}
elif(tmp == '3'):
    Server = {'IP':"http://140.118.155.77:8080"}
else:
    Server = {'IP':"http://127.0.0.1:8080"}

tmp = raw_input('\nChange Name to: (Default=1) \n\t(1):M10815017 \n\t(2):M10815054 \n\t(3):Simulator \n')
if(tmp == '2'):
    Server['Name'] = 'M10815054'
elif(tmp == '3'):
    Server['Name'] = 'Simulator'
else:
    Server['Name'] = 'M10815017'

with open('./ipconfig.json', 'w') as outfile:
    json.dump(Server, outfile)
    
print '\nServer : ' , Server
print 'Saved.'
