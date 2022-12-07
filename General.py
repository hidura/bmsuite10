from datetime import datetime
import hashlib
from email.utils import parsedate
import os
import json

import xmlrpc.client
import requests


main_server ="http://bmsuite.oikoschain.com:2462"

class general:
   
    
    def allowed_file(self,filename):
        ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
        return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


class Odoo:

    def __init__(self):

        with open(os.path.dirname(os.path.abspath(__file__)) + "/credentials.json") as f:
            info = json.loads(f.read())

        self.loconnection = xmlrpc.client.ServerProxy("{}/xmlrpc/2/common".format(info['odoo']['host']))

        self.lourl, self.lodb, self.lousername, self.lopassword = \
            info['odoo']['host'], info['odoo']['db'], info['odoo']['user'], info['odoo']['password']
        self.uid = self.loconnection.authenticate(self.lodb, self.lousername, self.lopassword, {})
        self.lo_models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(self.lourl))

        connection_cred = {"lourl": self.lourl, "lodb": self.lodb,
                        "lousername": self.lousername, "lopassword": self.lopassword, 
                        "lo_models": self.lo_models,
                        "louid": self.uid
                        }

        


    def search(self, table_name, domain, type):
        """
        Params:
            table_name: That's the name of the table that's going to be read.
            domain: the parameters that will be passed to read the table.
            type: Could be search, read or search_read.
        """
        return self.lo_models.execute_kw(self.lodb, self.uid, self.lopassword, 
        table_name, type, [domain])


    def create(self, table_name,information):
        """
        Params:
            table_name: That's the name of the table that's going to be read.
            information: The information that will be stored on the server.
        """
        return self.lo_models.execute_kw(self.lodb, self.uid, self.lopassword, 
        table_name, "create", [information])


class RequestProc:
    """This class is building to take the information from
    the byte."""
    def merge_two_dicts(self, x, y):
        """Given two dicts, merge them into a new dict as a shallow copy."""
        z = x.copy()
        z.update(y)
        return z


    def __init__(self):
        self.dataPckg = {}
    
    
    def getRequest(self,request):
        if request.method == 'GET':
            dataPckg = request.args.to_dict()
            return dataPckg
        elif request.method == 'POST':
            
            if len(request.form.to_dict()):
                dataPckg = request.form.to_dict()
                return dataPckg
            if request.json != None:
                dataPckg = request.json
                return dataPckg
            if request.data.decode()!='':
                dataPckg = json.loads(request.data.decode())
                return dataPckg
            if len(request.files.to_dict())>0:
                newdict = self.merge_two_dicts(request.files.to_dict(), self.dataPckg)
                dataPckg=newdict
                return dataPckg
    
    def getSession(self,session_id,request):
        #This method will check if the session is not expired, if
        #it's will return the session, if not will return a false.
        path = request.cookies.get('path')
        sha1=hashlib.new('sha1')
        date_time = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        sha1.update(date_time.encode('utf-8'))
        
        json_info = {
        'jsonrpc': '2.0',
        'method': 'call',
        'params': {},
        'id': sha1.hexdigest()
        }
        
        check_session = requests.post(f"{path}/web/session/check", json=json_info,
                                      headers={"Cookie":f"session_id={session_id}"})
        session_resp = json.loads(check_session.content.decode())
        if "error" in session_resp:
            #If there's something wrong with the session_id, eliminate all the cookies in the system
            #And return false
            return False
        
        return session_resp