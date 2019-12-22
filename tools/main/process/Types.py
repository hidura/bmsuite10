from sqlalchemy.orm.session import sessionmaker
from sqlalchemy.sql.expression import and_

from tools.DataBase.CodeGenerator import CodeGen
from tools.DataBase.Connect import conection
from tools.DataBase.Definition import db
from tools.DataBase.Definition.Level import Level
from tools.DataBase.Definition.Type import Type
from tools.DataBase.Process import DBProcess


class Types:
    def __init__(self):
        self.status = 200
        self.msg = None
        self.type = "text/plain"
        self.session = db.session

    def create(self, inputs):
        # This method will create an expense.
        self.code = CodeGen().GenCode({"table":
                                           Type.__tablename__,
                                       "column": Type.code.name})
        # Generating the code.
        level=None
        if Type.level.name in inputs:
            level = int(inputs[Type.level.name])
            raw_code = str(level)+str(self.code)
            self.code = int(raw_code)
        tpname=""
        if Type.tpname.name in inputs:
            tpname=inputs[Type.tpname.name]


        self.session.add(Type(code=self.code, tpname=tpname, level=level))
        # Saving
        self.session.commit()
        return {"status": 200, "value": {Type.code.name: self.code}, 'type': 'application/json'}

    def Handle(self, inputs):
        # This method will modify an expanse.
        item = int(inputs[Type.code.name])
        storeDict = {}

        for column in DBProcess(Type.Type_tbl).getColumnDefinition:
            if column["name"] in inputs:
                storeDict[column["expr"]] = DBProcess(Type.Type_tbl).parse(column, inputs[column["name"]])

        self.session.query(Type).filter_by(code=item).update(storeDict)
        self.session.commit()

        return {"status": 200, "value": {Type.code.name: item}, 'type': 'application/json'}

    def Get(self, inputs):
        # This method gets the data, from the db.
        storeDict = []
        if Type.code.name in inputs:
            storeDict = self.session.query(Type, Level.lvl_name). \
                filter(and_(Level.code == Type.level, Type.code == int(inputs[Type.code.name])))
        elif Type.tpname.name in inputs:
            storeDict = self.session.query(Type, Level.lvl_name). \
                filter(and_(Level.code == Type.level, Type.tpname.like("%" + inputs[Type.tpname.name] + "%")))
        elif Type.level.name in inputs:
            storeDict = self.session.query(Type, Level.lvl_name). \
                filter(and_(Level.code == Type.level, Type.level == int(inputs[Type.level.name])))
        # The next area is in charge to extract the information,
        # from the store Dict and add it to the dataCol to be returned
        storeDict=storeDict.order_by(Type.tpname.asc())
        dataCol = []

        for dataLst in storeDict:

            dicStore = {"level_name": dataLst._asdict()["lvl_name"]}
            for key in DBProcess(Type.Type_tbl).getColumnDefinition:

                dataDict = dataLst._asdict()[Type.__name__].__dict__  # Getting the dictionary of the list.
                colname = key["name"]  # Getting the column name.
                if "_sa_" not in colname:  # Just if the column name is on the dictionary, add it to the dictStore.
                    dicStore[colname] = dataDict[colname]

            dataCol.append(dicStore)
            # Appending everything to be returned

        return {"status": 200, "value": dataCol, 'type': 'application/json'}

if __name__ == '__main__':
    print(Types().create({Type.tpname.name: "Galon-224", Type.level.name: 5}))


__author__ = 'hidura'
