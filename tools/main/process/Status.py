from sqlalchemy.orm.session import sessionmaker
from sqlalchemy.sql.expression import and_

from tools.DataBase.CodeGenerator import CodeGen
from tools.DataBase.Connect import conection
from tools.DataBase.Definition import db
from tools.DataBase.Definition.Status import Status
from tools.DataBase.Definition.Type import Type
from tools.DataBase.Process import DBProcess
from tools.main.general import general


class StatusProc:
    def __init__(self):
        self.status = 200
        self.msg = None
        self.type = "text/plain"

        self.session = db.session

    def create(self, inputs):
        # This method will create an expense.
        if Status.code.name not in inputs:
            self.code = CodeGen().GenCode({"table": Status.__tablename__,
                                       "column": Status.code.name})
        else:
            self.code = int(inputs[Status.code.name])

        name = ""
        if Status.description.name in inputs:
            name=inputs[Status.description.name]

        tpstatus=None
        if Status.tp_status.name in inputs:
            tpstatus = int(inputs[Status.tp_status.name])

        # Generating the code.
        self.session.add(Status(code=self.code, name=name, tp_status=tpstatus))
        # Saving
        self.session.commit()
        return {"status": 200, "value": {Status.code.name: self.code}, 'type': 'application/json'}

    def Handle(self, inputs):
        # This method will modify an expanse.
        item = int(inputs[Status.code.name])
        storeDict = {}

        for column in DBProcess(Status.Status_tbl).getColumnDefinition:
            if column["name"] in inputs:
                storeDict[column["expr"]] = inputs[column["name"]]

        self.session.query(Status).filter_by(code=item).update(storeDict)
        self.session.commit()
        return {"status": 200, "value": {Status.code.name: item}, 'type': 'application/json'}

    def Get(self, inputs):
        self.msg=[]
        storeDict = self.session.query(Status, Type.tpname). \
            filter(Status.statustp == Type.code)
        if Status.code.name in inputs:
            storeDict = storeDict.filter(Status.code==int(inputs[Status.code.name]))

        elif Status.description.name in inputs:
            storeDict = storeDict.filter(Status.description.ilike("%"+str(inputs[Status.description.name])+"%"))

        elif Status.statustp.name in inputs:
            storeDict = storeDict.filter(Status.statustp == int(inputs[Status.statustp.name]))

        for dataLst in storeDict:

            dicStore = {Type.tpname.name: dataLst._asdict()[Type.tpname.name]}
            for key in DBProcess(Status.Status_tbl).getColumnDefinition:

                dataDict = dataLst._asdict()[Status.__name__].__dict__  # Getting the dictionary of the list.
                colname = key["name"]  # Getting the column name.
                if "_sa_" not in colname:  # Just if the column name is on the dictionary, add it to the dictStore.
                    dicStore[colname] = dataDict[colname]

            self.msg.append(dicStore)
            # Appending everything to be returned


        return {"status": 200, "value": self.msg, 'type': 'application/json'}

if __name__ == '__main__':
    StatusProc().create({Status.description.name:"Factura abierta", Status.code.name:24,
                         Status.tp_ :2})


__author__ = 'hidura'
