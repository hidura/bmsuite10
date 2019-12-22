
from datetime import datetime
import os
import shlex
from subprocess import Popen
import subprocess
import sys
from xml.dom.minidom import parseString


class core:
    
    def urldec(self):
        url = self.environ['SERVER_NAME'].split('.')
        if len(url) > 2:
            url = self.environ['SERVER_NAME']
            
            domainSpl = url.split('.')
            
            domainSpl.reverse()
            domain = ""
            dmlst = []
            cont = 0
            if len(domainSpl)>3:
                    while cont < 3:
                            if (cont == 2):
                                    dmlst.append(domain[:-1])
                            domain = domainSpl[cont]+"."+domain
                            cont += 1
            
                    dmlst.append(domain[:-1])
            else:
                    while cont <= 2:
                            domain = domainSpl[cont]+"."+domain
                            if (cont == 1):
                                    dmlst.append(domain[:-1])
                            cont += 1
            
                    dmlst.append(domain[:-1])

            return(dmlst)

        else:
            return [self.environ['SERVER_NAME']]
            
        
    
    
    
    
    def __init__(self, environ = None, location = None):
        self.response = None
        
        if environ == None and location == None:
            #If the environ and the location are None, no make anything.
            self.response = """<h1>Petition doesn't have <u>Environ</u> or <u>Location</u></h1>"""
        
        elif environ != None:
            
            self.environ = environ
            
            
            
            from tools.Utilities import buildRq
            buildReq = buildRq()
            from tools.main import main
            request = buildReq.extrctEnv(environ, environ['DOCUMENT_ROOT'])

            # try:
            #     self.response = main(request, environ).getResult()
            # except Exception as ex:
            #     error = {"error": str(ex.args[0])}
            #     self.response = {"status": 200, "value": error, "type": "application/json"}
            self.response = main(request, environ).getResult()
                
                
    
    def result(self):
        if self.response != None:
            
            return self.response
        else:
            
            return ["plain", "Problem with the communication with the core..."]
        
        
        
    def logs(self, logData):
        logdir = os.listdir(self.environ['DOCUMENT_ROOT']+'logs/')
        a = datetime.now()
        logtime = ''
        for piece in a.timetuple()[:3]:
            logtime += str(piece)+'-'
        logtime = logtime[:-1]+" "
        
        for piece in a.timetuple()[3:]:
            logtime += str(piece)+':'
        
        logtime = logtime[:-3]
        
        if len(logdir) < 1:
            log = open(self.environ['DOCUMENT_ROOT']+'logs/error.log', 'w')
            for piece in str(logData).split('\n'):
                log.write('['+logtime+']'+str(piece)+'\n')
            log.close()
        else:
            log = open(self.environ['DOCUMENT_ROOT']+'logs/error.log', 'r')
            if len(log.readlines()) > 500:
                self.cleanLogs(self.environ['DOCUMENT_ROOT']+'logs')
                log = open(self.environ['DOCUMENT_ROOT']+'logs/error.log', 'w')
            else:
                log = open(self.environ['DOCUMENT_ROOT']+'logs/error.log', 'a')
            for piece in str(logData).split('\n'):
                log.write('['+logtime+']'+str(piece)+'\n')
            log.close()
         
        
        return str(logData)
    
    def cleanLogs(self, location):
        
        logfiles = os.listdir(location)
        if len(logfiles) == 9:
            os.remove(logfiles[-1])
            logfiles = logfiles[:-1]
            cont = 1
            for log in logfiles:
                os.rename(self.environ['DOCUMENT_ROOT']+'logs/'+log, self.environ['DOCUMENT_ROOT']+'logs/error_'+str(cont)+'.log')
        else:
            cont = 1
            for log in logfiles:
                os.rename(self.environ['DOCUMENT_ROOT']+'logs/'+log, self.environ['DOCUMENT_ROOT']+'logs/error_'+str(cont)+'.log')
