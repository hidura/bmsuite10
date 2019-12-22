import json

import requests

from tools.DataBase.CodeGenerator import CodeGen
from tools.DataBase.Definition.Base import db
from tools.DataBase.Definition.BuyOrderProds import BuyOrderProds
from tools.DataBase.Definition.BuyOrderTbl import BuyOrderTbl
from tools.DataBase.Definition.Supplier import Supplier
from tools.DataBase.Definition.SupplierOrder import SupplierOrder
from tools.DataBase.Definition.Type import Type
from tools.DataBase.Definition.Views.ItemMins import ItemMins
from tools.DataBase.Definition.Views.getaccounts import getaccounts
from tools.DataBase.Definition.WareHouse import WareHouse
from tools.DataBase.ODM.DataModelODM import rule_user
from tools.DataBase.Process import DBProcess
from tools.main import general
from tools.main.process.General import General, NotificationsCls
from tools.main.process.login import login


class BuyOrder:
    def __init__(self):



        self.status = 200
        self.msg = None
        self.type = "text/plain"

        self.session = db.session

    def loadInitial(self, inputs=None):
        self.msg = {"supplier":[], "min_products":[],"paytype":[],
                    "warehouse":[], "accounts":[], 'rules':[]}
        data = self.session.query(Supplier)
        for piece in data:
            del piece.__dict__['_sa_instance_state']
            self.msg["supplier"].append(piece)

        data = self.session.query(WareHouse)
        for piece in data:
            del piece.__dict__['_sa_instance_state']
            self.msg["warehouse"].append(piece)

        data = self.session.query(ItemMins).\
            filter(WareHouse.mainwarehouse==True)
        for piece in data:
            del piece.__dict__['_sa_instance_state']
            self.msg["min_products"].append(piece.__Publish__())

        for piece in db.session.query(getaccounts):
            self.msg['accounts'].append(piece.__Publish__())

        self.msg['rules']=rule_user.objects().to_json()

        # Extracting the paytype
        data = self.session.query(Type).filter_by(level = 11)
        for piece in data:
            del piece.__dict__['_sa_instance_state']
            self.msg["paytype"].append(piece)
        return self.msg


    def create(self, inputs):
        # Create new
        buyorder = CodeGen().GenCode({"table": BuyOrderTbl.__tablename__, "column": BuyOrderTbl.code.name})
        self.session.add(BuyOrderTbl(code=buyorder,warehouse=int(inputs[BuyOrderTbl.warehouse.name]),
                                     buy_name=inputs[BuyOrderTbl.buy_name.name],
                                     registred=float(general().date2julian()),
                                     receive_date=float(general().date2julian(inputs[BuyOrderTbl.receive_date.name])),
                                     recive_time=str(inputs[BuyOrderTbl.recive_time.name])))


        self.session.commit()
        products = []
        for piece in json.loads(inputs["products"]):
            products.append(BuyOrderProds(buyorder=buyorder,product=int(piece["product"]),
                                          product_name=piece["product_name"],
                                          amount=float(piece["amount"]),
                                          tax=float(piece['tax']) if 'tax' in piece else 0.00,
                                          price_uni=float(piece['subtotal']) if 'subtotal' in piece else 0.00,
                                          total=float(piece['total']) if 'total' in piece else 0.00,
                                          discount=float(piece['discount']) if 'discount' in piece else 0.00,
                                          supplier=int(piece["supplier"]) if "supplier" in piece else int(inputs['supplier']),
                                          notes=piece["notes"] if 'notes' in piece else ""))
        self.session.bulk_save_objects(products)
        self.session.commit()

        self.msg = {BuyOrderTbl.code.name: buyorder}
        return self.msg

    def Handle(self, inputs):
        # Handle the created ...
        storeDict = {}
        for column in DBProcess(BuyOrderTbl.BuyOrderTbl_tbl).getColumnDefinition:
            if column["name"] in inputs:
                storeDict[column["expr"]] = DBProcess(BuyOrderTbl.BuyOrderTbl_tbl).parse(column, inputs[column["name"]])

        self.session.query(BuyOrderTbl).filter_by(code=int(inputs[BuyOrderTbl.code.name])).update(storeDict)

        self.session.commit()

        products = []
        for piece in inputs["products"]:
            products.append(BuyOrderProds(buyorder=int(inputs[BuyOrderTbl.code.name]), product=int(piece["product"]),
                                          amount=float(piece["amount"]), supplier=int(piece["supplier"]),
                                          notes=piece["notes"]))
        self.session.bulk_save_objects(products)
        self.session.commit()




    def getOrderByCode(self, inputs):
        data = self.session.query(ItemMins). \
            filter(WareHouse.mainwarehouse == True)
        for piece in data:
            del piece.__dict__['_sa_instance_state']
            self.msg["min_products"].append(piece.__Publish__())

        return self.msg


    def requestProducts(self,inputs):
        # This method make the request to the product.

        response = requests.post(inputs['bmsnet']+'add_order',
                                 data=json.dumps(inputs))

        if response.status_code == 200:

            return {"key":response.content.decode().strip('"')}

        else:
            raise Exception(str(print(response.text)))


    def receiveResponse(self, inputs):
        # This method receive the response from the supplier and generate the notification.
        SupplierOrder.handle(inputs, inputs["key_uuid"])
        for user_code in rule_user.objects(rule_code=17):
            NotificationsCls().create({'recipient':user_code.user_code,
                                       'message':"El suplidor %s respondio a tu peticion!"%(inputs["supplier_name"]),
                                       'link':'/view_order?id='+inputs["key_uuid"]})
            user_info = login().Get({'code': user_code.user_code})["value"]

            general().sendMail('Subject: %s\n\n%s' % ("Nueva notificacion, NOT-REPLY", "<p>Tiene una notificacion "
                                                                                       "de compra registrada, "
                                                                                       "para verla dirijase a BMSUITE</p>"
                                                                                       "<p>-- <br/>BMSUITE</p>"),
                               user_info['username'])
if __name__ == '__main__':
    None