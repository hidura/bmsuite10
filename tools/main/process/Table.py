from mongoengine.connection import disconnect
from sqlalchemy.orm.session import sessionmaker
from sqlalchemy.sql.expression import and_

from tools.DataBase.CodeGenerator import CodeGen
from tools.DataBase.Connect import conection
from tools.DataBase.Definition import db
from tools.DataBase.Definition.Area import Area
from tools.DataBase.Definition.Status import Status
from tools.DataBase.Definition.Tables import Tables
from tools.DataBase.ODM.DataModelODM import PreOrderTable
from tools.DataBase.Process import DBProcess


class Table:
    def __init__(self):
        self.status = 200
        self.msg = None
        self.type = "text/plain"

        self.session = db.session

    def create(self, inputs):
        # This method will create an expense.
        self.code = CodeGen().GenCode({"table": Tables.__tablename__,
                                       "column": Tables.code.name})
        tblname=""
        if Tables.tblname.name in inputs:
            tblname = inputs[Tables.tblname.name]

        table_area = None
        if Tables.area.name in inputs:
            table_area = int(inputs[Tables.area.name])

        table_type = None
        if Tables.table_type.name in inputs:
            table_type = int(inputs[Tables.table_type.name])

        status = None
        if Tables.status.name in inputs:
            if str(inputs[Tables.status.name]).lower()=="on":
                status = 11

        # Generating the code.
        self.session.add(Tables(code=self.code,
                                tblname=tblname, table_type=table_type,
                                area=table_area, status=status))
        # Saving with the name, at least.
        self.session.commit()
        return {"status": 200, "value": {Tables.code.name: self.code},
                'type': 'application/json'}

    def Handle(self, inputs):
        # This method will modify an expanse.
        where=""
        self.msg = {}
        if Tables.tblname.name in inputs and Tables.code.name not in inputs:
            where = and_(Tables.tblname == inputs[Tables.tblname.name])
            self.msg[Tables.tblname.name] = inputs[Tables.tblname.name]
        else:
            where = and_(Tables.code == int(inputs[Tables.code.name]))
            self.msg[Tables.code.name] = inputs[Tables.code.name]

        status = 12
        if Tables.status.name in inputs:
            if str(inputs[Tables.status.name]).lower() == "on":
                status = 11
        inputs[Tables.status.name] = status

        storeDict = {}
        process = DBProcess(Tables.Tables_tbl)
        for column in process.getColumnDefinition:
            if column["name"] in inputs:
                storeDict[column["expr"]] = process.parse(column,inputs[column["name"]])
        self.session.query(Tables).filter(where).update(storeDict)

        self.session.commit()
        return {"status": 200, "value": self.msg, 'type': 'application/json'}

    def Get(self, inputs):
        # This method gets the data, from the db.
        storeDict = []
        if Tables.code.name in inputs:
            storeDict = self.session.query(Tables, Status.description). \
                filter(and_(Status.code == Tables.status, Tables.code
                            == int(inputs["table"]))).order_by(Tables.area.asc())
        elif Tables.tblname.name in inputs and Tables.area.name not in inputs:
            storeDict = self.session.query(Tables, Status.description). \
                filter(and_(Status.code == Tables.status,
                            Tables.tblname.like("%"+inputs[Tables.tblname.name]+"%"))).order_by(Tables.area.asc())

        elif Tables.tblname.name in inputs and Tables.area.name in inputs:
            storeDict = self.session.query(Tables, Status.description). \
                filter(and_(Status.code == Tables.status, Tables.area==int(inputs[Tables.area.name]),
                            Tables.tblname.like("%" + inputs[Tables.tblname.name] + "%"))).order_by(Tables.area.asc())

        # The next area is in charge to extract the information,
        # from the store Dict and add it to the dataCol to be returned

        dataCol = []

        for dataLst in storeDict:

            dicStore = {"status_name": dataLst._asdict()[Status.description.name]}

            for key in DBProcess(Tables.Tables_tbl).getColumnDefinition:
                dataDict = dataLst._asdict()[Tables.__name__].__dict__  # Getting the dictionary of the list.
                colname = key["name"]  # Getting the column name.
                if colname in dataDict:  # Just if the column name is on the dictionary, add it to the dictStore.
                    dicStore[colname] = dataDict[colname]

            area_info=self.session.query(Area).filter(Area.code==dicStore[Tables.area.name]).first()
            if area_info!=None:
                dicStore["area_name"]=area_info.area_name
            sale_table = PreOrderTable.objects(table_code=dicStore[Tables.code.name], status=24).first()
            if sale_table != None:
                dicStore["bill"] = sale_table.preorder
            dataCol.append(dicStore)
            # Appending everything to be returned

        return {"status": 200, "value": dataCol, 'type': 'application/json'}

    # Table on the bills area.


    def getTableActive(self, inputs):
        # This method will bring the tables with the code of the preorder.
        storeDict = []
        storeDict = self.session.query(Tables, Status.description). \
            filter(and_(Status.code == Tables.status, Tables.area == int(inputs[Tables.area.name])))

        dataCol = []
        for dataLst in storeDict:

            dicStore = {"status_name": dataLst._asdict()[Status.description.name]}

            for key in DBProcess(Tables.Tables_tbl).getColumnDefinition:
                dataDict = dataLst._asdict()[Tables.__name__].__dict__  # Getting the dictionary of the list.
                colname = key["name"]  # Getting the column name.
                if colname in dataDict:  # Just if the column name is on the dictionary, add it to the dictStore.
                    dicStore[colname] = dataDict[colname]

            area_info=self.session.query(Area).filter(Area.code==dicStore[Tables.area.name]).first()
            if area_info!=None:
                dicStore["area_name"]=area_info.area_name
            sale_table = PreOrderTable.objects(table_code=dicStore[Tables.code.name], status=24).first()
            if sale_table != None:
                dicStore["bill"] = sale_table.preorder
            dataCol.append(dicStore)
            # Appending everything to be returned
        return {"status": 200, "value": dataCol, 'type': 'application/json'}


if __name__ == '__main__':
    print(Table().Handle({Tables.tblname.name:"Mesa 1",
                          Tables.status.name:11,
                          Tables.area.name:3,
                          "table":6}))

__author__ = 'hidura'
