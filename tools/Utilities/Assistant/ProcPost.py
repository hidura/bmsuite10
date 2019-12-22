# -*- coding: utf-8 -*-
'''
Created By: hidura
On Date: Oct 13, 2010
'''
import cgi

import io
import json
from multiprocessing import Process, Queue
import os
import urllib.parse
from urllib.parse import unquote


class pproc:
    """This class is building to take the information from
    the byte."""
    
    def __init__(self, environ, wsginp):
        self.formDict = {}  # Creating the Form dictionary that will content all the fields names and the values!

        if(environ['CONTENT_TYPE'] != None and str(environ['CONTENT_TYPE']).find(";")>=0):
            boundary = environ['CONTENT_TYPE'].split(';')[1].split('=')[1]  # Extracting the number of the mime.
        self.location = environ['DOCUMENT_ROOT'] + '/tmp/'
        if (str(wsginp).find("Content-Disposition: form-data") < 0):
            dataCol = unquote(wsginp.decode("utf-8"))
            if dataCol[0] =="{" and dataCol[len(dataCol)-1] == "}" or str(environ['CONTENT_TYPE']) =="application/json":
                #This is the case that the receive is JSON.
                self.formDict = json.loads(dataCol)
            else:
                for input in dataCol.split("&"):
                    if (input.split("=")[1] != ""):
                        self.formDict[input.split("=")[0]] = input.split("=")[1].replace("+", " ")
            
        else:
            input = str(wsginp)[1:].strip("''").replace('\\n', '\n')  # Transforming the byte into a string, eliminating the 'b', striping the quotes and replacing the \\n for \n
            dataSplit = input.split(boundary)  # Separating by the input by the boundary
            for piece in dataSplit:
                # Using the multiprocessing of Python to extract the data
                q = Queue()
                p = Process(target=self.dataProc, args=(q, piece))
                p.start()
                data = q.get()
                if len(data) == 2:
                    self.formDict[data[0]] = data[1]
                p.join()

    def dataProc(self, queue, field):
        """This method has to extract the information 
        from the field and inserted inside the formDict.
        If is a file it will be saved to!"""
        
        dataSpl = field[:200].split('\n')[0:3]  # Extracting the header fields
        
        flStart = 1  # This will be the variable that store the initial point of the file.
        file = None  # This will indicate if in the field is a file.
        binar = None  # This will indicates if is binary or text.
        formList = []
        if len(dataSpl) == 3:
            for info in dataSpl[1].split(';'):
                # Separating the data by the ;
                if 'name' in info.split("=")[0] and 'filename' not in info.split("=")[0]:
                    # If name is in the info that is the fieldNM 
                    fieldNm = info.split("=")[1].strip('""')
                    if '"\\r' in fieldNm:
                        # Cleaning the name
                        fieldNm = fieldNm[:-3]
                if 'filename' in info.split("=")[0]:
                    # If is the filename is a file!
                    if type(info.split("=")[1:]).__name__ == 'list':
                        fileNm = ''
                        for partNM in info.split("=")[1:]:
                            if '"\\r' in partNM:
                                # Cleaning the name of the file.
                                partNM = partNM[:-3]
                            # Collecting the fileNm
                            fileNm += partNM.strip('""')
                    else:
                        # Otherwise the fileNm will be the first position on the list in this split.
                        fileNm = info.split("=")[1]
                    # Appending the file field Name to the formList
                    formList.append(fieldNm)
                    # Doing thr same with the file name.
                    formList.append(self.location + fileNm)
                    # Extracting the file type information.
                    flTpInf = dataSpl[2].split(":")[1].split('/')
                    # If text is not on the file type information that means this is a binary file.
                    if 'text' not in flTpInf[0]:
                        # Making binary true
                        binar = True
                        # And creating the file.
                        file = open(self.location + fileNm, 'wb')
                    else:
                        # Otherwise create the file as a text file.
                        file = open(self.location + fileNm, 'w')
            # Is totally necessary that the file has information not a nonetype. 
            if file != None:
                # Here is saving the file!
                part = ''
                # The part is the string that collect the data.
                for piece in dataSpl:
                    # Collecting the data piece by piece.
                    part += field[:field.find(piece) + len(piece)]
                # Now to concrete the saving of the file.
                if binar == True:
                    # This part is for the binary.
                    tmpData = field[field.find(piece) + len(piece):]
                    tmpData = tmpData[4:]  # These represent the 4 first strings \r\n
                    tmpData = tmpData.replace('\r', '\\r')
                    newData = tmpData.replace('\n', '\\n')
                    dataFile = "b'" + newData[:-6] + "'"
                    file.write(eval(dataFile))
                else:
                    # Otherwise save the files as a text.
                    flStart += (len(dataSpl[1]) + len(dataSpl[2]) + 7)
                    data = field[flStart:-1]
                    newData = ''
                    data = data.replace("\\'", "'")
                    for piece in data.split('\\r'):
                        newData += piece.replace('\\t', '\t').expandtabs()
                    file.write(newData[:-2])
                    
                # Close the file.
                file.close()
            else:
                # This part if for extract the data from the fields not from the file.
                part = ''
                # The same thing collecting the data as a string.
                for piece in dataSpl:
                    
                    part += field[:field.find(piece) + len(piece)]
                # Save the same as a newData.
                newData = field[field.find(piece) + len(piece):]
                
                flStart += (len(dataSpl[1]) + len(dataSpl[2]) + 4)
                
                formList.append(fieldNm)
                
                formList.append(field[flStart:-5])
        
        return queue.put(formList)
            
    def sendResult(self):
        """Returning the reuslts!"""
        return (self.formDict)
