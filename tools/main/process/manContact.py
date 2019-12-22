# -*- coding: utf8 -*-
'''
Created on Jan 28, 2014

@author: hidura
'''
from sqlalchemy.sql.expression import select, and_
from tools.DataBase.CodeGenerator import CodeGen
from tools.DataBase.Connect import conection
from sqlalchemy.orm import sessionmaker

from tools.DataBase.Definition import db
from tools.DataBase.Definition.Contact import Contact
from tools.DataBase.Definition.Status import Status
from tools.DataBase.Process import DBProcess
from tools.main.general import general


class ManContact:

    def __init__(self):

        self.status = 200
        self.msg = None
        self.type = "text/plain"

        self.session = db.session

    def Get(self, inputs):
        dataCol=[]
        """The module of find the information of a Contact."""
        dataPack =[]
        if Contact.contact_name.name in inputs:
            dataPack = self.session.query(Contact, Status.description).\
                filter(and_(Contact.contact_name.like("%"+inputs[Contact.contact_name.name]+"%"), Contact.status==Status.code))

        elif Contact.code.name in inputs:
            dataPack = self.session.query(Contact, Status.description).\
                filter(and_(Contact.code == int(inputs[Contact.code.name]), Contact.status==Status.code))

        for dataLst in dataPack:
            dicStore = {"status_name": dataLst._asdict()[Status.description.name]}

            for key in DBProcess(Contact.Contact_tbl).getColumnDefinition:
                dataDict = dataLst._asdict()[Contact.__name__].__dict__  # Getting the dictionary of the list.
                colname = key["name"]  # Getting the column name.
                if colname in dataDict:  # Just if the column name is on the dictionary, add it to the dictStore.
                    value =DBProcess(Contact.Contact_tbl).parse2publish(dataDict[colname])

                    if colname == "birthdate":
                        value = general().julian2date(str(dataDict[colname]))

                    dicStore[colname] = value

            dataCol.append(dicStore)
            # Appending everything to be returned

        return {"status":200, "value":dataCol, 'type':'application/json'}

    def create(self, inputs):
        # Create a new ID for the contact
        contact_id = CodeGen().GenCode({"table": Contact.__tablename__, "column":Contact.code.name})
        # Generating the ID
        self.session.add(Contact(code=contact_id))
        # Saving
        self.session.commit()

        return {"status": 200, "value": {Contact.code.name: contact_id}, 'type': 'application/json'}

    def Handle(self, inputs):
        """This function, save and stores or modify the
        contact information.
        As parameter receive:
        Name.
        LastName.
        CellPhone.
        Telephone.
        Address.
        Email.
        Status.
        """

        item = int(inputs[Contact.code.name])
        birthdate = general().date2julian("1900-01-01")
        if "birthdate" in inputs:
            if len(inputs["birthdate"])==9:
                birthdate=general.date2julian(inputs["birthdate"])
        inputs[Contact.birthdate.name]=birthdate

        storeDict = {}
        for column in DBProcess(Contact.Contact_tbl).getColumnDefinition:
            if column["name"] in inputs:
                storeDict[column["expr"]] = DBProcess(Contact.Contact_tbl).parse(column, inputs[column["name"]])

        self.session.query(Contact).filter_by(code=item).update(storeDict)
        self.msg={"code":item}
        self.session.commit()
        return {"status": 200, "value": self.msg, 'type': 'application/json'}

if __name__ == '__main__':
    None


__author__ = 'hidura'
