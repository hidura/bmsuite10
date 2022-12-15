from datetime import datetime
import sys
import os


sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import json
import requests
from flask import Flask, request, render_template, session, url_for, redirect, flash,make_response
from markupsafe import Markup
from General import Odoo,general,RequestProc, main_server
from passlib.hash import sha256_crypt as crypt
import hashlib


ALLOWED_EXTENSIONS = set(['pdf', 'png', 'jpg', 'jpeg'])


app = Flask(__name__)

UPLOAD_FOLDER = os.path.dirname(os.path.abspath(__file__))+'/static/'
with open(os.path.dirname(os.path.abspath(__file__))+"/config.json") as f:
    config = json.loads(f.read())


with app.app_context():
    None
    
static_file_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'static')




@app.route("/", methods=['GET'])
def mainpage():
    
    internal_id = request.cookies.get('int_session_id')
    print(internal_id)
    if internal_id==None:
        return render_template('login.html', basic={"title": "Sugelico 2.0"})
    session_id = request.cookies.get('session_id')
    path = request.cookies.get('path')
    dbname = request.cookies.get('dbname')
    buzz_name = request.cookies.get('buzz_name')
    
    resp = make_response(render_template('index.html',basic={'title':buzz_name}, 
                                         user_details={'name':buzz_name,
                                                                     'lastname':""}))
    
    return resp





@app.route("/logout", methods=['GET'])
def logout():
    
    resp = make_response(render_template('login.html', basic={'title':"Sugelico 2.0"}))
    resp.set_cookie('int_session_id','',expires=0)
    resp.set_cookie('path','',expires=0)
    resp.set_cookie('dbname','',expires=0)
    resp.set_cookie('buzz_name','',expires=0)
    resp.set_cookie('session_id','',expires=0)
    return resp
    




@app.route("/loginweb", methods=['POST', 'GET'])
def loginweb():
    if request.method=="POST":
        sha1=hashlib.new('sha1')
        now = datetime.now()
        date_time = now.strftime("%d/%m/%Y %H:%M:%S")
        
        sha1.update(date_time.encode('utf-8'))
        
        data = RequestProc().getRequest(request)
        
        json_info = {
        'jsonrpc': '2.0',
        'method': 'call',
        'params': {"login":data['login'],
                    'password':data['passwd'],
                    'db':'odoo15_cm'},
        'id': sha1.hexdigest()
        }
        x = requests.post(f"{main_server}/web/session/authenticate", json=json_info)
        response = json.loads(x.content.decode())
        if "error" in response:
            message = response['error']['message']
            data = response['error']['data']
            if data['name']=="odoo.exceptions.AccessDenied":
                return render_template('login.html', basic={"title": "Usuario o contraseña no validos"})
        cookie_info = x.headers['Set-Cookie']
        cookie=cookie_info.split(";")[0].split("=")[1]
        
        
        json_info = {
        'jsonrpc': '2.0',
        'method': 'call',
        'params': {"username":data['login']},
        'id': sha1.hexdigest()
        }
        getMasterInfo = requests.post(f"{main_server}/bmscore/getMasterInfo", json=json_info, 
                        headers={"Cookie":f"session_id={cookie}"})
        
        responseMaster= json.loads(getMasterInfo.content.decode())
        resp = make_response(render_template('logininternal.html', basic={'title':responseMaster["result"]["partner"]['name']}))
        resp.set_cookie('session_id', cookie)
        resp.set_cookie('path', responseMaster["result"]["odoo_path"])
        resp.set_cookie("buzz_name",responseMaster["result"]["partner"]['name'])
        resp.set_cookie("dbname",responseMaster["result"]["dbname"])
        
        return resp
    else:
        return render_template('login.html', basic={"title": "Sugelico 2.0"})


@app.route("/logininternal", methods=['POST'])
def logininternal():
    internal_id = request.cookies.get('int_session_id')
    session_id = request.cookies.get('session_id')
    path = request.cookies.get('path')
    dbname = request.cookies.get('dbname')
    buzz_name = request.cookies.get('buzz_name')
    if request.method=="POST":
        sha1=hashlib.new('sha1')
        now = datetime.now()
        date_time = now.strftime("%d/%m/%Y %H:%M:%S")
        
        sha1.update(date_time.encode('utf-8'))
        
        data = RequestProc().getRequest(request)
        
        
        json_info = {
        'jsonrpc': '2.0',
        'method': 'call',
        'params': {"login":data['login'],
                    'password':data['passwd'],
                    'db':dbname},
        'id': sha1.hexdigest()
        }
        
        x = requests.post(f"{path}/web/session/authenticate", json=json_info)
        
        cookie_info = x.headers['Set-Cookie']
        cookie=cookie_info.split(";")[0].split("=")[1]
        
        
        
        resp = make_response(render_template('index.html', basic={'title':buzz_name},
                                             user_details={'name':buzz_name,
                                                                     'lastname':""}))
        print(f"sdfasdfasfdasdf:{internal_id}")
        resp.set_cookie('int_session_id', cookie)
        
        
        return resp
    elif request.method=="GET":
        print(internal_id)
        resp = make_response(render_template('logininternal.html', basic={'title':buzz_name}))
        
    else:
        return redirect("/", code=302)

@app.route("/getFloors", methods=['POST'])
def getFloors():
    internal_id = request.cookies.get('int_session_id')
    path = request.cookies.get('path')
    
    if request.method=="POST":
        sha1=hashlib.new('sha1')
        now = datetime.now()
        date_time = now.strftime("%d/%m/%Y %H:%M:%S")
        
        sha1.update(date_time.encode('utf-8'))
        
        data = RequestProc().getRequest(request)
        
        
        json_info = {
        'jsonrpc': '2.0',
        'method': 'call',
        'params': {"pos":data['pos']},
        'id': sha1.hexdigest()
        }
        
        floors_resp = requests.post(f"{path}/bmsclient/getFloor", json=json_info, headers={"Cookie":f"session_id={internal_id}"})
        floors_result=json.loads(floors_resp.content.decode())
        
    return json.dumps(floors_result["result"])



@app.route("/getFloorTables", methods=['POST'])
def getFloorTables():
    internal_id = request.cookies.get('int_session_id')
    path = request.cookies.get('path')+"/bmsclient/getTablesByFloor"
    
    if request.method=="POST":
        sha1=hashlib.new('sha1')
        now = datetime.now()
        date_time = now.strftime("%d/%m/%Y %H:%M:%S")
        
        sha1.update(date_time.encode('utf-8'))
        
        data = RequestProc().getRequest(request)
        
        
        json_info = {
        'jsonrpc': '2.0',
        'method': 'call',
        'params': {"zone_id":data['zone']},
        'id': sha1.hexdigest()
        }
        tables_resp = requests.post(f"{path}", json=json_info, headers={"Cookie":f"session_id={internal_id}"})
        tables_list=json.loads(tables_resp.content.decode())
        return tables_list['result']
    
    
@app.route("/getProducts", methods=['POST'])
def getProducts():
    internal_id = request.cookies.get('int_session_id')
    path = request.cookies.get('path')
    if request.method=="POST":
        sha1=hashlib.new('sha1')
        now = datetime.now()
        date_time = now.strftime("%d/%m/%Y %H:%M:%S")
        
        sha1.update(date_time.encode('utf-8'))
        
        data = RequestProc().getRequest(request)
        
        
        json_info = {
        'jsonrpc': '2.0',
        'method': 'call',
        'params': {},
        'id': sha1.hexdigest()
        }
        
        product_resp = requests.post(f"{path}/bmsclient/getProducts", json=json_info, headers={"Cookie":f"session_id={internal_id}"})
        products_list=json.loads(product_resp.content.decode())
        
        return products_list['result']


@app.route("/getVariants", methods=['POST'])
def getVariants():
    internal_id = request.cookies.get('int_session_id')
    path = request.cookies.get('path')
    if request.method=="POST":
        sha1=hashlib.new('sha1')
        now = datetime.now()
        date_time = now.strftime("%d/%m/%Y %H:%M:%S")
        
        sha1.update(date_time.encode('utf-8'))
        
        data = RequestProc().getRequest(request)
        
        
        json_info = {
        'jsonrpc': '2.0',
        'method': 'call',
        'params': {},
        'id': sha1.hexdigest()
        }
        
        product_resp = requests.post(f"{path}/bmsclient/getVariants", json=json_info, headers={"Cookie":f"session_id={internal_id}"})
        products_list=json.loads(product_resp.content.decode())
        return products_list['result']




@app.route("/loadPOS", methods=['POST'])
def loadPOS():
    sha1=hashlib.new('sha1')
    now = datetime.now()
    date_time = now.strftime("%d/%m/%Y %H:%M:%S")
    path = request.cookies.get('path')
    sha1.update(date_time.encode('utf-8'))
    
    int_session_id = request.cookies.get('int_session_id')
    session_info=RequestProc().getSession(int_session_id, request)
    if not session_info:
        resp = make_response(render_template('login.html', basic={'title':"Sugelico 2.0"}))
        resp.set_cookie('int_session_id','',expires=0)
        resp.set_cookie('path','',expires=0)
        resp.set_cookie('dbname','',expires=0)
        resp.set_cookie('buzz_name','',expires=0)
        resp.set_cookie('session_id','',expires=0)
        return resp
        
    
    json_info = {
    'jsonrpc': '2.0',
    'method': 'call',
    'params': {},
    'id': sha1.hexdigest()
    }
    posconfig = requests.post(f"{path}/bmsclient/getPOSConfig", json=json_info,headers={"Cookie":f"session_id={int_session_id}"})
    
    pos_response= json.loads(posconfig.content.decode())
    return pos_response['result']




@app.route("/loadSession", methods=['POST'])
def loadSession():
    sha1=hashlib.new('sha1')
    now = datetime.now()
    date_time = now.strftime("%d/%m/%Y %H:%M:%S")
    path = request.cookies.get('path')
    data = RequestProc().getRequest(request)
    sha1.update(date_time.encode('utf-8'))
    
    int_session_id = request.cookies.get('int_session_id')
        
    
    json_info = {
    'jsonrpc': '2.0',
    'method': 'call',
    'params': {"sessions":data['session_ids']},
    'id': sha1.hexdigest()
    }
    possession = requests.post(f"{path}/bmsclient/getPOSSession", 
                              json=json_info,headers={"Cookie":f"session_id={int_session_id}"})
    
    pos_response= json.loads(possession.content.decode())
    return pos_response['result']





@app.route("/addOrder", methods=['POST'])
def addOrder():
    sha1=hashlib.new('sha1')
    now = datetime.now()
    date_time = now.strftime("%d/%m/%Y %H:%M:%S")
    path = request.cookies.get('path')
    print(path)
    data = RequestProc().getRequest(request)
    sha1.update(date_time.encode('utf-8'))
    
    int_session_id = request.cookies.get('int_session_id')
    
        
    
    json_info = {
    'jsonrpc': '2.0',
    'method': 'call',
    'params': data,
    'id': sha1.hexdigest()
    }
    
    order = requests.post(f"{path}/bmsclient/createPOSORDER", 
                              json=json_info,headers={"Cookie":f"session_id={int_session_id}"})
    
    order= json.loads(order.content.decode())
    return order['result']




@app.route("/getOrder", methods=['POST'])
def getOrder():
    sha1=hashlib.new('sha1')
    now = datetime.now()
    date_time = now.strftime("%d/%m/%Y %H:%M:%S")
    path = request.cookies.get('path')
    
    data = RequestProc().getRequest(request)
    sha1.update(date_time.encode('utf-8'))
    
    int_session_id = request.cookies.get('int_session_id')
    
        
    
    json_info = {
    'jsonrpc': '2.0',
    'method': 'call',
    'params': data,
    'id': sha1.hexdigest()
    }
    
    order = requests.post(f"{path}/bmsclient/getPOSOrder", 
                              json=json_info,headers={"Cookie":f"session_id={int_session_id}"})
    
    order= json.loads(order.content.decode())
    return order['result']

#app.jinja_env.globals.update(loadPOS=loadPOS)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8447, debug=True)
