# -*- coding: utf-8 -*-
'''
Created on Jan 11, 2010

@author: hidura
'''
#Import Area
import sys


def application(environ, start_response):
    
    status = '200 OK'
    
    
    ##Importing the Python Apps
    sys.path.append("/etc/medSys/")
    from tools.loadKar import core
    
    response = core(environ)#Here the assistant takes the parameters and begins the work
    
    responseData = response.result()#Here obtaining the result of the assistant
    
    
    if type(responseData).__name__ == 'list':
        Ctype = 'text/'+responseData[0]
        responseData = responseData[1]
    else:
        Ctype = 'text/html'
        
    responseData = responseData.encode('utf8')

    
    response_headers = [('Content-type', Ctype+"; charset=utf-8"),
                        ('Content-Length', str(len(responseData)))]#Creating the Header of the data
    
    start_response(status, response_headers)#Sending the Header of the data
    return [responseData]#Returning the data to the web page.
    
