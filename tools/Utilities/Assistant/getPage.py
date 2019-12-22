#!/usr/local/bin/python3
# -*- coding: latin-1 -*-

'''
Created on Jul 17, 2013

@author: hidura

'''
import os
from bs4 import BeautifulSoup
import re

from sqlalchemy.sql.expression import select

from tools.DataBase.ODM.DataModelODM import Group_module
from tools.main.process.Clients import Client
from tools.main.process.login import login


class getNewPage:
    def_path="/resources/site/"#Future hard path.
    def setData(self):
        # This method add the data to that is open.
        if self.fileType == "html":
            soup = BeautifulSoup(self.dataFile)
            general_status = False# This is the status of if the general.js is present.

            #Ger all scripts
            for script in soup.find_all("script"):
                if script.has_attr("src"):
                    src = script["src"]
                    if "http://" not in src:
                        if "general.js" in src:
                            general_status = True
                        script["src"] = self.def_path+src

            if not general_status:
                generalJS = soup.new_tag("script")
                generalJS["type"] = "text/javascript"
                generalJS["src"] = self.def_path+"js/general.js"
                soup.find_all("head").append(generalJS)

            #Ger all link
            for link in soup.find_all("link"):
                if link.has_attr("href"):
                    src =link["href"]
                    if "http://" not in src:
                        link["href"]=self.def_path+src

            #Ger all images
            for img in soup.find_all("img"):
                if img.has_attr("src"):
                    src =img["src"]
                    img["src"]=self.def_path+src

            process = soup.find_all('process')
            ClsPckg = [Client]
            for proc in process:
                if proc.has_attr('value') == True:
                    for pieceCls in ClsPckg:
                        for piece in dir(pieceCls):
                            if piece == proc.attrs['value']:
                                mainFnc = pieceCls()
                                retVal=getattr(mainFnc, proc.attrs['value'])(soup, self.inputs, self.environ)

                    #executeCode(proc.attrs['value'], proc.parent, soup, self.input)
                proc.extract()

            self.setDefault(soup)

            if soup.find('html')!=None:
                self.dataFile = soup.find('html').prettify()
            else:
                self.dataFile = soup.prettify()
    
    def __init__(self, path, inputs, environ):
        self.inputs = inputs
        self.environ = environ

        self.dataFile = ""
        pattern = re.compile('\\W')
        self.target=""
        self.fileType=""

        if pattern.search(path)!= None:
            self.target=path
            if len(path.split("."))>1:
                self.fileType = path.split(".")[1]
        else:
            #The only thing that can have the path to the page is a dot '.' or a interrogation sign '?'
            #Now cleaning all.
            self.target = path.split("?")[0]
            self.target = self.target.split(".")[0]
            self.target = self.target+".html"#For default is a webpage.
            self.fileType="html"
        mainPath = environ["DOCUMENT_ROOT"] + self.def_path
        with open(mainPath + self.target, "r", encoding="ISO-8859-1") as file:
            self.dataFile = str(file.read())
        self.setData()
        file.close()
    
    def getResult(self):
        return self.dataFile

    def setDefault(self, codeHTML):
        if codeHTML.find("title")!=None:
            codeHTML.find("title").string="Sugelico Panel"
        sideBar = codeHTML.find(id="principal_menu")
        menu_lst = codeHTML.find(id="modules_section")

        menu=""
        name=""

        if "key" in self.inputs:
            key = login().decLoginKey(self.inputs["key"])
            if key != None:
                menuStr = login().getuserGroupModule(self.inputs)["value"]
                menuStr += "<a href='#' class='dropdown-item close_session' " \
                           "onClick='logout(this); return false;'>Cerrar Sesión</a>"
                menu = BeautifulSoup(menuStr)

                profile = login().getProfile(self.inputs)["value"]
                name=profile["name"]
                name_area = codeHTML.find(id="dropdownMenuButton")
                if name_area != None:
                    dataCol = login().getProfile(self.inputs)
                    name_area.string = str(dataCol["value"]["name"])
                if menu_lst!=None:
                    menu_lst.\
                        append(BeautifulSoup(login().getuserModule(self.inputs)["value"]))# Adding the group of Modules
                if codeHTML.find(id="module_name") != None and "group" in self.inputs:
                    group_info = Group_module.objects(code=int(self.inputs["group"]), status=11).first()
                    codeHTML.find(id="module_name")["style"]="width:100%;text-decoration: underline;"
                    codeHTML.find(id="module_name").string = group_info.name
        if sideBar != None:
            sideBar.append(menu)



            
        ##Looking for new messages
        msg_amount=codeHTML.find(id="msg_amount")
        if msg_amount!=None:
            msg_amount.string = "0"
        dropdownmenu = codeHTML.find(id="dropmenu")
        if dropdownmenu != None:
            dropdownmenu.string = """<li><a href="#">Editar perfil<i class="pull-right icon-pencil"></i></a></li>
                            <li><a href="#">Cuenta<i class="pull-right icon-usd"></i></a></li>
                            <li><a href="#">Ayuda<i class="pull-right icon-question-sign"></i></a></li>
                            <li><a href="#">Tour<i class="pull-right icon-info-sign"></i></a></li>
                            <li class="divider"></li>
                            <li><a href="#" class="text-right">Salir del sistema</a></li>"""
                            
                            
        title_lst = codeHTML.find_all("title")
        for title in title_lst:
            if "-" in title.string:
                pageTitle = title.string.split("-")[1]
                title = codeHTML.find(id="panelPage")
                if title != None:
                    title.string = pageTitle
                subtitle = codeHTML.find(id="subtitle")
                if subtitle != None:
                    subtitle.string = pageTitle
