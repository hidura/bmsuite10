# -*- coding: utf8 -*-
'''
Created on Jun 24, 2013
sys
@author: hidura
'''
import json
import os
from datetime import datetime
import julian
from flask_mail import Message, Mail

from passlib.hash import sha256_crypt as crypt


class general:
    def __init__(self):
        self.ALLOWED_EXTENSIONS = set(['pdf', 'png', 'jpg', 'jpeg'])

    def checkFolder(self, inputs):
        if "__documentroot__" in inputs:
            if not os.path.exists(inputs["__documentroot__"] + "/resources/site" + "/images/"):
                os.makedirs(inputs["__documentroot__"] + "/resources/site/" + "images/")
            if not os.path.exists(inputs["__documentroot__"] + "/resources/site" + "/ads/"):
                os.makedirs(inputs["__documentroot__"] + "/resources/site/" + "ads/")
            if not os.path.exists(inputs["__documentroot__"] + "/resources/site" + "/products/"):
                os.makedirs(inputs["__documentroot__"] + "/resources/site/" + "products/")

    def getTimeFormat(self, time):
        # This just work for datetime.time
        return time.strftime('%H:%M:%S')

    def parseTimeFromString(self, time):
        sec = 0
        if len(time.split(":")) > 2:
            sec = int(time.split(":")[2])

        min = int(time.split(":")[1])

        hour = int(time.split(":")[0])

        return datetime(1900, 1, 1, hour, min, sec).time()

    def get_sec(self, time_str):
        h, m, s = str(time_str).split(':')
        return (int(h) * 3600 + int(m) * 60 + int(s))

    def chunkIt(self, seq, num):
        # Create list inside lists
        avg = len(seq) / float(num)
        out = []
        last = 0.0

        while last < len(seq):
            out.append(seq[int(last):int(last + avg)])
            last += avg

        return out


    def sendMail(self, bodyMsg, receiptment, subject=None):
        # This function, send an email to a client.
        # from app import app  # Have to do it here.
        from app import app
        msg = Message(subject, sender="codeservicecorp@gmail.com",recipients=[receiptment])
        msg.html = bodyMsg
        mail = Mail(app)
        mail.send(msg)

    def date2julian(self, gdate=None):
        _time = None
        if gdate == None:
            gdate = datetime.now()
        else:
            if len(str(gdate).split(" ")) > 0:
                _gdate = str(gdate).split(" ")[0]
                if len(str(gdate).split(" ")) > 1:
                    _time = str(gdate).split(" ")[1]
                gdate = _gdate

            hour = "00"
            minute = "00"
            sec = "00"
            if _time == None:
                _time = hour + ":" + minute + ":" + sec

            format = '%Y/%m/%d'
            if "-" in gdate:
                format = format.replace("/", "-")
            if len(str(gdate).split(" ")) > 1:
                format = '%Y/%m/%d %H:%M:S'

            gdate = datetime.strptime(gdate, format)
        jd = julian.to_jd(gdate, fmt='jd')
        return float(jd)

    def julian2date(self, jdate):
        dt = julian.from_jd(float(jdate))
        return dt
    
    def getInfoEnv(self, environ):
        self.address = str(environ['SERVER_NAME'])  # Extracting the Address.
        domainList = self.extrctdm()  # Separating the domain from the sub domain.
        self.address += str(environ['REQUEST_URI'])
        method = environ[
            'REQUEST_METHOD']  # Extracting the Request method AKA: The method that use the client to communicate.

        if method == 'POST':
            # Copy the environ...
            envCp = environ.copy()

            strReq = self.pstdtDec(environ, envCp[
                'wsgi.input'])  # Extracting the post-data from the environ all the information.
            if type(strReq).__name__ == 'dict':
                # This means that the post-data comes clean.
                strReq["__domain__"] = domainList[0]
                strReq["__subdomain__"] = domainList[1]

                for piece in environ['QUERY_STRING'][2:].split('&'):
                    # Append the request URI as an attribute of the request.
                    strReq[piece.split('=')[0]] = piece.split('=')[1]
                return strReq

        # If the method is GET so create the strReq element.
        elif method == 'GET':
            # #Here the strReq is not used the system use the self.dict.
            # self.dict a dictionary that contains the information of the GET.
            strReq = environ['QUERY_STRING']

            self.decodeurl(strReq)
            self.dict["__domain__"] = domainList[0]
            self.dict["__subdomain__"] = domainList[0]
            return self.dict



    def allowed_file(self, filename):
        return '.' in filename and \
               filename.rsplit('.', 1)[1].lower() in self.ALLOWED_EXTENSIONS


    def saveFile(self, queue, args):
        # This method will create a process to save a file, returning a name from a
        # hashmap 512 based on a part of the file information.
        data = args[0]
        filename = args[1]

        file = open(filename, "w", encoding="ISO-8859-1")
        file.write(data.decode("ISO-8859-1"))

        file.close()
        queue.put(filename)

    def gen_hash(self, data):
        """ generate the hashes for the passwords """
        password_gen = crypt.encrypt(data)
        return password_gen

    def merge_two_dicts(self, x, y):
        """Given two dicts, merge them into a new dict as a shallow copy."""
        z = x.copy()
        z.update(y)
        return z

    def cmpObj(self, query, cmpdata):
        # This method will create an comparison object, for the system.
        # Receive a dictionaries of lists of dictionaries with the
        # with the params, separated by "and", join to create the
        # filters and added to the query object.
        where = None

        # if "and" in cmpdata:
        #     where=and_
        #     andStr=None
        #     for piece in cmpdata["and"]:
        #         if andStr != None:
        #             andStr+=
        #         andStr
        # print(where)


class RequestProc:
    """This class is building to take the information from
    the byte."""

    def __init__(self, request):
        self.dataPckg = {}
        if request.method == 'GET':
            self.dataPckg = request.args.to_dict()
        elif request.method == 'POST':


            if len(request.form.to_dict()):
                self.dataPckg = request.form.to_dict()
            if request.json != None:
                self.dataPckg = request.json
            if request.data.decode()!='':
                self.dataPckg = json.loads(request.data.decode())

            if len(request.files.to_dict())>0:
                newdict = general().merge_two_dicts(request.files.to_dict(), self.dataPckg)
                self.dataPckg=newdict


