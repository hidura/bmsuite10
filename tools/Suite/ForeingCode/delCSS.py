"""
Created By: hidura
On Date: Jan 25, 2011
"""
import os
import sys
from xml.dom.minidom import parseString


class delCSS:
        """This class has to save 
        the changes on the css file.
        """
        
        def __init__(self, args):
            
            document = parseString(args)
            request = document.firstChild
            
            address = request.firstChild.getElementsByTagName('element')[0]
            newdata = request.firstChild.getElementsByTagName('element')[1]
            if address.getAttribute('value')[0] != '/':
                cssfl = open(os.environ['HOME']+address.getAttribute('value'), 'r')
            else:
                cssfl = open(address.getAttribute('value'), 'r')
            cssData = cssfl.read()
            cssfl.close()
            
            dataCSS = newdata.getAttribute('value').split(',')
            
            
            
            result = ''
            cssDict = {}
            for piece in cssData.split('}'):
                if len(piece.split('{')) > 1:
                    
                    cssDict[piece.split('{')[0]] = piece.split('{')[1]
                elif piece.find("@") >= 0:
                    result += piece
            
            
            
            
                
            for key in cssDict:
                if key not in dataCSS:
                    result += key+"{"+cssDict[key]+"}"
            
            
            cssfl = open(cssfl.name, 'w')

            cssfl.write(result)
            cssfl.close()
            
            
if __name__ == "__main__":
    #Executing the savCSS class.
    delCSS(sys.stdin.read())
