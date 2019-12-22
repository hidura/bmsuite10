# -*- coding: utf-8 -*-
'''
Created By: hidura
On Date: Jul 4, 2010
'''

# Import area
from hashlib import sha1
import cgi
import json
from http.cookies import SimpleCookie
from urllib.parse import unquote_plus
from tools.Utilities.Errors.Errors import error
from .ProcPost import pproc


class buildRq:
    def pstdtDec(self, environ, data):
        """
        This method returns a complete
        string request that will be send into
        the system."""
        rawData = data.read()

        if '<element ' in str(rawData):
            """
            Antes de devolver esta mierda
            pasarlo por StringIO y en la primera
            quitarle el '>' y agregarle el path y el method
            y volver a colocarle el '>'
            """
            return rawData.decode()
        elif str(rawData) != '':
            return pproc(environ, rawData).sendResult()
        else:
            error("Problems with the environ- Not found request")

    def decodeurl(self, data):
        """This method will
        decode the arguments."""
        self.dict = {}
        for piece in data.split('&'):
            if piece.find('=') > -1:
                pos = int(piece.find('='))
                self.dict[piece[0:(pos)]] = unquote_plus(piece[(pos + 1):len(piece)])

    def extrctdm(self):
        """In this method the domain is divide in
        all 2 pieces the sub-domain and the domain."""
        # Extracting the domain and the sub domains names
        pathlen = len(self.address) - 1
        dots = 0  # This represents the amount of dot '.' what the system has seems.
        tmpcol = ''  # This variable it's the temporal collector of characters.
        sbdomainList = []  # The sub domain list
        while (pathlen >= 0):
            """This code must not be modified."""
            # In the time that this loop is executing for event point the
            # loop will append the string collected to a list.
            if self.address[pathlen] == '.':
                if dots == 0:
                    # If the dots is 0 create the tmpcol
                    dots += 1
                    tmpcol = self.address[pathlen] + tmpcol
                else:
                    # Otherwise append to the subdomain list a tmpcol.
                    sbdomainList.append(tmpcol)
                    # Clean the tmpcol var.
                    tmpcol = ''
            else:
                # Collecting the character. in the
                tmpcol = self.address[pathlen] + tmpcol
            # Reducing one.
            pathlen -= 1

        if len(sbdomainList) == 0:
            # Adding the sub-domain to the list
            sbdomainList.append(tmpcol)
            # And the www as the index.
            sbdomainList.append("www")
        else:
            # Otherwise append the list to the variable.
            sbdomainList.append(tmpcol)
        # Adding to the domain list the sub-domain.
        domainList = [sbdomainList[0]]
        subdomain = ""
        for piece in sbdomainList:
            if piece != sbdomainList[0]:
                subdomain += piece + '.'
        domainList.append((subdomain[:len(subdomain) - 1]))
        return domainList

    def extractVal(self, field, cgi_field):
        if cgi_field.filename != None:
            # Go to the save file.
            fileExt = str(cgi_field.filename).split(".")[len(str(cgi_field.filename).split(".")) - 1]
            newName = sha1(cgi_field.filename.encode()).hexdigest() + "." + fileExt
            value = {"filename": newName, "value": cgi_field.value}
            self.dict[field] = value
        else:
            value = cgi_field.value
            if field in self.dict:
                value_lst = self.dict[field]
                if type(value_lst).__name__ == 'list':
                    value_lst.append(value)
                else:
                    self.dict[field] = [value_lst, value]
            else:
                self.dict[field] = value

    def extrctEnv(self, environ, location):
        """This is the method that extract
        all the data from the environ."""
        method = environ[
            'REQUEST_METHOD']  # Extracting the Request method AKA: The method that use the client to communicate.
        self.dict = {}
        if str(method) == "POST":
            # Copy the environ...
            post_env = environ.copy()
            query_string = post_env['QUERY_STRING']
            post_env['QUERY_STRING'] = ''
            env_cp = environ.copy()
            content_type = env_cp["CONTENT_TYPE"]
            data = None
            if "multipart" in content_type:
                data = environ["wsgi.input"]
                post = cgi.FieldStorage(
                    fp=data,
                    environ=post_env,
                    keep_blank_values=True
                )
                for field in post.keys():
                    value = None
                    cgi_field = post[field]
                    if type(cgi_field).__name__ == 'list':
                        for piece in cgi_field:
                            self.extractVal(field, piece)
                    else:
                        self.extractVal(field, cgi_field)

            elif "false" in content_type or "json" in content_type:
                data = environ["wsgi.input"].read().decode("ISO-8859-1")
                self.dict = json.loads(data)
            elif "text/plain;charset=UTF-8" in content_type:
                data = environ["wsgi.input"].read().decode("ISO-8859-1")

                for query in data.split("&"):
                    self.dict[query.split("=")[0]] = unquote_plus(query.split("=")[1])
            elif "application/x-www-form-urlencoded" in content_type:
                data = environ["wsgi.input"].read().decode("ISO-8859-1")
                for query in data.split("&"):
                    self.dict[query.split("=")[0]] = unquote_plus(query.split("=")[1])

                    # raise Exception(str(self.dict+","+content_type))



                    # strReq = self.pstdtDec(environ, envCp['wsgi.input'])  # Extracting the post-data from the environ all the information.
                    # return strReq
                    #
                    # if type(strReq).__name__ == 'dict':
                    #     # If the result is a dictionary, then add the query string on the environ if there's any.
                    #     queryString = environ['QUERY_STRING']
                    #     if queryString.find("=") > 0:
                    #         for query in queryString.split("&"):
                    #             strReq[query.split("=")[0]] = query.split("=")[1]
                    #
                    #     return strReq
                    #
        # If the method is GET so create the strReq element.
        elif str(method).upper() == 'GET':
            # #Here the strReq is not used the system use the self.dict.
            # self.dict a dictionary that contains the information of the GET.
            strReq = environ['QUERY_STRING']

            self.decodeurl(strReq)

            # if len(self.dict)==0:
            #     if environ["REQUEST_URI"] !='/':
            #         self.dict["md"]=environ["REQUEST_URI"]
            #     else:
            #         #Send the not found page
            #         self.dict["md"]="not_found.html"


            # if 'md' not in self.dict and "code" not in self.dict:
            #     self.dict['md'] = 'index'
            if len(self.dict) == 0:
                self.dict["md"] = "login"

        if "HTTP_COOKIE" in environ:
            cookie = SimpleCookie()
            cookie.load(environ['HTTP_COOKIE'])

            # self.dict["key"]= cookie['loginkey'].value
            for __cookie__ in cookie:
                if "loginkey" == __cookie__:
                    self.dict["key"] = cookie[__cookie__].value
                else:
                    self.dict[__cookie__] = cookie[__cookie__].value

        # classname = ""
        # if "classname" in self.dict:
        #     classname = self.dict["classname"]
        #
        # if "key" not in self.dict and classname != "login.LoginSys":
        #     #If there's no key and the classname is not login.LoginSys, send back to the login.
        #     self.dict={"md":"login"}

        return self.dict
