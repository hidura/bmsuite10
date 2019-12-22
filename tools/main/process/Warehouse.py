import json
from decimal import Decimal

from mongoengine.connection import disconnect

from tools.DataBase.CodeGenerator import CodeGen
from tools.DataBase.Connect import conection
from sqlalchemy.orm.session import sessionmaker
from sqlalchemy.sql.expression import and_

from tools.DataBase.Definition import db
from tools.DataBase.Definition.ProductsAmount import ProductsAmount
from tools.DataBase.Definition.ProductsMove import ProductsMove
from tools.DataBase.Definition.Status import Status
from tools.DataBase.Definition.WareHouse import WareHouse
from tools.DataBase.ODM.DataModelODM import warehouse_prods, Moveproducts
from tools.DataBase.Process import DBProcess
from tools.main import general


class warehouse:
    def __init__(self):
        self.status = 200
        self.msg = None
        self.type = "text/plain"

        self.session = db.session


    def create(self, inputs):
        # This method will create an expense.
        self.code = CodeGen().GenCode({"table": WareHouse.__tablename__, "column": WareHouse.code.name})
        # Generating the code.

        self.session.add(WareHouse(code=self.code, status=12,
                                   billDisc=False))
        # Saving with the name, at least.
        self.session.commit()
        return {"status": 200, "value": {WareHouse.code.name: self.code}, 'type': 'application/json'}

    def Handle(self, inputs):
        # This method will modify an expanse.
        warehouse_target = int(inputs[WareHouse.code.name])
        storeDict = {}
        #Defining the status
        status = 12
        if "status" in inputs:
            if str(inputs["status"]).lower() =="on":
                status = 11
        mainwarehouse=False
        if "mainwarehouse" in inputs:
            if inputs["mainwarehouse"]=='on':
                mainwarehouse=True
        inputs["mainwarehouse"]=mainwarehouse
        inputs["status"] = status

        for column in DBProcess(WareHouse.WareHouse_tbl).getColumnDefinition:
            if column["name"] in inputs:
                storeDict[column["expr"]] = DBProcess(WareHouse.WareHouse_tbl).parse(column,inputs[column["name"]])

        self.session.query(WareHouse).filter_by(code=warehouse_target).update(storeDict)
        self.session.commit()
        return {"status": 200, "value": {WareHouse.code.name: warehouse_target}, 'type': 'application/json'}

    def addProduct2Warehouse(self, inputs):

        amount=int(inputs["amount"])

        code=CodeGen().GenCode({"table": "warehouse_prods", "column": "code"})
        warehouse_prods(warehouse=int(inputs[WareHouse.code.name]),
                        product=int(inputs["product"]),code=code,
                        amount=amount).save()

        return {"status": 200, "value": {WareHouse.code.name: code}, 'type': 'application/json'}

    def delProduct2Warehouse(self, inputs):

        code=int(inputs["code"])
        warehouse_prods.objects(code=code).update(set__status=13)

        return {"status": 200, "value": {WareHouse.code.name: code}, 'type': 'application/json'}


    def addMovement(self, inputs):
        self.code = CodeGen().GenCode({"table": ProductsMove.__tablename__,
                                       "column": ProductsMove.code.name})
        # Generating the code.

        self.session.add(ProductsMove(code=self.code))

        # Saving
        self.session.commit()
        return {"status": 200, "value": {ProductsMove.code.name: self.code}, 'type': 'application/json'}

    def RegisterMove(self, inputs):
        # This method register a move of product

        created = general().date2julian()
        inputs["created"] = created
        if ProductsMove.send_date.name in inputs:
            inputs[ProductsMove.send_date.name] = general().date2julian(inputs[ProductsMove.send_date.name])

        item = int(inputs[ProductsMove.code.name])

        storeDict = {}
        for column in DBProcess(ProductsMove.ProductsMove_tbl).getColumnDefinition:
            if column["name"] in inputs:
                storeDict[column["expr"]] = DBProcess(ProductsMove.ProductsMove_tbl).\
                    parse(column,inputs[column["name"]])



        # Adding the product to the warehouse.
        for product in json.loads(inputs["products"]):

            connection = self.connORM.raw_connection()
            cursor = connection.cursor()

            code = CodeGen().GenCode({"table": "Moveproducts", "column": "code"})

            Moveproducts(code=code, give_by=int(inputs["from_warehouse"]), receive_by=int(inputs["to_warehouse"]),
                         product=int(product["product"]), created_date=general().date2julian(),
                         description=product["item_name"]).save()

            cursor.callproc('products_movement', [int(product["product"]), Decimal(product["amount"]),
                                                  int(inputs["from_warehouse"]), int(inputs["to_warehouse"])])
            cursor.close()

        self.session.commit()

        return {"status": 200, "value": {ProductsMove.code.name: item}, 'type': 'application/json'}

    def Get(self, inputs):
        # This method gets the data, from the db.
        storeDict = []
        if WareHouse.code.name in inputs:
            storeDict = self.session.query(WareHouse, Status.description). \
                filter(and_(Status.code == WareHouse.status, WareHouse.code
                            == int(inputs[WareHouse.code.name])))
        elif WareHouse.description.name in inputs:
            storeDict = self.session.query(WareHouse, Status.description). \
                filter(and_(Status.code == WareHouse.status,
                            WareHouse.description.like("%"+inputs[WareHouse.description.name]+"%")))
        # The next area is in charge to extract the information,
        # from the store Dict and add it to the dataCol to be returned
        dataCol = []
        for dataLst in storeDict:

            dicStore = {"status_name": dataLst._asdict()[Status.description.name]}

            for key in DBProcess(WareHouse.WareHouse_tbl).getColumnDefinition:
                dataDict = dataLst._asdict()[WareHouse.__name__].__dict__  # Getting the dictionary of the list.
                colname = key["name"]  # Getting the column name.
                if colname in dataDict:  # Just if the column name is on the dictionary, add it to the dictStore.
                    dicStore[colname] = dataDict[colname]

            dataCol.append(dicStore)
            # Appending everything to be returned

        return {"status": 200, "value": dataCol, 'type': 'application/json'}