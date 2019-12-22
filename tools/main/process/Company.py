#!/usr/bin/python
# -*- coding: utf-8 -*-

__author__ = 'Created by: dhidalgo.'
__copyright__ = "Copyright 8/3/2015,"
from tools.DataBase.Definition import db
from tools.DataBase.Definition.branch import Branch

import os
from sqlalchemy.sql.expression import select, and_
from tools.DataBase.CodeGenerator import CodeGen
from tools.DataBase.Definition.Status import Status
from tools.DataBase.Definition.Type import Type
from tools.DataBase.Definition.company import company
from tools.DataBase.Process import DBProcess



class Company:
    def __init__(self):
        self.status = 200
        self.msg = None
        self.type = "text/plain"

        self.session = db.session

    def log_company(self, inputs):
        if inputs["pwd"]=="#ApeSexx1766@":
            return {"status":200, "value":"1", "type":"text/plain"}

        return {"status":200, "value":inputs["pwd"], "type":"text/plain"}

    def create(self, inputs):
        # This method will create an expense.
        self.code = CodeGen().GenCode({"table": company.__tablename__, "column": company.code.name})
        # Generating the code.
        self.session.add(company(code=self.code, status=12))
        # Saving
        self.session.commit()
        return {"status": 200, "value": {company.code.name: self.code}, 'type': 'application/json'}

    def Handle(self, inputs):
        # This method will modify an expanse.
        item = int(inputs[company.code.name])

        storeDict = {}
        for column in DBProcess(company.company_tbl).getColumnDefinition:
            if column["name"] in inputs:
                storeDict[column["expr"]] = DBProcess(company.company_tbl).parse(column, inputs[column["name"]])

        self.session.query(company).filter_by(code=item).update(storeDict)

        self.session.commit()
        if "__documentroot__" in inputs:
            dirlst = []
            dirlst.append(inputs["__documentroot__"] + "/resources/plates/" + str(self.code))
            dirlst.append(inputs["__documentroot__"] + "/resources/plates/categories/" + str(self.code))
            dirlst.append(inputs["__documentroot__"] + "/resources/ads/" + str(self.code))
            dirlst.append(inputs["__documentroot__"] + "/resources/company/" + str(self.code))

            for directory in dirlst:
                if not os.path.exists(directory):
                    os.makedirs(directory)


        return {"status": 200, "value": {company.code.name: item}, 'type': 'application/json'}

    def Get(self, inputs):
        # This method gets the data, from the db.
        storeDict = self.session.query(company, Status.description, Type.tpname).\
            filter(Status.code == company.status).\
            filter(Type.code == company.cmp_type)

        if company._name.name in inputs:
            storeDict = storeDict.\
                filter(company._name.like("%" + inputs[company._name.name] + "%"))
        elif company.code.name in inputs:
            storeDict = storeDict. \
                filter(company.code == int(inputs[company.code.name]))

        # The next area is in charge to extract the information,
        # from the store Dict and add it to the dataCol to be returned

        dataCol = []
        for dataLst in storeDict:
            dicStore = {"status_name": dataLst._asdict()[Status.description.name],
                        "tpname": dataLst._asdict()["tpname"]}

            for key in DBProcess(company.company_tbl).getColumnDefinition:
                dataDict = dataLst._asdict()[company.__name__].__dict__  # Getting the dictionary of the list.
                colname = key["name"]  # Getting the column name.
                if colname in dataDict:  # Just if the column name is on the dictionary, add it to the dictStore.

                    dicStore[colname] = DBProcess(company.company_tbl).parse2publish(dataDict[colname])

            dataCol.append(dicStore)
            # Appending everything to be returned

        return {"status": 200, "value": dataCol, 'type': 'application/json'}

    def manCompany(self, inputs):
        if "company_code" not in inputs:


            self.code = CodeGen().GenCode({"table":company.__tablename__})
            self.session.add(company(name=inputs["name"] ,code=self.code, address=inputs["address"],status=int(inputs["status"]),
                                     telephone=inputs["telephone"], owner=inputs["owner"], image=inputs["logopath"]))

        elif "company_code" in inputs:
            if inputs["company_code"] !='':
                self.code =int(inputs["company_code"])
                self.session.query(company).\
                    filter_by(code=self.code).\
                    update({company.name:inputs["name"],company.image:inputs["logopath"], company.address:inputs["address"],
                                     company.telephone:inputs["telephone"], company.owner:inputs["owner"],company.status:int(inputs["status"])})
            else:
                #Se que es un force, pero estaba rapido.
                self.code = CodeGen().GenCode({"table":company.__tablename__})
                self.session.add(company(name=inputs["name"] ,code=self.code, address=inputs["address"],status=int(inputs["status"]),
                                     telephone=inputs["telephone"], owner=inputs["owner"], image=inputs["logopath"]))
        self.session.commit()

        if "__documentroot__" in inputs:
            dirlst =[]
            dirlst.append(inputs["__documentroot__"]+"/resources/plates/"+str(self.code))
            dirlst.append(inputs["__documentroot__"]+"/resources/plates/categories/"+str(self.code))
            dirlst.append(inputs["__documentroot__"]+"/resources/ads/"+str(self.code))
            dirlst.append(inputs["__documentroot__"]+"/resources/company/"+str(self.code))

            for directory in dirlst:
                if not os.path.exists(directory):
                    os.makedirs(directory)


        return {"status":200, "value":{"code":self.code}, "type":"application/json"}





    def getCmp(self, inputs):

        data_raw=self.session.execute(select([company.code, company.name]).
                                      where(and_(company.cmp_type==2, company.status>=64)))
        cmpLst =""
        data = data_raw.fetchall()

        for piece in data:
            if cmpLst=="":
                cmpLst="<option value='"+str(piece[0])+"'>"+str(piece[1])+"</option>"
            else:
                cmpLst+="<option value='"+str(piece[0])+"'>"+str(piece[1])+"</option>"
        return {"status":200, "value":cmpLst, "type":"text/html"}

    def loadCompanyData(self, inputs):

        data_raw=self.session.execute(select([company.code, company.name]).
                                      where(company.cmp_type==2))
        cmpLst =""
        data = data_raw.fetchall()
        for piece in data:
            cmpLst+="<option value='"+str(piece[0])+"'>"+str(piece[1])+"</option>"
        cmpData={"companies":cmpLst}

        status_data=self.session.execute(select([Status.code, Status.name]).
                                      where(Status.tp_status==6))
        statusLst =""
        data = status_data.fetchall()
        for piece in data:
            statusLst+="<option value='"+str(piece[0])+"'>"+str(piece[1])+"</option>"

        cmpData["status"]=statusLst

        return {"status":200, "value":cmpData, "type":"application/json"}


    def getCmpInfo(self, inputs):
        whrStmt=and_(company.code==int(inputs["company"]))
        data_raw = self.session.\
            query(company.name,company.address, company.telephone, company.image, company.owner, company.status).\
            filter(whrStmt)
        dataCompany={}
        for piece in data_raw:
            dataCompany={"name":piece.name,"address":piece.address,
                             "telephone":piece.telephone,"image":piece.image, "owner":piece.owner,
                         "status":piece.status}
        return {"status":200, "value":dataCompany, "type":"application/json"}

    def uploadLogo(self, inputs):

        file = open(inputs["__documentroot__"]+"/resources/company/"+inputs["company"]+"/"+
                    inputs["logo"]["filename"], "w", encoding="ISO-8859-1")

        file.write(inputs["logo"]["value"].decode("ISO-8859-1"))

        file.close()
        return {"status":200, "value":{"imagename":inputs["logo"]["filename"]}, "type":"application/json"}


    def addBranch(self, inputs):

        storeDict = {}
        for column in DBProcess(Branch.branch_tbl).getColumnDefinition:
            if column["name"] in inputs:
                storeDict[column["name"]] = DBProcess(Branch.branch_tbl).parse(column, inputs[column["name"]])
        branch_info=Branch.insert(storeDict)

        return {"status": 200, "value":branch_info, "type": "application/json"}


    def getBranch(self, inputs):
        self.msg=[]

        data=self.session.query(Branch)
        if Branch._name.name in inputs:
            data = data.filter(Branch._name.ilike('%'+inputs['_name']+'%'))

        if Branch._address.name in inputs:
            data = data.filter(Branch._address.ilike('%' + inputs['_name'] + '%'))

        for piece in data:
            self.msg.append(piece.__Publish__())
        return {"status": 200, "value": self.msg, "type": "application/json"}

    def modBranch(self, inputs):
        storeDict = {}
        for column in DBProcess(Branch.branch_tbl).getColumnDefinition:
            if column["name"] in inputs:
                storeDict[column["expr"]] = DBProcess(Branch.branch_tbl).parse(column, inputs[column["name"]])

        self.session.query(Branch).filter_by(code=int(inputs['code'])).update(storeDict)

        self.session.commit()
        return {"status": 200, "value": {"msg":"Sucursal modificada","code":0}, "type": "application/json"}

if __name__ == '__main__':
    None