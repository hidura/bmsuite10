import json
from decimal import Decimal

from sqlalchemy.orm.session import sessionmaker
from sqlalchemy.sql.expression import and_
from tools.DataBase.CodeGenerator import CodeGen
from tools.DataBase.Connect import conection
from tools.DataBase.Definition import db
from tools.DataBase.Definition.Client import Client
from tools.DataBase.Definition.Item import Item
from tools.DataBase.Definition.Merma import Merma
from tools.DataBase.Definition.ProductsAmount import ProductsAmount
from tools.DataBase.Definition.Status import Status
from tools.DataBase.Definition.Supplier import Supplier
from tools.DataBase.Definition.Type import Type
from tools.DataBase.Definition.User import User
from tools.DataBase.Definition.Views.BuyItemsRep import BuyItemsRep
from tools.DataBase.Definition.Views.SalesRep import SalesRep
from tools.DataBase.Definition.WareHouse import WareHouse
from tools.DataBase.Definition.buybills import buybills
from tools.DataBase.Definition.salebills import salebills
from tools.DataBase.ODM.DataModelODM import Buyitems, Equivalence, MermaProd, recipe_items, account_movement, \
    cashbox_bills, ncf_codes, ncfType
from tools.DataBase.Process import DBProcess
from tools.main.general import general
from tools.main.process.Accounts import Accounts
from tools.main.process.Items import Items
from tools.main.process.Types import Types
from tools.main.process.login import login


class Accounting:
    def __init__(self):

        self.status = 200
        self.msg = None
        self.type = "text/plain"

        self.session = db.session

    def create(self, inputs):
        # This method will create an expense.
        self.code = CodeGen().GenCode({"table": buybills.__tablename__, "column": buybills.code.name})
        # Generating the code.

        self.session.add(buybills(code=self.code, status=11))
        # Saving
        self.session.commit()
        return {"status": 200, "value": {buybills.code.name: self.code}, 'type': 'application/json'}


    def Handle(self, inputs):
        # This method will modify an expanse.
        if buybills.code.name in inputs:
            item = int(inputs[buybills.code.name])
        else:
            item = CodeGen().GenCode({"table": buybills.__tablename__, "column": buybills.code.name})
            self.session.add(buybills(code=item, status=11))

        storeDict = {}
        for column in DBProcess(buybills.buybills_tbl).getColumnDefinition:
            if column["name"] in [buybills.generated.name, buybills.payalert.name, buybills.expires.name]:
                jdate = general().date2julian(inputs[column["name"]])
                inputs[column["name"]]=jdate


            if column["name"] in inputs:
                storeDict[column["expr"]] = DBProcess(buybills.buybills_tbl).parse(column, inputs[column["name"]])

        self.session.query(buybills).filter_by(code=item).update(storeDict)
        if "products" in inputs:
            products = json.loads(inputs["products"])
            for piece in products:

                amount = float(piece["amount"])
                warehose = 0 if "warehouse" not in inputs else int(inputs["warehouse"])
                if "amount" in piece:

                    connection = self.connORM.raw_connection()
                    cursor = connection.cursor()
                    data =cursor.callproc('products_movement', [int(piece["product"]), amount,
                                                          warehose, 0])

                    cursor.close()
                    connection.commit()
        self.session.commit()
        return {"status": 200, "value": {buybills.code.name: item}, 'type': 'application/json'}

    def Get(self, inputs):
        #This method gets the data, from the db.
        storeDict =[]
        where =and_()
        if buybills.code.name in inputs:
            storeDict = self.session.query(buybills, Status.name, Supplier.sup_name).\
                filter(and_(Status.code == buybills.status, Supplier.code == buybills.supplier,
                            buybills.code== int(inputs[buybills.code.name])))

        elif buybills.supplier.name in inputs and \
                        buybills.generated.name not in inputs and \
                        buybills.expires.name not in inputs:

            storeDict = self.session.query(buybills, Status.name, Supplier.sup_name).\
                filter(and_(Status.code == buybills.status, Supplier.code==buybills.supplier, buybills.supplier
                            == int(inputs[buybills.supplier.name])))

        elif buybills.supplier.name in inputs and \
                 buybills.generated.name in inputs:
            storeDict = self.session.query(buybills, Status.name, Supplier.sup_name). \
                filter(and_(Status.code == buybills.status, buybills.code
                            == int(inputs[buybills.supplier.name])))
        # The next area is in charge to extract the information,
        # from the store Dict and add it to the dataCol to be returned

        dataCol=[]

        for dataLst in storeDict:

            dicStore = {"status_name":dataLst._asdict()["name"],
                        Supplier.sup_name.name: dataLst._asdict()
                        [Supplier.sup_name.name]}

            for key in DBProcess(buybills.buybills_tbl).getColumnDefinition:
                dataDict = dataLst._asdict()[buybills.__name__].__dict__  # Getting the dictionary of the list.
                colname = key["name"]  # Getting the column name.
                if colname in dataDict:  # Just if the column name is on the dictionary, add it to the dictStore.
                    if colname in [buybills.generated.name, buybills.payalert.name, buybills.expires.name]:
                        if dataDict[colname]!=None:
                            jdate = general().julian2date(str(dataDict[colname]))
                            dataDict[colname] = jdate
                        else:
                            dataDict[colname]=" "
                    dicStore[colname] = DBProcess(buybills.buybills_tbl).parse2publish(dataDict[colname])

            dataCol.append(dicStore)
            # Appending everything to be returned

        return {"status": 200, "value": dataCol, 'type': 'application/json'}


    def addItem2Bill(self, inputs):
        self.code = CodeGen().GenCode({"table": "Buyitems", "column": "code"})
        equivalence = 1
        if "from_eq" in inputs:
            equivalence = int(str(inputs["from_eq"]).split(":")[0])
        unit = 517
        if "to_eq" in inputs:
            unit = int(inputs["to_eq"])

        amount = float(inputs["amount"])
        equivalence_data = Equivalence.objects(from_eq=unit, to_eq=equivalence)

        equivalence_info = equivalence_data.first()
        if equivalence_info!= None:
            if equivalence_info.optype == "*":
                amount = float(equivalence_info.equivalence) * float(inputs["amount"])
            if equivalence_info.optype == "/":
                amount = float(equivalence_info.equivalence) / float(inputs["amount"])


        Buyitems(code=self.code, product=int(inputs["product"]), amount=amount,
                 total=float(inputs["total"]), tax=float(inputs["total_tax"]),
                 bill=int(inputs["bill"]),unit=unit,term="",portion="",notes="",
                 created_by=login().decLoginKey(inputs["key"]),created_date=general().date2julian()).save()

        cur_amount = self.session.query(Item.amount).filter_by(code=int(inputs["product"])).first()[0]

        if cur_amount == None or cur_amount=='None':
            cur_amount = 0.00

        Items().Handle({Item.code.name: inputs["product"], Item.amount.name: float(cur_amount) + amount})

        warehouse_info = self.session.query(WareHouse).filter_by(mainwarehouse=True)
        warehouse_info = self.session.query(WareHouse).filter_by(mainwarehouse=True)
        if warehouse_info != None and "amount" in inputs:
            warehose = warehouse_info[0]
            connection = self.connORM.raw_connection()
            cursor = connection.cursor()

            cursor.callproc('products_movement', [self.code, amount,
                                                  warehose.code, 0])
            cursor.close()


        return {"status": 200, "value": {"code":self.code}, 'type': 'application/json'}



    def delItem2Bill(self, inputs):
        self.code =int(inputs["code"])
        buy_item_data = Buyitems.objects(code=self.code).first()



        amount = float(buy_item_data.amount)



        cur_amount = self.session.query(Item.amount).filter_by(code=buy_item_data.product).first()[0]

        if cur_amount == None or cur_amount=='None':
            cur_amount = 0.00

        Items().Handle({Item.code.name: buy_item_data.product, Item.amount.name: float(cur_amount)-amount})

        Buyitems.objects(code=self.code).update(set__status=13)
        return {"status": 200, "value": {"code":self.code}, 'type': 'application/json'}

    def getItem2Bill(self, inputs):

        items = Buyitems.objects(bill=inputs["bill"])
        self.msg=[]

        for piece in items:
            dicStore={"code":piece.code,
                             "item_name":Items().Get({"code":piece.product})["value"][0]["item_name"],
                             "item":piece.product,
                             "amount":piece.amount, "total":piece.total,
                             "tax":piece.tax, "status": piece.status}
            # Just for the products that are part of a recipe.
            item_recipe = recipe_items.objects(item=piece.product, status__lte=12).first()
            lastbuy = Buyitems.objects(product=piece.product).order_by('-id').first()

            if item_recipe != None and lastbuy == None:
                unit_info=Types().Get({"code": item_recipe.unit})["value"]
                if len(unit_info) > 0:
                    dicStore["unit_name"] = unit_info[0]["tpname"]
                else:
                    dicStore["unit_name"] = "Unidad"
            elif item_recipe == None and lastbuy != None:

                unit_info=Types().Get({"code": lastbuy.unit})["value"]
                if len(unit_info) > 0:
                    dicStore["unit_name"] = unit_info[0]["tpname"]
                else:
                    dicStore["unit_name"] = "Unidad"
            elif item_recipe != None and lastbuy != None:
                if item_recipe.unit == lastbuy.unit:
                    dicStore["unit_name"] = Types().Get({"code": lastbuy.unit})["value"][0]["tpname"]
                else:
                    dataEq = Equivalence.objects(from_eq=item_recipe.unit, to_eq=lastbuy.unit).first()
                    if dataEq != None:
                        dicStore["unit_name"] = Types().Get({"code": lastbuy.unit})["value"][0]["tpname"]
                        optype = dataEq.optype
                        equivalence = dataEq.equivalence
                        new_amount = dicStore[Item.amount.name]
                        if optype == "/":
                            new_amount = '{0:.2f}'.format(float(dicStore[Item.amount.name]) / equivalence)
                        elif optype == "*":
                            new_amount = '{0:.2f}'.format(float(dicStore[Item.amount.name]) * equivalence)
                        dicStore[Item.amount.name] = new_amount
                    else:
                        tpinfo=Types().Get({"code": lastbuy.unit})["value"]
                        if len(tpinfo)>0:
                            dicStore["unit_name"] = tpinfo[0]["tpname"]
                        else:
                            dicStore["unit_name"] ="Unidad"
            self.msg.append(dicStore)

        return {"status": 200, "value": self.msg, 'type': 'application/json'}


    def addEquivalence(self, inputs):
        equivalence = 1
        if "equivalence" in inputs:
            equivalence = float(inputs["equivalence"])

        self.code = CodeGen().GenCode({"table": "Equivalence", "column": "code"})

        Equivalence(code=self.code, eq_name=inputs["eq_name"],
                    from_eq=int(inputs["from_eq"]), to_eq=int(inputs["to_eq"]),
                    equivalence=equivalence, optype="*",
                    created_by=login().decLoginKey(inputs["key"]),
                    created_date=general().date2julian()).save()

        self.reversecode = CodeGen().GenCode({"table": "Equivalence", "column": "code"})

        Equivalence(code=self.reversecode, eq_name=inputs["eq_name"]+"(Reverso)",
                    to_eq=int(inputs["from_eq"]), from_eq=int(inputs["to_eq"]),
                    equivalence=equivalence, optype="/",
                    created_by=login().decLoginKey(inputs["key"]),
                    created_date=general().date2julian()).save()

        return {"status": 200, "value": {"code": self.code, "reversecode":self.reversecode}, 'type': 'application/json'}

    def delEquivalence(self, inputs):
        equivalence = 1

        Equivalence.objects(code=int(inputs["code"])).delete()

        return {"status": 200, "value": {"msg": "Borrado!"}, 'type': 'application/json'}


    def getEquivalence(self, inputs):
        unit = 517
        equivalent=517

        if "unit" in inputs:
            unit = int(inputs["unit"])

        if "equivalent" in inputs:
            equivalent = int(inputs["equivalent"])

        eq_info=Equivalence.objects(from_eq=unit, to_eq=equivalent).first()
        self.msg=[]
        if eq_info!=None:
            self.msg.append({"from_eq":eq_info.from_eq, "to_eq":eq_info.to_eq, "code":eq_info.code,
                             "optype":eq_info.optype, "equivalence":eq_info.equivalence, "status":eq_info.status})
        return {"status": 200, "value": self.msg, 'type': 'application/json'}

    def modItem2Bill(self, inputs):
        self.code = CodeGen().GenCode({"table": "Buyitems", "column": "code"})

        Buyitems.objects(code=self.code).update(set__item=int(inputs["product"]),
                                                set__total_item=float(inputs["total"]), set__total_tax=float(inputs["tax"]),
                                                set__other_costs=float(inputs["other_costs"]),set__discount=float(inputs["discount"]),
                                                set__unit=int(inputs["unit"]), set__equivalence=float(inputs["equivalence"]),
                                                set__created_by=login().decLoginKey(inputs["key"]), set__created_date=general().date2julian())

        cur_amount = Items().Get({Item.code.name: inputs["product"]})["value"][0][Item.amount.name]
        return {"status": 200, "value": {"code": self.code}, 'type': 'application/json'}

    def create_merma(self, inputs):
        self.code = CodeGen().GenCode({"table": Merma.__tablename__, "column": Merma.code.name})
        # Generating the code.

        self.session.add(Merma(code=self.code, status=12,
                               created_by=login().decLoginKey(inputs["key"])))
        # Saving
        self.session.commit()
        return {"status": 200, "value": {"code": self.code}, 'type': 'application/json'}

    def merma_Handle(self, inputs):
        item = int(inputs[Merma.code.name])
        storeDict = {}
        for column in DBProcess(Merma.Merma_tbl).getColumnDefinition:

            if column["name"] in [Merma.created.name] and column["name"] in inputs:
                jdate = general().date2julian(inputs[column["name"]])
                inputs[column["name"]] = jdate

            if column["name"] in inputs:
                storeDict[column["expr"]] = DBProcess(Merma.Merma_tbl).parse(column, inputs[column["name"]])

        self.session.query(Merma).filter_by(code=item).update(storeDict)
        self.session.commit()
        creator_profile = login().getProfile(inputs)

        user_rootlst = login().Get({User.usrtype.name: 74})["value"]

        url_merma="http://erpt.sugelico.com/?md=merma&merma="+str(item)
        bodymsg = "<h2>Productos mermados</h2>" \
                  "<p>" + \
                  " Colocado por el usuario: " + creator_profile["value"][0]["name"] \
                  + " Codigo del reverso: <a href='" + url_merma + "'>"+str(item)+"</a></p>"

        for user_root in user_rootlst:
            general().sendMail(user_root[User.username.name], bodymsg)
        return {"status": 200, "value": {Merma.code.name: item}, 'type': 'application/json'}

    def merma_addProd(self, inputs):
        self.code = inputs[Merma.code.name]
        # Generating the code.
        mermaprod_code= CodeGen().GenCode({"table": "MermaProd", "column": "code"})
        product =int(inputs["product"])

        MermaProd(code=mermaprod_code, product=product, amount=float(inputs["amount"]),
                  merma=self.code).save()

        equivalence = 1
        if "from_eq" in inputs:
            equivalence = int(str(inputs["from_eq"]).split(":")[0])
        unit = 517
        if "to_eq" in inputs:
            unit = int(inputs["to_eq"])

        amount = float(inputs["amount"])
        equivalence_data = Equivalence.objects(from_eq=equivalence, to_eq=unit)

        if equivalence_data != None:
            equivalence_info = equivalence_data.first()
            if equivalence_info.optype == "*":
                amount = float(equivalence_info.equivalence) * float(inputs["amount"])
            if equivalence_info.optype == "/":
                amount = float(equivalence_info.equivalence) / float(inputs["amount"])


        cur_amount = Items().Get({Item.code.name: inputs["product"]})["value"][0][Item.amount.name]

        if cur_amount == None or cur_amount == 'None':
            cur_amount = 0.00
        if (float(cur_amount)-amount)>=0:
            Items().Handle(
            {Item.code.name: inputs["product"], Item.amount.name:  float(cur_amount)-amount})
            return {"status": 200, "value": {"code": mermaprod_code}, 'type': 'application/json'}
        else:

            return {"status": 200, "value": {"error": "Cantidad a mermar, "
                                                      "no puede ser mayor a cantidad actual"},
                    'type': 'application/json'}


    def merma_Get(self, inputs):

        storeDict = self.session.query(Merma).filter_by(code = int(inputs["code"])).first()
        dataCol = []
        if storeDict!=None:
            dataDict ={Merma.merma_made.name:storeDict.merma_made,
                       Merma.code.name:storeDict.code,
                       Merma.description.name:storeDict.description,
                       Merma.created.name:general().julian2date(str(storeDict.created)),
                       Merma.created_by.name:login().getProfile({"usercode":storeDict.created_by})["value"]["name"]}

            productsMerma = MermaProd.objects(merma=storeDict.code)
            products = []
            for prodsInMerma in productsMerma:
                #MermaProd(code=mermaprod_code, product=product, amount=float(inputs["amount"]),
                #          merma=self.code).save()
                products.append({"code":prodsInMerma.mermaprod_code,
                                 "product_name":Items().Get({Item.code.name:prodsInMerma.product})
                                 ["value"][0][Item.item_name.name],
                                 "product":prodsInMerma.product, "amount":prodsInMerma.amount})
            dataDict["products"]=products
            dataCol.append(dataDict)

        return {"status": 200, "value": dataCol, 'type': 'application/json'}


    def getBuyItems(self, inputs):
        from_date = general().date2julian()
        if "from" in inputs:
            if len(inputs["from"]) > 4:
                from_date = general().date2julian(inputs["from"])

        end_date = general().date2julian()
        if "end" in inputs:
            if len(inputs["end"]) > 4:
                end_date = general().date2julian(inputs["end"])

        dataCol=[]
        category_filter=and_(Item.category>0)
        if "category" in inputs:
            if int(inputs["category"])>0:
                category_filter = and_(Item.category == int(inputs["category"]))

        products = self.session.query(Item.code).filter(category_filter).order_by(Item.item_name.asc())
        for piece_prod in products:
            for item in Buyitems.objects(created_date__gte=from_date,
                                         created_date__lte=end_date,
                                         product=piece_prod.code):

                item_info=Items().Get({Item.code.name:piece_prod.code})["value"]

                supplier_info = self.session.query(Supplier.sup_name).\
                        filter(buybills.code == item.bill).\
                        filter(buybills.supplier == Supplier.code).first()

                supplier_name=""
                if supplier_info!=None:
                    supplier_name=supplier_info[0]


                product_name=""
                unit_name = "Unidad"
                if len(item_info)>0:
                    product_name=item_info[0][Item.item_name.name]
                    unit_name = item_info[0]["unit_name"]

                dataCol.append({"bill":item.bill,"product":item.product, Item.item_name.name:product_name,
                                "bought_amount":float(item.amount),
                                "unit":unit_name,"date":general().julian2date(str(item.created_date)),
                                "bought_price": '{0:.2f}'.format(float(item.total)), "status":item.status,
                                "status_name":self.session.query(Status.name).
                               filter(Status.code==item.status).first()[0],
                                "supplier":supplier_name, "":item.to_json()})

        return {"status": 200, "value": dataCol, 'type': 'application/json'}


    def get606(self, inputs):
        from_date = general().date2julian(str(inputs["from_date"]))

        end_date=general().date2julian()
        if "end_date" in inputs:
            end_date=general().date2julian(str(inputs["end_date"]))

        self.msg=[]
        storeDict = self.session.query(buybills.generated,Supplier.sup_name, buybills.ncf,
                                       buybills.subtotal, buybills.total_tax, buybills.total,
                                       buybills.code, buybills.description,Supplier.rnc).\
            filter(Supplier.code == buybills.supplier).\
            filter(buybills.generated >= int(from_date)).\
            filter(buybills.generated <= int(end_date)).\
            order_by(Supplier.sup_name.asc(), buybills.generated.asc()).\
            group_by(Supplier.sup_name, buybills.generated, buybills.ncf,
                     buybills.subtotal, buybills.total_tax,
                     buybills.total,buybills.code, buybills.description,Supplier.rnc)

        for piece in storeDict:
            self.msg.append({buybills.generated.name:general().julian2date(str(piece[0])),
                             Supplier.sup_name.name:piece[1], buybills.ncf.name:piece[2],
                             buybills.subtotal.name:str(piece[3]), buybills.total_tax.name:str(piece[4]),
                             buybills.total.name: str(piece[5]), buybills.code.name:str(piece[6]),
                             buybills.description.name:str(piece[7]),Supplier.rnc.name:str(piece[8])})

        return {"status": 200, "value": self.msg, 'type': 'application/json'}



    def get607(self, inputs):
        from_date = general().date2julian(str(inputs["from_date"]))

        end_date=general().date2julian()
        if "end_date" in inputs:
            end_date=general().date2julian(str(inputs["end_date"]))


        details=self.session.query(SalesRep)
        if from_date == end_date:
            details= details.filter_by(billdate=from_date)
        else:

            details= details.\
                filter(SalesRep.billdate >= int(from_date)).\
                filter(SalesRep.billdate <= int(end_date))

        msg=[]
        details=details.order_by(SalesRep.billncf.asc())
        for piece in details:
            del piece.__dict__['_sa_instance_state']

            msg.append(piece.__dict__)


        self.msg={"details":msg, "total_ncf":len(msg), "total":cashbox_bills.objects(registred__gte=from_date,
                                            registred__lte=end_date).order_by("paytype+").sum('total')/1.28}
        return {"status": 200, "value": self.msg,
                'type': 'application/json'}


    def getBillsBy(self, inputs):
        _from_date = inputs["from"]
        _to_date = inputs["end"]

        from_date = int(general().date2julian(_from_date.split(" ")[0])) + 1
        to_date = int(general().date2julian(_to_date.split(" ")[0])) + 1
        if from_date == to_date:
            bills= self.session.query(BuyItemsRep).filter_by(or_billdate=from_date)
        else:
            bills = self.session.query(BuyItemsRep).\
                filter(BuyItemsRep.or_billdate >= from_date).\
                filter(BuyItemsRep.or_billdate <= to_date)

        if BuyItemsRep.billsupplier.name in inputs:
            if int(inputs[BuyItemsRep.billsupplier.name])>0:
                bills = bills.filter_by(billsupplier=int(inputs[BuyItemsRep.billsupplier.name]))
            else:
                bills = bills.filter(BuyItemsRep.billsupplier > int(inputs[BuyItemsRep.billsupplier.name]))
        if BuyItemsRep.sup_name.name in inputs:
            bills=bills.filter(BuyItemsRep.sup_name.ilike("%"+inputs[BuyItemsRep.sup_name.name]+"%"))

        if BuyItemsRep.sup_rnc.name in inputs:
            bills=bills.filter(BuyItemsRep.sup_rnc.ilike("%"+inputs[BuyItemsRep.sup_rnc.name]+"%"))



        data = bills.order_by(BuyItemsRep.billdate.asc())
        self.msg = []
        for piece in data:
            del piece.__dict__['_sa_instance_state']
            piece.__dict__[BuyItemsRep.billdate.name]=piece.__dict__[BuyItemsRep.billdate.name].strftime("%Y-%m-%d")
            piece.__dict__[BuyItemsRep.billexpires.name]=piece.__dict__[BuyItemsRep.billexpires.name].strftime("%Y-%m-%d")
            piece.__dict__[BuyItemsRep.billpayalert.name]=piece.__dict__[BuyItemsRep.billpayalert.name].strftime("%Y-%m-%d")

            piece.__dict__[BuyItemsRep.billsubtotal.name] = float(piece.__dict__[BuyItemsRep.billsubtotal.name])
            piece.__dict__[BuyItemsRep.billtotal.name] = float(piece.__dict__[BuyItemsRep.billtotal.name])
            piece.__dict__[BuyItemsRep.billtax.name] = float(piece.__dict__[BuyItemsRep.billtax.name])
            piece.__dict__[BuyItemsRep.billothercosts.name] = float(piece.__dict__[BuyItemsRep.billothercosts.name])
            self.msg.append(piece.__dict__)

        return {"status": 200, "value": self.msg, 'type': 'application/json'}




if __name__ == '__main__':
    print(Accounting().getBuyItems({"from":"01-01-2016", "end":"10-01-2016"}))
    # print(Accounting().addItem2Bill({"amount":"1","bill":"2",
    #                                  "classname":"Accounting.addItem2Bill","cur_amount":"",
    #                                  "discount":"0.00","from_eq":"51:Onza",
    #                                  "other_costs":"0.00","product":"235","subtotal":"0.00",
    #                                  "to_eq":"539","total":"0.00","total_tax":"0.00",
    #                                  "unit":"51","key":"57a883378f01b96f9e43ccee"}))

__author__ = 'hidura'
