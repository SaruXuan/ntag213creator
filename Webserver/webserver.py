# -*- coding: utf-8 -*-
## Environment
# pip install Flask
# pip install eventlet
# pip install flask-socketio
# pip install mysql-connector-python
from flask import *
from flask_socketio import *
import mysql.connector

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
app.config['DEBUG'] = False
socketio = SocketIO(app)    # flask_socketio

# DBhost = "127.0.0.1"
DBhost = "140.118.155.77"
DEVICE_LIST = ["M10815017", "M10815054", "Simulator"]
DEVICE_DICT = dict.fromkeys(DEVICE_LIST , False)
APPLY_WRITE = dict.fromkeys(DEVICE_LIST , False)    # 透過這個全域變數來讓設備知道是否要執行寫入
WRITE_DATA = dict.fromkeys(DEVICE_LIST , "XXXXXXXXXXXXXXXX")    # 16bytes

# Debug
# DEVICE_DICT["M10815054"] = True
DEVICE_DICT["Simulator"] = True

##### MySQL #####
print "Connecting to database... ",
AMIIBO_DB = mysql.connector.connect(
    host = DBhost,
    user = "M10815017",
    password = "0924123359",
    database = "amiibo",
)
print "done."

def DBgetGameID():
    # return int->Animal Crossing's GameID
    cursor = AMIIBO_DB.cursor()
    cursor.execute('SELECT `GAME_ID` FROM `game_name` WHERE `NAME`="Animal Crossing"')
    result = cursor.fetchall()
    return result[0][0]

def DBgetAmiiboByKey(key):
    # languageID: 1=eng 2=tchi 3=jap
    # return (unicode->NAME`, unicode->img_url)
    cursor = AMIIBO_DB.cursor()
    # SQL = 'SELECT `NAME`,`IMAGE_URL` FROM `language` as a, `treasure_name` as b, `treasure` as c WHERE a.`LANGUAGE_ID`={} AND a.`LANGUAGE_ID`=b.`LANGUAGE_ID` AND b.`TREASURE_ID`=c.`TREASURE_ID` AND `TREASURE_KEY`="{}"'.format(str(languageID), key)
    SQL = 'SELECT c.`TREASURE_ID`,a.`LANGUAGE_ID`,`NAME`,`IMAGE_URL`,`TREASURE_KEY` FROM `language` as a, `treasure_name` as b, `treasure` as c WHERE a.`LANGUAGE_ID`=b.`LANGUAGE_ID` AND b.`TREASURE_ID`=c.`TREASURE_ID` AND `TREASURE_KEY`="{}"'.format(key)
    cursor.execute(SQL)
    result = cursor.fetchall()
    try:
        data = {"name":[None, None, None], "url":result[0][3], "key":result[0][4]}
        for lan in result:
            data["name"][lan[1]-1] = lan[2]
    except:
        return None
    return data

def DBgetAllAmiibo():
    cursor = AMIIBO_DB.cursor()
    SQL = 'SELECT c.`TREASURE_ID`,a.`LANGUAGE_ID`,`NAME`,`IMAGE_URL`,`TREASURE_KEY` FROM `language` as a, `treasure_name` as b, `treasure` as c WHERE a.`LANGUAGE_ID`=b.`LANGUAGE_ID` AND b.`TREASURE_ID`=c.`TREASURE_ID`'
    cursor.execute(SQL)
    result = cursor.fetchall()
    AllData = []
    treasure_list = []
    for ami in result:
        if(ami[0] not in treasure_list):
            treasure_list.append(ami[0])
            amii = {"name":[None, None, None], "url":ami[3], "key":ami[4]}
            amii["name"][ami[1]-1] = ami[2]
            AllData.append(amii)
        else:
            index = treasure_list.index(ami[0])
            AllData[index]["name"][ami[1]-1] = ami[2]
    return AllData

##### API #####
### RC522 DEVICE ###
@app.route("/Login/<name>")
def RPI_Login(name):
    global DEVICE_DICT
    print "[NEW DEVICE]", name
    if(name in DEVICE_DICT):
        DEVICE_DICT[name] = True
        parm = {'device': name}
        emit('ActiveDevice', parm, namespace='/index', broadcast=True)
        return "Success"
    return "Fail"

@app.route("/Logout/<name>")
def RPI_Logout(name):
    global DEVICE_DICT
    print "[DEL DEVICE]", name
    if(name in DEVICE_DICT):
        DEVICE_DICT[name] = False
        parm = {'device': name}
        emit('InactiveDevice', parm, namespace='/index', broadcast=True)
        return "Success"
    return "Fail"
    
### Card Detecting ###
@app.route("/card_detected/<name>/<data>")
def CardDetected(name, data):
    print "[CardDetected]",
    print "DEVICE:", name,
    print "DATA:", data
    img_url = "/imgs/Empty.jpg"
    card_name = [u"Empty", u"空白卡", u"Empty"]
    
    if(data!="empty"):
        CardDir = DBgetAmiiboByKey(data)
        # CardDir = {'url': u'/imgs/188 ANKHA.png', 'name': [u'Ankha', u'\u8277\u540e', u'\u30ca\u30a4\u30eb'], 'key': u'YHXcd3KDw1Cjt6dn'}
        if(CardDir):
            img_url = CardDir['url']
            card_name = CardDir['name']
    parm = {'img_url':img_url , 'card_name':card_name}
    emit('CardDetected',parm, namespace='/reader' , room = name)
    if(APPLY_WRITE[name]):
        return WRITE_DATA[name]
    return 'OK'

@app.route("/write_done/<name>")
def WriteDone(name):
    print "[Write Done]",
    print "DEVICE:", name
    print
    APPLY_WRITE[name] = False
    WRITE_DATA[name] = "XXXXXXXXXXXXXXXX"
    emit('WriteDone',{}, namespace='/writer' , room = name)
    return 'OK'
    
### Sources ###
@app.route('/imgs/<path:filename>')
def image(filename):
    return send_from_directory('./static/img', filename)

@app.route('/javascript/<path:filename>')
def js(filename):
    return send_from_directory('./templates', filename)

### WEB SOCKET ###
# Join Room
@socketio.on('join', namespace='/index')
@socketio.on('join', namespace='/reader')
@socketio.on('join', namespace='/writer')
def join(message):
    room = message["room"]
    print '[Join room]', room
    join_room(room)
    
# ApplyToWrite
@socketio.on('ApplyToWrite', namespace='/writer')
def ApplyToWrite(message):
    print "[ApplyToWrite]", message
    device = message["device"]
    APPLY_WRITE[device] = True
    WRITE_DATA[device] = message["data"]
    ## Debug CardContent
    # import random
    # data = ''
    # for i in range(16):
        # data += random.choice('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789')
    # WRITE_DATA[device] = data
    ## Debug CardContent
    
    if(not message["data"]):
        WRITE_DATA[device] = ""     # PS: WRITE_DATA[device] == "" 將會erase卡片

@socketio.on('simulate', namespace='/simulator')
def simulate(message):
    content = CardDetected("Simulator", message['key'])
    print 'Sim:',message['key']
    if(content != "OK"):
        WriteDone("Simulator")
    
##### HTML #####
# DEVICE LIST
@app.route('/')
def index():
    global DEVICE_DICT
    return render_template('index.html' , device_dict = DEVICE_DICT)
    
@app.route('/sim')
def simulator():
    return render_template('simulator.html', Amiibos = DBgetAllAmiibo())
    
# Amiibo Reader
@app.route('/reader/<name>')
def reader(name):
    if(name in DEVICE_DICT):
        if(DEVICE_DICT[name]):
            return render_template('reader.html' , device = name)
    return redirect(url_for("index"))
    
# Amiibo Writer
@app.route('/writer/<name>')
def writer(name):
    if(name in DEVICE_DICT):
        if(DEVICE_DICT[name]):
            return render_template('writer.html' , device = name, Amiibos = DBgetAllAmiibo())
    return redirect(url_for("index"))

try:
    print 'Server actived'
    socketio.run(app, port=8080, host='0.0.0.0')
    
except:
    pass
    
finally:
    print '\n[Exit] webserver.py\n'   
