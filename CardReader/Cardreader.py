# -*- coding: utf-8 -*-
# Install:
# git clone https://github.com/lthiery/SPI-Py.git
# cd SPI-Py
# sudo python setup.py install
import RPi.GPIO as GPIO
import urllib2
import json
import threading
from time import sleep
from DJokeMFRC522 import *
from buzzer import *

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
# PIN_BUZZER = 18

# Server IP
config = json.load(open('./ipconfig.json'))
Server = config['IP']
RPI_name = config['Name']
# RC522
RC522 = DJ_RC522()
LastID = None

def checkEmpty(data):
    if(len(data)==16):
        for d in data:
            if d!=0:
                return False
        return True
    return False

def WriteData(data):
    # data = ["abcd", "efgh", "ijkl", "mnop"]
    if(len(data)>4):
        return False
    i = 0
    for sector in [4,5,6,7]:
        RC522.BLOCK_ADDRS = sector
        RC522.write(data[i][:4])
        i += 1
    return True

def EraseData():
    i = 0
    for sector in [4,5,6,7]:
        RC522.BLOCK_ADDRS = sector
        RC522.erase()
        i += 1
    return True

def ReadData():
    RC522.BLOCK_ADDRS = [4, 5, 6, 7]
    id, data = RC522.read()
    return id, data

def checkID(ID):
    global LastID
    sleep(1)
    if(LastID==ID):
        # print "Reset LastID"
        LastID = None

def list2str(data):
    string = ""
    for d in data:
        try:
            string += str(unichr(d))
        except:
            string += " "
    return string

print 'Server : ' , Server
print 'Name : ' , RPI_name , '\n'

while(True):
    try:
        print "RC522 Connected."
        print "Connect to",Server+"/Login/"+str(RPI_name)
        content = urllib2.urlopen(Server+"/Login/"+str(RPI_name)).read()
        print "Server Connected.\n"
        SND_connected()
        while(True):
            wait = False
            id, data = ReadData()
            if(LastID != id):
                print '[ID]:',id, '[DATA]:',data
                if not checkEmpty(data):
                    print "[Empty]: No",
                    strdata = list2str(data)
                    print "[Strdata]: \""+strdata+"\""
                    if(not strdata or " " in strdata):
                        raise TypeError
                else:
                    print "[Empty]: Yes"
                    strdata = "empty"
                print
                content = urllib2.urlopen(Server+"/card_detected/"+str(RPI_name)+"/"+strdata).read()
                if(content == "OK"):
                    SND_cardDetect()
                    threading.Thread(target=checkID, args =(id,)).start()
                else: # Need to Write content = "XXXXXXXXXXXXXXXX"
                    # data = ["abcd", "efgh", "ijkl", "mnop"]
                    print "[Writing] ",
                    if(content):
                        data = [content[i:i+4] for i in range(0,len(content),4)]
                        state = WriteData(data)
                    else:
                        state = EraseData()
                    if(state):
                        print "done.\n"
                        wait = True
                        content = urllib2.urlopen(Server+"/write_done/"+str(RPI_name)).read()
                        SND_cardDetect()
                        threading.Thread(target=checkID, args =(id,)).start()
                    else:
                        print "Error.\n"
                        SND_disconnected()
            LastID = id
            if(wait):
                sleep(1)
    except TypeError:
        SND_disconnected()
        try:
            content = urllib2.urlopen(Server+"/Logout/"+str(RPI_name)).read()
        except:
            pass
        sleep(1)
    except KeyboardInterrupt:
        print "[Exit] Closing CardReader.py ......"
        SND_disconnected()
        GPIO.cleanup()
        try:
            content = urllib2.urlopen(Server+"/Logout/"+str(RPI_name)).read()
            print "Logout:", content
        except:
            pass
        break
    except Exception as e:
        print "Error...",e
        SND_disconnected()