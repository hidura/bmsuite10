"""
Created By: hidura
On Date: Jan 25, 2011
"""
import os
import sys
from xml.dom.minidom import parseString


class savCSS:
        """This class has to save 
        the changes on the css file.
        """
        
        def __init__(self, args):
            
            document = parseString(args)
            request = document.firstChild
            
            address = request.firstChild.getElementsByTagName('element')[0]
            newdata = request.firstChild.getElementsByTagName('element')[1]
            cssfl = None
            if address.getAttribute('value')[0] != '/':
                cssfl = open(os.environ['HOME']+address.getAttribute('value'), 'r')
            else:
                cssfl = open(address.getAttribute('value'), 'r')
            
            
            if cssfl != None:
                cssData = cssfl.read()
                cssfl.close()
                
                dataCSS = ''
                for child in newdata.childNodes:
                    if child.nodeType == 3:
                        dataCSS += child.nodeValue
                    
                ###Making split to the data from the web page.
                nwcssDict = {}
                keyLst = []
                for piece in dataCSS.split('}'):
                    if len(piece.split('{')) > 1:
                        keyLst.append(piece.split('{')[0])
                        nwcssDict[piece.split('{')[0]] = piece.split('{')[1]
                
                result = ''
                cssDict = {}
                if cssData.find('\n') < 0:
                    if piece.find("@") >= 0:
                            for sbPiece in piece.split(";"):
                                if len(sbPiece)>0: 
                                    if sbPiece[0] == '@':
                                        result += sbPiece+';\n'
                    else:
                        for piece in cssData.split('}'):
                            if len(piece.split('{')) > 1:
                                if 'undefined' not in piece.split('{')[1]:
                                    cssDict[piece.split('{')[0]] = piece.split('{')[1]
                else:
                    for piece in cssData.split('\n'):
                        if "{" not in piece: 
                            for sbPiece in piece.split(";"):
                                    if len(sbPiece)>0: 
                                        if sbPiece[0] == '@':
                                            result += sbPiece+';\n'
                                    
                        else:
                            for sbPiece in piece.split("}"):
                                if len(sbPiece.split('{')) > 1:
                                    cssDict[sbPiece.split('{')[0]] = sbPiece.split('{')[1]
                cssfl = open(cssfl.name, 'w')
                cssfl.write(result)
                cssfl.close()
                
                cssfl = open(cssfl.name, 'a')
                result = ''
                for key in nwcssDict:
                    result += key+"{"+nwcssDict[key]+"}"
                
                
                
                    
                for key in cssDict:
                    if key not in nwcssDict:
                        result += key+"{"+cssDict[key]+"}"
                
                cssfl.write(result)
                cssfl.close()
                
                
                
                
                
                
            
            
if __name__ == "__main__":
    #Executing the savCSS class.
    savCSS(sys.stdin.read())
