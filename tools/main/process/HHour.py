from mongoengine.connection import disconnect
from sqlalchemy.orm.session import sessionmaker

from tools.DataBase.CodeGenerator import CodeGen
from tools.DataBase.Connect import conection
from tools.DataBase.Definition import db
from tools.DataBase.Definition.HappyHour import HappyHour
from tools.DataBase.Definition.Status import Status
from tools.DataBase.Process import DBProcess


class HHour:
    def __init__(self):
        self.status = 200
        self.msg = None
        self.type = "text/plain"

        self.session = db.session

    def create(self, inputs):
        # This method will create an expense.
        if HappyHour.code.name not in inputs:
            self.code = CodeGen().GenCode({"table": HappyHour.__tablename__,
                                       "column": HappyHour.code.name})
        else:
            self.code = int(inputs[HappyHour.code.name])

        # Generating the code.
        self.session.add(HappyHour(code=self.code))
        # Saving
        self.session.commit()
        return {"status": 200, "value": {HappyHour.code.name: self.code}, 'type': 'application/json'}

    def Handle(self, inputs):
        # This method will modify an expanse.
        item = int(inputs[HappyHour.code.name])
        storeDict = {}

        for column in DBProcess(HappyHour.HappyHour_tbl).getColumnDefinition:
            if column["name"] in inputs:
                storeDict[column["expr"]] = inputs[column["name"]]

        self.session.query(HappyHour).filter_by(code=item).update(storeDict)
        self.session.commit()
        return {"status": 200, "value": {HappyHour.code.name: item}, 'type': 'application/json'}

    def Get(self, inputs):
        self.msg=[]
        storeDict = self.session.query(HappyHour, Status.description). \
            filter(Status.code == HappyHour.status)

        if HappyHour.code.name in inputs:
            storeDict = storeDict.filter(HappyHour.code == int(inputs[HappyHour.code.name]))

        elif HappyHour.product.name in inputs:
            storeDict = storeDict.filter(HappyHour.product == int(inputs[HappyHour.product.name]))


        for dataLst in storeDict:

            dicStore = {"status_name": dataLst._asdict()[Status.description.name]}
            for key in DBProcess(Status.Status_tbl).getColumnDefinition:

                dataDict = dataLst._asdict()[HappyHour.__name__].__dict__  # Getting the dictionary of the list.
                colname = key["name"]  # Getting the column name.
                if "_sa_" not in colname:  # Just if the column name is on the dictionary, add it to the dictStore.
                    dicStore[colname] = dataDict[colname]

            self.msg.append(dicStore)
            # Appending everything to be returned


        return {"status": 200, "value": self.msg, 'type': 'application/json'}
