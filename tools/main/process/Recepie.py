from sqlalchemy.orm.session import sessionmaker
from sqlalchemy.sql.expression import and_

from tools.DataBase.CodeGenerator import CodeGen
from tools.DataBase.Connect import conection
from tools.DataBase.Definition import db
from tools.DataBase.Definition.Item import Item
from tools.DataBase.Definition.Recipe import Recipe
from tools.DataBase.Definition.Status import Status
from tools.DataBase.Definition.Type import Type
from tools.DataBase.Definition.company import company
from tools.DataBase.Process import DBProcess
from tools.main.general import general
from tools.main.process.Items import Items


class Recepie:
    def __init__(self):
        self.status = 200
        self.msg = None
        self.type = "text/plain"

        self.session = db.session

    def create(self, inputs):
        # This method will create an expense.
        self.code = CodeGen().GenCode({"table": Recipe.__tablename__, "column": Recipe.code.name})
        # Generating the code.
        self.session.add(Recipe(code=self.code, status=12))
        # Saving
        self.session.commit()
        return {"status": 200, "value": {Recipe.code.name: self.code}, 'type': 'application/json'}

    def Handle(self, inputs):
        # This method will modify an expanse.
        code = int(inputs[Recipe.code.name])

        storeDict = {}
        for column in DBProcess(Recipe.Recepie_tbl).getColumnDefinition:
            if column["name"] in inputs:
                storeDict[column["expr"]] = DBProcess(Recipe.Recepie_tbl).parse(column, inputs[column["name"]])

        self.session.query(Recipe).filter_by(code=code).update(storeDict)

        self.session.commit()
        return {"status": 200, "value": {Recipe.code.name: code}, 'type': 'application/json'}

    def Get(self, inputs):
        # This method gets the data, from the db.
        storeDict = []
        if Recipe.code.name in inputs:
            storeDict = self.session.query(Recipe, Status.description,Item.item_name). \
                filter(and_(Status.code == Recipe.status, company.code == Recipe.commerce,
                            Recipe.item == Item.code,
                            Recipe.code == int(inputs[Recipe.code.name])))
        elif Recipe.item_name.name in inputs:
            storeDict = self.session.query(Recipe, Status.description, company.name). \
                filter(and_(Status.code == Recipe.status, company.code==Recipe.commerce,
                            Recipe.item == Item.code,
                            Item.item_name.like("%" + inputs[Item.item_name.name] + "%")))
        # The next area is in charge to extract the information,
        # from the store Dict and add it to the dataCol to be returned

        dataCol = []

        for dataLst in storeDict:
            dicStore = {Status.description.name: dataLst._asdict()[Status.description.name],
                        Type.tpname.name: dataLst._asdict()[Type.tpname.name],
                        Item.item_name.name:dataLst._asdict()[Item.item_name.name]}

            for key in DBProcess(Recipe.Recepie_tbl).getColumnDefinition:
                dataDict = dataLst._asdict()[Item.__name__].__dict__  # Getting the dictionary of the list.
                colname = key["name"]  # Getting the column name.
                if colname in dataDict:  # Just if the column name is on the dictionary, add it to the dictStore.

                    dicStore[colname] = DBProcess(Item.Item_tbl).parse2publish(dataDict[colname])

            dataCol.append(dicStore)
            # Appending everything to be returned

        return {"status": 200, "value": dataCol, 'type': 'application/json'}


if __name__ == '__main__':
    Recepie()

__author__ = 'hidura'
