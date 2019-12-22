import time
import json
from datetime import datetime
from decimal import Decimal
from mongoengine.queryset.visitor import Q
from sqlalchemy import func
from sqlalchemy.orm.session import sessionmaker
from sqlalchemy.sql.expression import and_

from tools.DataBase.CodeGenerator import CodeGen
from tools.DataBase.Connect import conection
from tools.DataBase.Definition.Base import db
from tools.DataBase.Definition.CashBox import CashBox
from tools.DataBase.Definition.Client import Client
from tools.DataBase.Definition.Contact import Contact
from tools.DataBase.Definition.Item import Item
from tools.DataBase.Definition.PayTypeBill import PayTypeBill
from tools.DataBase.Definition.Preparation import Preparation
from tools.DataBase.Definition.ProductReverse import ProductReverse
from tools.DataBase.Definition.Status import Status
from tools.DataBase.Definition.Tables import Tables
from tools.DataBase.Definition.Type import Type
from tools.DataBase.Definition.User import User
from tools.DataBase.Definition.Views.SalesDebt import SalesDebt
from tools.DataBase.Definition.Views.SalesRep import SalesRep
from tools.DataBase.Definition.PreOrder import PreOrder as preorder_tbl
from tools.DataBase.Definition.cashboxOpen import cashboxOpen
from tools.DataBase.Definition.category import category
from tools.DataBase.Definition.company import company
from tools.DataBase.Definition.ncf import NCF
from tools.DataBase.ODM.DataModelODM import PreOrder, PreOrderTable, ProductPre, \
    recipe_items, Buyitems, ncfType, ncf_codes, PreOrderProdDel, PrepProducts, ProductSale, InputSale, account_movement, \
    ConsumeDeferred, cashbox_open, cashbox_bills, Salebills_payment, Bill2Print, cashbox, discount, archieve_preorder, \
    rules_company, sysrules
from tools.DataBase.Process import DBProcess
from tools.main.general import general
from tools.main.process.Accounts import Accounts
from tools.main.process.Clients import Clients
from tools.main.process.Company import Company
from tools.main.process.General import General
from tools.main.process.Items import Items
from tools.main.process.login import login
from tools.DataBase.Definition.salebills import salebills


class Bills:
    def __init__(self):
        self.status = 200
        self.msg = None
        self.type = "text/plain"

        self.session = db.session
        self.engine = db.engine

    def create(self, inputs):
        # This method will create an expense.
        self.code = CodeGen().GenCode({"table": salebills.__tablename__, "column": salebills.code.name})
        # Generating the code.
        preorder = int(inputs["preorder"])
        billInfo=self.session.query(salebills).filter_by(preorder=preorder).first()
        if billInfo!=None:
            code=billInfo.code
            self.session.commit()
            return {"status": 200, "value": {salebills.code.name: code}, 'type': 'application/json'}

        self.session.add(salebills(code=self.code, status=21,
                                   preorder=preorder))

        # Saving
        self.session.commit()
        
        
        
        return {"status": 200, "value": {salebills.code.name: self.code}, 'type': 'application/json'}

    def Handle(self, inputs):
        # This method will modify an expanse.
        bill = int(inputs[salebills.code.name])
        storeDict = {}

        for column in DBProcess(salebills.salebills_tbl).getColumnDefinition:
            if column["name"] in inputs:
                storeDict[column["expr"]] = inputs[column["name"]]

        self.session.query(salebills).filter_by(code=bill).update(storeDict)

        self.session.commit()
        
        
        

        return {"status": 200, "value": {salebills.code.name: bill}, 'type': 'application/json'}

    def Get(self, inputs):
        # This method gets the data, from the db.
        storeDict = []
        if salebills.code.name in inputs:
            storeDict = self.session.query(salebills, Status.name, Type.type_name). \
                filter(and_(Status.code == salebills.status, salebills.code
                            == int(inputs[salebills.code.name])))

        # The next area is in charge to extract the information,
        # from the store Dict and add it to the dataCol to be returned

        dataCol = []

        for dataLst in storeDict:

            dicStore = {"status_name": dataLst.__dict__["name"], "type_name": dataLst.__dict__["type_name"]}

            for key in DBProcess(salebills.salebills_tbl).getColumnDefinition:
                dataDict = dataLst.__dict__[salebills.__name__].__dict__  # Getting the dictionary of the list.
                colname = key["name"]  # Getting the column name.
                if colname in dataDict:  # Just if the column name is on the dictionary, add it to the dictStore.
                    dicStore[colname] = DBProcess(salebills.salebills_tbl).parse2publish(dataDict[colname])

            dataCol.append(dicStore)
            # Appending everything to be returned
        
        
        
        return {"status": 200, "value": dataCol, 'type': 'application/json'}


    # Custom methods
    def openPreorder(self, inputs):


        connection = self.engine.raw_connection()
        cursor = connection.cursor()
        inputs['order_type']=inputs['billtype']
        inputs['created_date']=general().date2julian()

        cursor.callproc('addpreorder', [json.dumps(inputs)])
        data = cursor.fetchall()

        billinfo=json.loads(data[0][0])
        cursor.close()
        connection.commit()


        return {"status": 200, "value": {"preorder": billinfo['preorder'],
                                         "bill":billinfo['bill'],
                                         "tbl_name":billinfo['tbl_name']}, 'type': 'application/json'}



    def modPreorder(self, inputs):
        usercode = login().decLoginKey(inputs["key"])
        billType = int(inputs["billtype"])
        preorder = CodeGen().GenCode({"table": "PreOrder", "column": "code"})

        PreOrder.objects(code=preorder).\
            update(set__created_by=usercode,
                   status=int(inputs["status"])).save()
        if billType == 101:
            # When is for consume in the place the bill
            # have to come with a table to be assigned.
            table = int(inputs["table"])
            PreOrderTable.objects(preorder=preorder, table_code=table).\
                update(set__preorder=preorder, set__table_code=table, set__people_on=int(inputs["people_on"]),
                       set__status=int(inputs["status"]))
        
        
        
        return {"status": 200, "value": {"preorder", preorder}, 'type': 'application/json'}



    def delProductPreorder(self, inputs):
        usercode = login().decLoginKey(inputs["key"])
        profile_user = login().getProfile({"usercode":usercode})["value"]
        preorder = int(inputs["preorder"])

        product = int(inputs["products"])
        reason = str(inputs["reason"])
        preorder_product = int(inputs["preorder_product"])
        product_data=ProductPre.objects(code=preorder_product).first()

        amount = int(product_data["amount"])
        code = CodeGen().GenCode({"table":"PreOrderProdDel", "column":"code"})

        ProductPre.objects(code=preorder_product).update(set__status=30)

        PreOrderProdDel(code=code, preorder=preorder, product=product, amount=amount,
                        reason=reason, created_by=usercode,
                        created_date=general().date2julian()).save()

        connection = self.engine.raw_connection()
        cursor = connection.cursor()

        cursor.callproc('regdelproduct', [recipe_items.objects(recipe=product_data.product).to_json(),
                                          amount,usercode, product_data.product, preorder_product])
        data = list(cursor.fetchall())
        cursor.close()
        connection.commit()
        #Mandar la confirmacion del borrado a las cuentas root y admin.
        user_rootlst = login().Get({User.usrtype.name: 74})["value"]
        bodymsg = "<h2>Producto Borrado</h2><p>"
        bodymsg+="<p> Se le informa que el producto de nombre: %s, de cantidad:%s, fue eliminado por el usuario:" \
                 " %s el mismo estaba colocado en la orden: <strong>%s</strong> y fue por la razon: %s" \
                 "</p>"%(product_data.product_name,product_data.amount,profile_user["name"],str(preorder), reason)


        for user_root in user_rootlst:
            try:
                general().sendMail('Subject: %s\n\n%s' % ("Producto Borrado-NO REPLY-", bodymsg),
                                   user_root[User.username.name])
                None
            except Exception as ex:
                raise Exception(str(ex))

        
        
        

        return {"status": 200, "value": {"delorder": code, "user_added":profile_user["name"]}, 'type': 'application/json'}



    def approbedelProductPreorder(self, inputs):
        usercode = login().decLoginKey(inputs["key"])
        profile = login().getProfile(inputs)
        if profile["type"] == 71 or profile["type"] ==74:
            code = inputs["code"]

            PreOrderProdDel.objects(code=code).\
                update(set__status=17, set__approved_by=usercode)
            
            
            
            return {"status": 200, "value": {"preorder", code}, 'type': 'application/json'}
        else:
            
            
            
            return {"status": 200, "value":
                {"error", "Usuario no puede hacer esta operación"},
                    'type': 'application/json'}



    def rejectdelProductPreorder(self, inputs):
        usercode = login().decLoginKey(inputs["key"])
        profile = login().getProfile(inputs)
        if profile["type"] == 71 or profile["type"] == 74:
            code = inputs["code"]

            PreOrderProdDel.objects(code=code). \
                update(set__status=17, set__approved_by=usercode)
            
            
            
            return {"status": 200, "value": {"preorder", code}, 'type': 'application/json'}
        else:
            
            
            
            return {"status": 200, "value":
                {"error", "Usuario no puede hacer esta operación"},
                    'type': 'application/json'}




    def addProd2Preorder(self, inputs):
        # Method that add the product to the preorder.

        preorder = int(inputs["preorder"])
        usercode = int(inputs["usercode"]) if "usercode" in inputs else login().decLoginKey(inputs["key"])

        self.msg = []
        if "products" in inputs:
            products = json.loads(str(inputs["products"])) if isinstance(inputs["products"], str) else inputs["products"]

            for line in products:
                term = ""
                portion = ""
                notes = ""
                companion = ""
                product = 0
                amount = 0
                client = "Generico"

                if isinstance(line, dict):
                    piece=line
                    if "terms" in piece:
                        term = piece["terms"] if piece["terms"]!= None else ""

                    if "portion" in piece:
                        portion = piece["portion"] if piece["portion"] != None else ""

                    if "notes" in piece:
                        notes = piece["notes"] if piece["notes"] != None else ""

                    product =int(piece["Cod"]) if "Cod" in piece else int(piece["product"])

                    amount = Decimal(piece["Cnt"]) if "Cnt" in piece else Decimal(piece["amount"])


                    client = str(piece["client"]).upper() if "client" in piece else "GENERICO"
                    ProductPreCode = int(piece["ordercode"]) if "ordercode" in piece else \
                        int(str(inputs["preorder"])+str(CodeGen().GenCode({"table": "ProductPre", "column": "code"})))
                    piece["ordercode"]=ProductPreCode# It looks crazy but makes sense if the thing don't come will works
                    companion = str(piece["companion"]) if "companion" in piece else ""
                    piece["usercode"] = usercode
                    piece["preorder"]=preorder

                product_pre_info = ProductPre.objects(code=ProductPreCode).first()

                saleItem = self.session.query(Item).filter_by(code=product).first()

                subtotal = Decimal(saleItem.subtotal)*amount
                tax = ((Decimal(saleItem.tax)/100)*Decimal(saleItem.subtotal))*amount
                total = Decimal(saleItem.price)*amount

                now = datetime.now()
                curHour=general().get_sec(str(now.hour)+":"+str(now.minute)+":"+str(now.second))
                curday = str(now.weekday()+1)

                disc_info=discount.objects(product=product,start_hour__lte=int(curHour),end_hour__gte=int(curHour),
                                           days__icontains=curday).first()
                total_discount=0.00
                if disc_info!=None:
                    total_discount = disc_info.amount_disc*amount
                if product_pre_info == None:
                    product_name=saleItem.item_name

                    ProductPre(code=ProductPreCode, preorder=preorder, product=product, amount=amount,
                               notes=notes, term=term, portion=portion, companion=companion,
                               subtotal=subtotal, tax=tax,
                               created_hour=curHour,product_name=product_name,
                               total=total, discount=total_discount,
                               created_date=general().date2julian(),
                               created_by=usercode, client=client.capitalize()).save()
                else:
                    if product_pre_info["status"]==30:
                        product_name = saleItem.item_name
                        ProductPre(code=int(str(ProductPreCode)+"1"), preorder=preorder, product=product, amount=amount,
                                   notes=notes, term=term, portion=portion, companion=companion,
                                   subtotal=subtotal, tax=tax,
                                   created_hour=curHour, product_name=product_name,
                                   total=total, discount=total_discount,
                                   created_date=general().date2julian(),
                                   created_by=usercode, client=client.capitalize()).save()
                    else:
                        ProductPre.objects(code=ProductPreCode).update(set__preorder=preorder, set__product=product,
                                                                   set__amount=amount,
                                                                   set__notes=notes, set__term=term,
                                                                   set__portion=portion, set__companion=companion,
                                                                   set__subtotal=subtotal,
                                                                   set__tax=tax,
                                                                   created_hour=curHour,
                                                                   set__total=total,discount=total_discount,
                                                                   set__created_date=general().date2julian(),
                                                                   set__created_by=usercode, set__client=client.capitalize())
                self.msg.append(ProductPreCode)
            self.discAmountProducts(products)



        if "Cod" in inputs or "ordercode" in inputs:
            term = ""
            if "term" in inputs:
                term = inputs["term"]

            portion = ""
            if "portion" in inputs:
                portion = inputs["portion"]

            notes = ""
            if "notes" in inputs:
                notes = inputs["notes"]

            product = 0

            if "Cod" in inputs:
                product = int(inputs["Cod"])
            elif "product" in inputs:
                product = int(inputs["product"])

            amount = 0
            if "Cnt" in inputs:
                amount = int(inputs["Cnt"])
            elif "amount" in inputs:
                amount = int(inputs["amount"])

            client = "Generico"
            if "client" in inputs:
                client = str(inputs["client"])

            if "ordercode" in inputs:
                ProductPreCode = int(inputs["ordercode"])
            else:
                ProductPreCode = CodeGen().GenCode({"table": "ProductPre", "column": "code"})

            companion = ""
            if "companion" in inputs:
                companion = inputs["companion"]
            saleItem = self.session.query(Item).filter_by(code=product).first()

            subtotal = saleItem.subtotal * amount
            tax = saleItem.tax * amount
            total = saleItem.price * amount
            now = datetime.now()
            curHour = general().get_sec(str(now.hour) + ":" + str(now.minute) + ":" + str(now.second))
            curday = str(now.weekday() + 1)

            disc_info = discount.objects(product=product, start_hour__lte=int(curHour), end_hour__gte=int(curHour),
                                         days__icontains=curday).first()
            total_discount = 0.00
            if disc_info != None:
                total_discount = disc_info.amount_disc * amount

            ProductPre(code=ProductPreCode, preorder=preorder, product=product, amount=amount,
                       notes=notes, term=term, portion=portion, companion=companion,
                       subtotal=subtotal, tax=tax,
                       total=total,
                       created_hour=curHour,
                       created_date=general().date2julian(),
                       created_by=usercode, client=client).save()
            self.msg.append(ProductPreCode)
            #self.discAmountProducts(inputs)

        
        
        
        return {"status": 200, "value": self.msg, 'type': 'application/json'}

    def addProdudsOffline(self, inputs):
        # Even when says Offline is because the products are send when is an error.
        # Method that add the product to the preorder.

        usercode = int(inputs["usercode"]) if "usercode" in inputs else login().decLoginKey(inputs["key"])

        self.msg = []
        if "products" in inputs:
            products = json.loads(str(inputs["products"])) if isinstance(inputs["products"], str) else inputs["products"]

            for line in products:
                term = ""
                portion = ""
                notes = ""
                companion = ""
                product = 0
                amount = 0
                client = "Generico"


                piece=line
                if "terms" in piece:
                    term = piece["terms"] if piece["terms"]!= None else ""

                if "portion" in piece:
                    portion = piece["portion"] if piece["portion"] != None else ""

                if "notes" in piece:
                    notes = piece["notes"] if piece["notes"] != None else ""

                product =int(piece["Cod"]) if "Cod" in piece else int(piece["product"])

                amount = Decimal(piece["Cnt"]) if "Cnt" in piece else Decimal(piece["amount"])


                client = str(piece["client"]).upper() if "client" in piece else "GENERICO"
                ProductPreCode = int(piece["ordercode"]) if "ordercode" in piece else \
                    int(str(inputs["preorder"])+str(CodeGen().GenCode({"table": "ProductPre", "column": "code"})))

                companion = str(piece["companion"]) if "companion" in piece else ""
                piece["usercode"] = usercode

                product_pre_info = ProductPre.objects(code=ProductPreCode).first()

                saleItem = self.session.query(Item).filter_by(code=product).first()

                subtotal = Decimal(saleItem.subtotal)*amount
                tax = ((Decimal(saleItem.tax)/100)*Decimal(saleItem.subtotal))*amount
                total = Decimal(saleItem.price)*amount

                now = datetime.now()
                curHour=general().get_sec(str(now.hour)+":"+str(now.minute)+":"+str(now.second))
                curday = str(now.weekday()+1)

                disc_info=discount.objects(product=product,start_hour__lte=int(curHour),end_hour__gte=int(curHour),
                                           days__icontains=curday).first()
                total_discount=0.00
                if disc_info!=None:
                    total_discount = disc_info.amount_disc*amount
                if product_pre_info == None:
                    product_name=saleItem.item_name
                    ProductPre(code=ProductPreCode, preorder=piece["preorder"], product=product, amount=amount,
                               notes=notes, term=term, portion=portion, companion=companion,
                               subtotal=subtotal, tax=tax,
                               created_hour=curHour,product_name=product_name,
                               total=total, discount=total_discount,
                               created_date=general().date2julian(),
                               created_by=usercode, client=client.capitalize()).save()
                else:
                    if product_pre_info["status"]==30:
                        product_name = saleItem.item_name
                        ProductPre(code=int(str(ProductPreCode)+"1"), preorder=piece["preorder"],
                                   product=product, amount=amount,
                                   notes=notes, term=term, portion=portion, companion=companion,
                                   subtotal=subtotal, tax=tax,
                                   created_hour=curHour, product_name=product_name,
                                   total=total, discount=total_discount,
                                   created_date=general().date2julian(),
                                   created_by=usercode, client=client.capitalize()).save()
                    else:
                        ProductPre.objects(code=ProductPreCode).update(set__preorder=piece["preorder"],
                                                                       set__product=product,
                                                                   set__amount=amount,
                                                                   set__notes=notes, set__term=term,
                                                                   set__portion=portion, set__companion=companion,
                                                                   set__subtotal=subtotal,
                                                                   set__tax=tax,
                                                                   created_hour=curHour,
                                                                   set__total=total,discount=total_discount,
                                                                   set__created_date=general().date2julian(),
                                                                   set__created_by=usercode,
                                                                       set__client=client.capitalize())
                self.msg.append({"ordercode":ProductPreCode})
            self.discAmountProducts(products)




        
        
        
        return {"status": 200, "value": self.msg, 'type': 'application/json'}

    # Apply discount to products
    def applyDiscount2Prod(self, inputs):
        # To transfer a product, we need the id of the product and the ID of the preorder.
        for piece in inputs["product"].split("|"):

            product = ProductPre.objects(
                code=int(piece)).first()  # Extracting the product with the pre-order.
            if product != None:
                dataSale = ProductPre.objects(code=int(piece)).first()
                product_info = self.session.query(Item).filter_by(code=int(dataSale.product)).first()

                subtotal = dataSale.subtotal - float(inputs["discount"])
                total_tax = (product_info.tax / 100) * Decimal(subtotal)
                ProductPre.objects(code=int(piece)). \
                    update(set__discount=float(inputs["discount"]),
                           set__subtotal=subtotal, set__tax=total_tax,
                           set__total=(Decimal(total_tax) + Decimal(subtotal)))
                return {"status": 200,
                        "value": {"msg": "Descuento aplicado"},
                        'type': 'application/json'}
        
        
        
        return {"status": 200,
                "value": {"msg": "Debe colocar un producto"},
                'type': 'application/json'}

    def checkProdsCart(self, inputs):
        # The method to check if the products is saved in the database.
        if ProductPre.objects(code=int(inputs["product_code"])).first()!=None:
            return {"status": 200, "value": True, 'type': 'application/json'}
        else:
            return {"status": 200, "value": False, 'type': 'application/json'}


    def getProdsPreorder(self, inputs):
        self.msg = []
        products =[]

        if inputs["preorder"]!=None and "status" not in inputs:
            products = ProductPre.objects(preorder=int(inputs["preorder"]), status__gt=30, status__lt=34)

        elif "preorder" in inputs and "status" in inputs:
            products = ProductPre.objects(preorder=int(inputs["preorder"]), status=int(inputs["status"]))

        for piece in products:
            product_name = self.session.query(Item.item_name).filter_by(code=piece.product).first()
            if product_name!=None:
                self.msg.append({"code":piece.code, "Cod":piece.product,
                             "Name":product_name[0],"status":piece.status,
                             "product":piece.product, "Cnt":piece.amount, "notes":piece.notes, "terms":piece.term,
                             "portion":piece.portion, "subtotal":piece.subtotal,"discount":piece.discount,
                                 "tax":piece.tax, "total":piece.total, "client_name":str(piece.client).upper()})

        
        
        
        return {"status": 200, "value": self.msg, 'type': 'application/json'}


    def reverseBill(self, inputs):

        bill_query = self.session.query(salebills).\
            filter_by(preorder=int(inputs["preorder"]))
        if "code" in inputs:
            bill_query = bill_query.filter_by(code=int(inputs["code"]))

        bill_info = bill_query.first()

        if bill_info != None:

            ncf_codes.objects(code=bill_info.ncf).update(set__status=11)
            PreOrder.objects(code=bill_info.preorder).update(set__status=11)
            ProductPre.objects(preorder=bill_info.preorder, status=34).update(set__status=31)
            PreOrderTable.objects(preorder=bill_info.preorder).update(set__status=24)
            cashbox_bills.objects(bill=bill_info.code).delete()
            self.session.query(PayTypeBill).filter_by(bill=bill_info.code).delete()
            self.session.commit()
            billData = {salebills.client.name: None,
                        salebills.waiter.name: None,
                        salebills.subtotal.name: 0.00,
                        salebills.preorder.name: int(inputs["preorder"]),
                        salebills.code.name:bill_info.code,
                        salebills.tax.name: 0.00,
                        salebills.discount.name: 0.00,
                        salebills.total.name: 0.00,
                        salebills.ncf.name: None}

            self.Handle(billData)
        else:
            return {"status": 200, "value": {"msg": "No se encontro la preorden"}, 'type': 'application/json'}
        return {"status": 200, "value": {"msg":"Borrado exitosamente"}, 'type': 'application/json'}



    def getProdsHistPreorder(self, inputs):
        self.msg = []
        products =[]
        cashbox_bill_info=None
        if "preorder" in inputs:
            products = ProductPre.objects(preorder=int(inputs["preorder"]))
            cashbox_bill_info = cashbox_bills.objects(preorder=int(inputs["preorder"])).first()
        else:
            return {"status": 200, "value": {"msg":"No coloco la orden o la misma no existe"}, 'type': 'application/json'}

        produs=[]
        subtotal = 0.00
        tax = 0.00
        total = 0.00
        discount = 0.00
        ncf=cashbox_bill_info.ncf if cashbox_bill_info !=None else None
        for piece in products:
            product_name = self.session.query(Item.item_name).filter_by(code=piece.product).first()
            if product_name!=None:
                subtotal += piece.subtotal
                tax += piece.tax
                discount += piece.discount
                total += piece.total
                order_date=general().julian2date(str(piece.created_date))
                produs.append({"code":piece.code, "Cod":piece.product,
                               "waiter":login().getProfile({"usercode":piece.created_by})["value"]["name"],
                               "hour":time.strftime('%H:%M:%S', time.gmtime(piece.created_hour)) if piece.created_hour !=None else None,
                             "Name":product_name[0],"status":piece.status,
                               "date":str(order_date.year)+"-"+str(order_date.month)+"-"+str(order_date.day),
                             "product":piece.product, "Cnt":piece.amount, "notes":piece.notes, "terms":piece.term,
                             "portion":piece.portion, "subtotal":piece.subtotal,"discount":piece.discount,
                                 "tax":piece.tax, "total":piece.total, "client_name":piece.client})

        self.msg={"prods":produs,"ncf":ncf, "subtotal":subtotal,
                  "tax":tax, "total":total, "discount":discount}

        
        
        
        return {"status": 200, "value": self.msg, 'type': 'application/json'}

    def discAmountProducts(self, inputs):
        # Method that discount the products from the database
        # after beign save it the discount information,
        # when is sellit.
        product = 0
        for piece in inputs:
            product = int(piece["Cod"]) if "Cod" in piece else int(piece["product"])
            ordercode= int(piece["ordercode"]) if "ordercode" in piece else int(piece["ordercode"])
            amount = float(piece["Cnt"]) if "Cnt" in piece else float(piece["amount"])
            preorder=int(piece["preorder"])

            usercode = int(piece["usercode"]) if "usercode" in piece else login().decLoginKey(piece["key"])

            connection = self.engine.raw_connection()
            cursor = connection.cursor()

            cursor.callproc('decreaseItems', [recipe_items.objects(recipe=product).to_json(),amount,
                                              usercode, product,ordercode,preorder ])
            data = list(cursor.fetchall())
            cursor.close()
            connection.commit()
        return {"status": 200, "value": self.msg, 'type': 'application/json'}

    def closeAccount(self, inputs):
        # This is the method that pass the preorder to the bill.
        billcode = 0
        bill_info = None
        preorder = 0
        remaining = 0.00

        if salebills.preorder.name in inputs:
            preorder = int(inputs[salebills.preorder.name])
            bill_info = self.session.query(salebills). \
                filter(salebills.preorder == preorder).first()


        elif salebills.code.name in inputs:
            bill_info = self.session.query(salebills). \
                filter(salebills.preorder == int(inputs[salebills.code.name])).first()
        else:
            # Add a new preorder
            billData=self.openPreorder(inputs)

        self.msg = {"bill_close": 0}
        waiter = login().decLoginKey(inputs["waiter"])
        inputs['waiter'] = waiter

        cashbox_code = 0
        cashbox_info = cashbox.objects(user_owner=waiter).first()
        if cashbox_info != None:
            cashBoxcur = cashbox_open.objects.filter(
                Q(cashbox=cashbox_info.code) & (Q(status=11) | Q(status=17))).first()
            if cashBoxcur != None:
                cashbox_code = cashBoxcur.code

        if cashbox_code==0:
            return {"status": 200, "value": {"error":"Solo un usuario con caja abierta puede cerrar esta mesa."},
                    'type': 'application/json'}

        if "products" in inputs:
            self.addProd2Preorder(inputs)
            self.msg = {"bill_close": 0}


        if bill_info !=None:
            # Just update if the bill is recently open.
            billcode = bill_info.code
        else:
            billcode = self.create({"preorder": preorder})["value"][salebills.code.name]

        billtype = 121
        if "billtype" in inputs:
            billtype = int(inputs["billtype"])
            if billtype==101 or billtype==102 :
                # Temporary, is a mistake and Idk on how many system are.
                billtype=121

        ncf=None
        if billtype!=122:
            ncf_data = self.getNCF(inputs)
            if "error" in ncf_data["value"]:
                return ncf_data
            elif "ncf" in ncf_data["value"]:
                ncf = ncf_data["value"]["code"]

                if "exp" in ncf_data["value"]:
                    self.msg["exp"] = ncf_data["value"]["exp"] # For now the pc version use this
                    self.msg["ncf_exp"]=ncf_data["value"]["exp"] # The tablet version use this one.
                self.msg["ncf"] = "00000000" + ncf_data["value"]["ncf"]
                inputs["ncf"]=self.msg["ncf"]
                self.msg["ncf_type"] = ncf_data["value"]["name"]
                self.msg["ncf_title"] = ncf_data["value"]["name"]
        client_info = Clients().Get({Client.code.name: int(inputs["client"])})["value"][0]
        self.msg["client"] = client_info[Client.cl_name.name]
        self.msg["rnc"] = client_info[Client.rnc.name]

        time = datetime.time(datetime.now())
        if "time" in inputs:
            time = datetime.strptime(inputs["time"], '%I:%M:%S')

        date = int(general().date2julian())
        if "date" in inputs:
            date = int(general().date2julian(inputs["date"]))
        inputs["_date"]=date
        billtax=0.00
        if "tax" in inputs:
            billtax =float(inputs["tax"])

        inputs['waiter'] = waiter
        inputs["billcode"] = billcode
        inputs["date"]=date
        inputs["cashbox"] = cashbox_code

        billData = {salebills.preorder.name: preorder, salebills.client.name: int(inputs["client"]),

                    salebills.waiter.name: waiter, salebills.order_type.name: int(inputs["order_type"]),

                    salebills.billtype.name: billtype,

                    salebills.subtotal.name: Decimal(inputs["subtotal"]), salebills.tax.name: billtax,

                    salebills.discount.name: Decimal(inputs["discount"]),
                    salebills.total.name: Decimal(inputs["total"]),

                    salebills.ncf.name: ncf, salebills.code.name: billcode, salebills._time.name: time,
                    salebills._date.name: date,

                    salebills.cashbox.name: cashbox_code}

        if billtype == 122:
            billData[salebills.paytype.name] = 0

        self.Handle(billData)

        self.addPayment2Bill(inputs)


        if salebills.preorder.name in inputs:

            ProductPre.objects(client__iexact=str(inputs["client_name_pre"]).upper(), status__gt=30,
                               preorder=int(inputs["preorder"])).update(set__status=34)

            if ProductPre.objects(status__gt=30, status__lt=34, preorder=int(inputs["preorder"])).first() == None:
                # Just if there's any more product to be billed the preorder and the preordertable is closed.
                PreOrder.objects(code=int(inputs["preorder"])).update(set__status=12)
                PreOrderTable.objects(preorder=int(inputs["preorder"])).update(set__status=12)
                PreOrderTable.objects(preorder=int(inputs["preorder"]), status=24).delete()
                self.msg["bill_close"] = 1





        self.msg["billcode"] = billcode
        self.addSaleProduct(inputs)
        accounting_entry = account_movement.objects(notes="BillID|" + str(billcode)).first()
        if accounting_entry == None:
            if billtype==122:
                # If the amount is not going to set as a credit,
                # then the system have to put it in the account of cash
                Accounts().transfer({"account_to": 6,
                                     "amount": Decimal(inputs["total"]),
                                     "notes": "BillID|" + str(billcode)+"|"+
                                              inputs["client_name_pre"]})
                if int(inputs["client"]) > 1:
                    connection = self.engine.raw_connection()
                    cursor = connection.cursor()

                    cursor.callproc('addbilltoclient', [int(inputs["client"]), Decimal(inputs["total"])])
                    data = list(cursor.fetchall())
                    cursor.close()
                    connection.commit()
                    None
            else:
                # If the amount is not going to set as a credit, then
                # the system have to put it in the account of deferred
                Accounts().transfer({"account_to": 7,
                                     "amount": Decimal(inputs["total"]),
                                     "notes": "BillID|" + str(billcode)})

        
        
        

        return {"status": 200, "value": self.msg, 'type': 'application/json'}

    def addPayment2Bill(self, inputs):

        paylst = []
        paymentlst=[]
        paytp=json.dumps(str(inputs["paytypelst"])) if isinstance(inputs["paytypelst"], str) \
                                                      else inputs["paytypelst"]
        ncf = None
        if "ncf" in inputs:
            ncf = inputs["ncf"]
        for piece in paytp:
            if "|" not in piece:
                date = int(general().date2julian())
                paylst.append(cashbox_bills(cashbox=inputs["cashbox"],
                                            bill=inputs["billcode"],
                                            registred=date,
                                            total=paytp[piece],
                                            preorder=inputs["preorder"],
                                            ncf=ncf,
                                            paytype=piece))


                paymentlst.append({"paytype":piece, "total_paid":paytp[piece],"bill":inputs["billcode"],
                               "billtype":inputs["billtype"], "cashbox":inputs["cashbox"],
                               "registred":inputs["_date"],"ncf":ncf, "total":inputs["total"],
                               "subtotal":inputs["subtotal"],
                               "tax":inputs["tax"], "extra":inputs["billtp_extra"], "_desc":inputs["discount"],
                               "client":inputs["client"]})


        connection = self.engine.raw_connection()
        cursor = connection.cursor()

        cursor.callproc('addpayments', [json.dumps(paymentlst)])
        data = list(cursor.fetchall())
        cursor.close()
        if len(paylst) > 0:
            cashbox_bills.objects.insert(paylst)
        connection.commit()
        
        
        

        return {"status": 200, "value": self.msg, 'type': 'application/json'}


    def ClosePeriod(self, inputs):

        bills = cashbox_bills.objects(cashbox=General().getCashBox(inputs), printed=0)
        billsLst={}
        for bill in bills:
            payments = Salebills_payment.objects(bill=bill.bill)
            for payment in payments:
                if payment !=None:
                    if str(payment.pay_type) not in billsLst:
                        billsLst[str(payment.pay_type)] = [payment.total]
                    else:
                        billsLst[str(payment.pay_type)].append(payment.total)
        
        
        
        return {"status": 200, "value": billsLst, 'type': 'application/json'}



    def discountDeferred(self, inputs):
        # Mark the discount of the differed
        if int(inputs["client"]) > 1:
            client_info = Clients().Get({Client.code.name: int(inputs["client"])})["value"][0]
            if float(client_info["credit"]) >=float(inputs["total"]):
                code = CodeGen().GenCode({"table": "ConsumeDeferred",
                                          "column": "code"})
                date = int(general().date2julian())
                if "date" in inputs:
                    date = int(general().date2julian(inputs["date"]))

                ConsumeDeferred(code=code, client=client_info["code"],
                                amount_consumed=float(inputs["total"]),
                                product_consumed=int(inputs["product"]),
                                consume_date=date, registred_by=login().decLoginKey(inputs["key"])).save()

                # Sending the money from the Deffered account to cashbox account.
                Accounts().transfer({"account_from": 7,
                                     "account_to": 4,
                                     "amount": Decimal(inputs["total"]),
                                     "notes": "Cosumo diferido a cliente:"
                                              + client_info["cl_name"] + ",Ref:"})

                self.addSaleProduct(inputs)
                Clients().HandleClient({Client.code.name: int(inputs["client"]),
                                        Client.credit.name: float(client_info["credit"])- float(inputs["total"])})
                self.msg={"msg":"Cliente agregado, exitosamente"}
            else:
                self.msg={"msg":"Cliente no tiene monto suficiente, para realizar esta operacion."}
            
            
            
            return {"status": 200, "value": self.msg, 'type': 'application/json'}
        self.msg={"msg":"No marco un cliente"}
        
        
        
        return {"status": 200, "value": self.msg, 'type': 'application/json'}


    def addSaleProduct(self, inputs):

        usercode = inputs["waiter"]
        cashbox = int(inputs["cashbox"])
        preorder=int(inputs["preorder"])
        if salebills.preorder.name in inputs:
            # This mean that the system did a inderect bill, so the preorder is the one
            # Which did the discount of the amount to the products.
            for product_pre in ProductPre.objects(preorder=preorder, status=34):
                product_name = ""
                saleItem = self.session.query(Item).filter_by(code=product_pre.product).first()
                product_name = saleItem.item_name
                code = CodeGen().GenCode({"table": "Buyitems",
                                          "column": "code"})
                if ProductSale.objects(product_precode=product_pre.code).first()==None:
                    ProductSale(code=code, preorder=preorder, product=product_pre.product,
                                product_name=product_name,cashbox=cashbox,product_precode=product_pre.code,
                             amount=product_pre.amount, notes=product_pre.notes, term=product_pre.term,
                             portion=product_pre.portion, subtotal=product_pre.subtotal, tax=product_pre.tax,
                             total=product_pre.total, status=product_pre.status, created_date=general().date2julian(),
                             created_by=1, bill=int(inputs["billcode"])).save()
        elif "products" in inputs:
            # This means that the system is going to make a direct bill.
            for product_pre in inputs["products"]:
                code = CodeGen().GenCode({"table": "Buyitems",
                                          "column": "code"})

                ProductSale(code=code, preorder=0, product=product_pre["code"],
                         amount=float(product_pre["amount"]), notes=product_pre["notes"], term=product_pre["term"],
                         portion=product_pre["portion"], subtotal=float(product_pre["subtotal"]), tax=float(product_pre["tax"]),
                         total=product_pre["total"], status=11, created_date=general().date2julian(),
                         created_by=1, bill=int(inputs["billcode"])).save()

        
        
        
        #ProductPre.objects(preorder=int(inputs["preorder"])).delete()

    def getCashBox(self, inputs):

        if "alluser" not in inputs:
            _query = self.session.query(salebills, Contact.contact_name).\
                filter(User.code==salebills.waiter).\
                filter(User.contact==Contact.code).\
                filter(salebills.waiter == login().decLoginKey(inputs["key"]))
        else:
            _query = self.session.query(salebills, Contact.contact_name).\
                filter(User.code==salebills.waiter).\
                filter(User.contact==Contact.code)
        _from_date = inputs["from_date"]
        _to_date = inputs["to_date"]
        from_hour = datetime.strptime("12:01:00", "%H:%M:%S")
        to_hour = datetime.strptime("23:59:59", "%H:%M:%S")
        if len(inputs["from_date"].split(" "))>2:
            from_hour = datetime.strptime(_from_date.split(" ")[1], "%H:%M:%S")
        if len(inputs["to_date"].split(" "))>2:
            to_hour = datetime.strptime(_to_date.split(" ")[1], "%H:%M:%S")

        from_date = int(general().date2julian(_from_date.split(" ")[0]))
        to_date = int(general().date2julian(_to_date.split(" ")[0]))

        if from_date == to_date:
            _query= _query.filter(salebills._date == from_date)
        else:
            _query= _query.filter(salebills._date >= from_date).filter(salebills._date < to_date)
        data = _query

        self.msg = []
        total = 0.00
        tax = 0.00
        subtotal = 0.00
        tip = 0.00
        for dataPiece in data:
            piece = dataPiece[0]
            cashier=dataPiece[1]
            #Fill all the self.msg as dictionary.
            tblname=""
            total += float(piece.total)
            subtotal+=float(piece.subtotal)
            tax+=float(piece.tax)
            tip+=float(piece.subtotal)*0.1
            billDict={
                "code":piece.code,
                "total":str(piece.total),
                "subtotal":str(piece.subtotal),
                "tip":str(float(piece.subtotal)*0.1),
                "tax":str(piece.tax),
                "paytype": piece.paytype,
                "paytype_name": self.session.query(Type).
                    filter(Type.code == piece.paytype).first().tpname,
                "billtype": piece.paytype,
                "billtype_name": self.session.query(Type).
                    filter(Type.code == piece.billtype).first().tpname,
                "date":general().julian2date(str(piece._date))}


            self.msg.append(billDict)

        
        
        
        return {"status": 200, "value": {"details":self.msg,"total":str(total),
                                         "tip":tip,"subtotal":subtotal,
                                         "tax":tax},'type': 'application/json'}



    def getCashBoxBills(self, inputs):
        _from_date = inputs["from"]
        _to_date = inputs["end"]
        from_hour = datetime.strptime("12:01:00", "%H:%M:%S")
        to_hour = datetime.strptime("23:59:59", "%H:%M:%S")
        if len(_from_date.split(" "))>2:
            from_hour = datetime.strptime(_from_date.split(" ")[1], "%H:%M:%S")
        if len(_to_date.split(" "))>2:
            to_hour = datetime.strptime(_to_date.split(" ")[1], "%H:%M:%S")

        from_date = int(general().date2julian(_from_date.split(" ")[0]))
        to_date = int(general().date2julian(_to_date.split(" ")[0]))


        if from_date == to_date:
            _query= self.session.query(SalesRep).filter_by(billdate=from_date)
        else:

            _query= self.session.query(SalesRep).\
                filter(SalesRep.billdate >= from_date).\
                filter(SalesRep.billdate <= to_date)

        if "user" in inputs:
            _query = _query.filter(SalesRep.billuser==int(inputs["user"]))
        data = _query
        self.msg=[]
        for piece in data:
            del piece.__dict__['_sa_instance_state']
            self.msg.append(piece.__dict__)

        
        
        
        return {"status": 200, "value": self.msg,'type': 'application/json'}

    def getBills(self, inputs):
        _from_date = inputs["from"]
        _to_date = inputs["end"]


        from_date = int(general().date2julian(_from_date.split(" ")[0]))+1
        to_date = int(general().date2julian(_to_date.split(" ")[0]))+1


        if from_date == to_date:
            _query= self.session.query(salebills).filter_by(_date=from_date)
        else:
            _query= self.session.query(salebills).\
                filter(salebills._date > from_date)
        data = _query.all()
        self.msg=[]
        for piece in data:
            print(piece)
            del piece.__dict__['_sa_instance_state']
            self.msg.append(piece.__Publish__())


        
        
        
        return {"status": 200, "value": self.msg,'type': 'application/json'}


    def getNCF(self, inputs):
        # Method that make a reversal of the discount of the product in orther to add or just delete a sale
        # the products from the database.
        # when is sellit.

        if "ncf_type" in inputs and "client_type" not in inputs and "company" not in inputs:
            if inputs["ncf_type"]!="00":
                _ncf_type = ncfType.objects(_type=str(inputs["ncf_type"])).first()
                ncf_serie = ncf_codes.objects(ncf_type=_ncf_type.code, status=11).order_by("+code")\
                    .first()
                ncf_serie = self.session.query(NCF).filter(NCF.ncf_type==int(inputs['ncf_type'])).first()
                if ncf_serie == None:
                    return {"status": 200, "value": {"error": "Acorde con la ley de Republica Dominicana, no puede "
                                                              "facturar sin comprobante. No existen mas comprobantes "
                                                              "de este tipo, debe volver colocar mas o elegir otro tipo."},
                            'type': 'application/json'}
                else:
                    if (ncf_serie.cur_number+1)>ncf_serie.ncf_limit:
                        return {"status": 200, "value": {"error": "Acorde con la ley de Republica Dominicana, no puede "
                                                                  "facturar sin comprobante. No existen mas comprobantes "
                                                                  "de este tipo, debe volver colocar mas o elegir otro tipo."},
                                'type': 'application/json'}


                    new_curnumber=ncf_serie.cur_number+1
                    ncf_serie.update({NCF.cur_number:new_curnumber})
                    self.session.commit()
                    return {"status": 200, "value":
                        {"ncf": _ncf_type.header + ncf_serie.secuence,
                         "code": ncf_serie.code, "status": ncf_serie.status,
                         "name": _ncf_type.name, "exp": ncf_serie.exp},
                            'type': 'application/json'}
            else:
                return {"status": 200, "value":{},
                        'type': 'application/json'}


        elif "client_type" in inputs and "company" in inputs:

            ncf_rule = sysrules.objects(name="ncf").first()
            if ncf_rule!=None:
                ncf_cmp_rule = rules_company.objects(company_code=int(inputs["company"]),
                                                     rule_code=ncf_rule.code).first()

                if ncf_cmp_rule != None:
                    _ncf_type = ncfType.objects(_type=str(inputs["client_type"])).first()
                    ncf_serie = ncf_codes.objects(ncf_type=_ncf_type.code, status=11).order_by("+code") \
                        .first()
                    if ncf_serie == None:
                        return {"status": 200, "value": {"error": "Acorde con la ley de Republica Dominicana, no puede "
                                                                  "facturar sin comprobante. No existen mas comprobantes "
                                                                  "de este tipo, debe volver colocar mas o elegir otro tipo."},
                                'type': 'application/json'}
                    else:
                        ncf_codes.objects(code=ncf_serie.code).update(set__status=15)
                        return {"status": 200, "value":
                            {"ncf": _ncf_type.header + ncf_serie.secuence,
                             "code": ncf_serie.code, "status": ncf_serie.status,
                             "name": _ncf_type.name, "exp": ncf_serie.exp},
                                'type': 'application/json'}
                else:
                    return {"status": 200, "value":{},
                            'type': 'application/json'}
            else:
                return {"status": 200, "value":
                    {},
                        'type': 'application/json'}
        else:
            return {"status": 200, "value": {},
                    'type': 'application/json'}




    def delProductfromBill(self, inputs):
        code = CodeGen().GenCode({"table":ProductReverse.__tablename__,
                                  "column":ProductReverse.code.name})
        time = datetime.time(datetime.now())
        if "time" in inputs:
            time = general().get_sec(str(datetime.strptime(inputs["time"], '%I:%M:%S').hour)+":"+
                                     str(datetime.strptime(inputs["time"], '%I:%M:%S').minute) + ":" +
                                     str(datetime.strptime(inputs["time"], '%I:%M:%S').second))
        status = 16
        if "status" in inputs:
            status=int(inputs["status"])
        usercode=login().decLoginKey(inputs["key"])
        self.session.add(ProductReverse(code=code, created_by=usercode,
                                        created_date=int(general().date2julian(inputs["date"])),
                                        _time=time,
                                        preorder=int(inputs["preorder"]),
                                        product=int(inputs["product"]),
                                        reason=inputs["reason"], status=status))


        self.session.commit()
        product_pre_info = ProductPre.objects(code=int(inputs["prodorder_code"])).first()
        if product_pre_info!=None:
            ProductPre.objects(code=int(inputs["prodorder_code"])).update(set__status=30)

            
            
            delete_by_profile = login().getProfile(inputs)
            creator_profile = login().getProfile({"usercode":product_pre_info.created_by})
            # Send the mail of the product eliminated.
            user_rootlst = login().Get({User.usrtype.name:74})["value"]
            item_name = self.session.query(Item.item_name).filter_by(code=int(inputs["product"])).first()[0]


            return {"status": 200, "value": {"code":
                                                 code,
                                             "waiter_name":
                                                 str(creator_profile["value"]["name"])},
                'type': 'application/json'}
        else:
            
            return {"status": 200, "value": {"error": "No existe ese producto a borrar"},
                    'type': 'application/json'}



    def create_preparation(self, inputs):
        self.code = CodeGen().GenCode({"table": Preparation.__tablename__, "column": Preparation.code.name})
        # Generating the code.

        self.session.add(Preparation(code=self.code, status=12,
                               created_by=login().decLoginKey(inputs["key"])))
        # Saving
        self.session.commit()
        
        
        return {"status": 200, "value": {"code": self.code}, 'type': 'application/json'}



    def prep_Handle(self, inputs):
        item = int(inputs[Preparation.code.name])
        storeDict = {}
        for column in DBProcess(Preparation.Preparation_tbl).getColumnDefinition:

            if column["name"] in [Preparation.created.name] and column["name"] in inputs:
                jdate = general().date2julian(inputs[column["name"]])
                inputs[column["name"]] = jdate

            if column["name"] in inputs:
                storeDict[column["expr"]] = DBProcess(Preparation.Preparation_tbl).parse(column, inputs[column["name"]])

        self.session.query(Preparation).filter_by(code=item).update(storeDict)
        self.session.commit()
        
        


        return {"status": 200, "value": {Preparation.code.name: item}, 'type': 'application/json'}

    def prepProduct(self, inputs):
        preparation = int(inputs["preparation"])
        prepCode = CodeGen().GenCode({"table": "PrepProduct", "column": "code"})

        PrepProducts(preparation=preparation, code=prepCode, product=int(inputs["product"]),
                     amount=float(inputs["amount"]), services=float(inputs["services"]),
                     created_date=int(general().date2julian()), description=inputs["description"]).save()
        self.session.commit()
        
        


    def GetSales(self, inputs):
        # This method gets the data, from the db.
        from_date = general().date2julian()
        if "from" in inputs:
            if len(inputs["from"])>4:
                from_date =general().date2julian(inputs["from"])

        end_date = general().date2julian()
        if "end" in inputs:
            if len(inputs["end"])>4:
                end_date =general().date2julian(inputs["end"])


        # The next area is in charge to extract the information,
        # from the store Dict and add it to the dataCol to be returned

        prodlst = self.session.query(Item, category, Type).\
            filter(Item.category==category.code) .\
            filter(Item.unit==Type.code) .\
            filter(Item.item_type==int(inputs[Item.item_type.name])).\
            filter(category.type_product==int(inputs['type_product']))
        msg=[]
        for product_data in prodlst:
            amount = 0
            product_info={Item.item_name.name: product_data[0].__Publish__()[Item.item_name.name],
                          Item.code.name: product_data[0].__Publish__()[Item.code.name],
                          Item.amount.name: product_data[0].__Publish__()[Item.amount.name],
                          Item.price.name: product_data[0].__Publish__()[Item.price.name],
                          "unit_name": product_data[2].__Publish__()[Type.tpname.name],}
            if int(inputs[Item.item_type.name])==41:
                amount = ProductSale.objects(product=int(product_info[Item.code.name]), created_date__lte=end_date,
                                                 created_date__gte=from_date).sum("amount")
            elif int(inputs[Item.item_type.name]) == 42:
                amount = InputSale.objects(product=int(product_info[Item.code.name]), created_date__lte=end_date,
                                             created_date__gte=from_date).sum("amount")
            else:
                amount = ProductSale.objects(product=int(product_info[Item.code.name]), created_date__lte=end_date,
                                             created_date__gte=from_date).sum("amount")
            buyitems=Buyitems.\
                objects(product=product_info[Item.code.name],
                        created_date__lte=end_date,
                        created_date__gte=from_date)
            amount_buy=0
            for piece_amount in buyitems:
                amount_buy+=piece_amount.amount

            product_info["sale_amount"]= amount
            product_info["buys_amount"]= amount_buy
            msg.append(product_info)



        return {"status": 200, "value": msg, 'type': 'application/json'}


    def openCashBox(self, inputs):
        # Finding the cashbox of the user if is open will give an error.
        cashBox_info = self.session.query(cashboxOpen).\
            filter(cashboxOpen.cashbox==int(inputs["cashbox"])).\
            filter(cashboxOpen.status==11).first()

        if cashBox_info==None:
                amount_open = Decimal(inputs["amount_open"])
                code = CodeGen().GenCode({"table": "cashbox_open", "column": "code"})

                self.session.add(cashboxOpen(code=code, cashbox=int(inputs["cashbox"]),
                                              open_amount=amount_open,open_date=general().date2julian(),
                                              close_date=0.00,close_amount=0.00,status=11))
                self.session.commit()
        else:
            
            return {"status": 500,
                    "value": {"error": "Debe cerrar la caja "
                                       "del dia anterior para comenzar otra."},
                    'type': 'application/json'}

        
        return {"status": 200, "value": {"code":code}, 'type': 'application/json'}

    def transfercashbox(self, inputs):
        self.msg={}

        cashbox_original=int(inputs["cashbox_original"])
        cashbox_destiny=int(inputs["cashbox_destiny"])
        PreOrder.objects(cashbox=cashbox_original, status=11).update(set__cashbox=cashbox_destiny)
        self.msg["msg"] = "Ordenes transferidas, puede proseguir con el cierre"

        return {"status": 200, "value": self.msg, 'type': 'application/json'}

    def addCashBox(self, inputs):
        # This method will add a cashbox to a user.
        usercode=int(inputs["usercode"])

        name = inputs["name"]
        code = CodeGen().GenCode({"table": "cashbox", "column": "code"})


        #cashbox(_name=name, user_owner=usercode, code=code, warehouse=int(inputs["warehouse"]), branch=int(inputs["branch"]),
        #        status=11, description=inputs["description"]).save()

        self.session.add(CashBox(_name=name, usercode=usercode, code=code, warehouse=int(inputs["warehouse"]), branch=int(inputs["branch"]),
                status=11))


        self.session.commit()

        
        return {"status": 200, "value": {"code": code}, 'type': 'application/json'}






    def closeCashBox(self, inputs):
        self.msg = {}
        if inputs["cashbox"]==None:
            self.msg["error"] = "Usuario sin caja creada, no puede cerrar una caja inexistente"
            
            
            
            return {"status": 200,
                    "value": self.msg,
                    'type': 'application/json'}
        cashbox_info = cashbox_open.objects(code=int(inputs["cashbox"]), status=11).first()
        if cashbox_info == None:
            cashbox_info=cashbox_open.objects(code=int(inputs["cashbox"]), status=17).first()
        if cashbox_info == None:
            self.msg["error"] = "Caja cerrada, favor abrir otra."
            
            
            
            return {"status": 200,
                    "value": self.msg,
                    'type': 'application/json'}
        initial = cashbox_info.amount_open
        final_amount = 0.00
        subtotal=0.00
        bill_lst = {}

        initial = cashbox_info.amount_open
        cashbox_code=cashbox_info.code
        # Get all the bills with the cashbox_id.
        productsInCashBox=self.closeCashBoxProds(inputs)
        products_inBill = productsInCashBox["value"]
        products_inBillMail=productsInCashBox["product_data"]
        cxc_inBills = self.cxcCloseCashBox({"cashbox":cashbox_code})
        bills = self.session.query(SalesRep).\
            filter_by(billcashbox=cashbox_code).\
            filter_by(billbilltp=121).\
            order_by(SalesRep.paytpname.asc())

        bills_inBill = [" ", "FACTURAS", " ", " "]
        subtotal_tp=0.00
        for piece in bills:
            final_amount += float(piece.billtotal)


            if piece.billpaytp in bill_lst:

                billLst = bill_lst[piece.billpaytp]
            else:
                bills_inBill.append("<tr><td colspan='3'><strong>SUB TOTAL: </strong></td><td>" +
                                    '{0:,.2f}'.format(subtotal)+"</td></tr>")

                subtotal_tp=0.00
                billLst=[]
                bill_lst[piece.billpaytp] = billLst

            sub_total_bill = piece.billsubtotal
            subtotal += float(sub_total_bill)

            billLst.append({salebills.total.name : piece.billtotal,
                            salebills.subtotal.name : sub_total_bill,
                "paytype": piece.billpaytp,
                "paytype_name": piece.paytpname,
                "date":general().julian2date(str(piece.billdate)),
                "preorder":piece.billpreorder})

            billStr = "<tr><td colspan='3'>"+str(piece.billpreorder) + "</td>  <td>" + \
                      '{0:,.2f}'.format(float(piece.billsubtotal))+"</td>"

            subtotal_tp +=float(piece.billsubtotal)
            if float(piece.billdisc) > 0:
                billStr += "<td><strong>Descuento</strong></td><td>" + '{0:,.2f}'.format(float(piece.billdisc))+"</td>"
            else:
                billStr += "<td>Descuento de: </td><td>0.00</td>"
            bills_inBill.append(billStr+"</tr>")





        close_cashbox = 0
        if "close_cashbox" in inputs:
            close_cashbox = int(inputs["close_cashbox"])

        status_cashbox = "Caja sin cerrar"

        if close_cashbox == 1:
            # If the command to close the cashbox is 1
            # the system try to find any preorder pending,
            # and if has no preorders then close the cashbox.
            # Otherwise if the close_cashbox is 0,
            # or is not on the inputs then just return just the information.
            preorders = PreOrder.objects(cashbox=int(inputs["cashbox"]), status=11).first()
            anotherOpenBox = cashbox_open.objects(status=11, cashbox__ne=int(inputs["cashbox"])).first()

            if preorders != None and anotherOpenBox ==None:
                self.msg["error"] = "Tiene mesas abiertas, no puede " \
                                    "cerrar la caja hasta que no cierre " \
                                    " todas las ordenes atachadas"
                status_cashbox=self.msg["error"]
                cashbox_open.objects(code=cashbox_info.code).update(set__status=17)
            elif preorders != None and anotherOpenBox !=None:
                self.msg["msg_warning"] = "Otro usuario inicio su caja, " \
                                          "desea pasar las mesas abiertas al " \
                                          " otro usuario?"
                status_cashbox = "Caja no pudo ser cerrada por ordenes abiertas"
                cashbox_open.objects(code=cashbox_info.code).update(set__status=17)
                # Collecting the cashbox opens
                self.msg["cashboxes"] =[]
                for cashbox_data in cashbox_open.objects(status=11, cashbox__ne=int(inputs["cashbox"])):
                    self.msg["cashboxes"].append(login().
                                                 getProfile({"usercode":cashbox.
                                                            objects(code=cashbox_data.cashbox).
                                                            first().user_owner})["value"]["name"]+"-"+
                                                 str(cashbox_data.code))

            else:
                cashbox_open.objects(code=cashbox_info.code).update(set__status=14,
                                                                    set__amount_close=final_amount,
                                                                    set__close_date=general().date2julian())

                status_cashbox = "Caja cerrada"
        self.sendCashBoxMail({"products":products_inBillMail, "bills":bills_inBill, "cxc":cxc_inBills["mail_data"],
                              "cashbox":cashbox_info,"final_amount":final_amount,"status":status_cashbox})
        self.msg["code"] = cashbox_code
        self.msg["initial"] = initial
        self.msg["bills"] = bill_lst
        self.msg["products"] = products_inBill
        self.msg["cxclist"]= cxc_inBills["value"]
        self.msg["opened"] = general().julian2date(str(cashbox_info.open_date))
        self.msg["closed"] = ""
        self.msg["sub_total"] = subtotal
        self.msg["final_amount"] = final_amount
        
        
        
        return {"status": 200,
                "value": self.msg,
                'type': 'application/json'}

    def closeCashBoxTab(self, inputs):
        self.msg = {}
        status_cashbox = "Caja sin cerrar"
        if inputs["cashbox"] == None:
            self.msg["error"] = "Usuario sin caja creada, no puede cerrar una caja inexistente"
            
            
            
            return {"status": 200,
                    "value": self.msg,
                    'type': 'application/json'}
        cashbox_info = cashbox_open.objects(code=int(inputs["cashbox"]), status=11).first()
        if cashbox_info == None:
            cashbox_info = cashbox_open.objects(code=int(inputs["cashbox"]), status=17).first()
        if cashbox_info == None:
            self.msg["error"] = "Usuario sin caja abierta"
            
            
            
            return {"status": 200,
                    "value": self.msg,
                    'type': 'application/json'}
        initial = cashbox_info.amount_open
        final_amount = 0.00
        final_subtotal = 0.00
        final_tax = 0.00
        bill_lst = [" ", "FACTURAS", " ", " "]
        initial = cashbox_info.amount_open

        final_amount = 0.00
        cashbox_code = cashbox_info.code
        # Get all the bills with the cashbox_id.
        productsInCashBox = self.closeCashBoxProds(inputs)
        products_inBill = productsInCashBox["value"]
        products_inBillMail = productsInCashBox["product_data"]
        cxc_inBills = self.cxcCloseCashBox({"cashbox": cashbox_code})
        bills = self.session.query(SalesRep). \
            filter_by(billcashbox=cashbox_code). \
            filter_by(billbilltp=121). \
            order_by(SalesRep.ptppaytype_id.asc())

        bills_inBill = []
        curpaytype = None

        total_paytype = 0.00
        for piece in bills:
            if piece != None:
                if curpaytype == None:
                    if piece.paytpname != None:
                        bills_inBill.append("<tr><td colspan='4'><strong>" + piece.paytpname + "</strong></td></tr>")
                        bill_lst.append(piece.paytpname)
                elif curpaytype != piece.ptppaytype_id and curpaytype != None:
                    payTpInfo = self.session.query(func.sum(SalesRep.ptpaid).label("total")). \
                        filter_by(billcashbox=cashbox_code). \
                        filter_by(billbilltp=121). \
                        filter_by(ptppaytype_id=curpaytype).first()
                    if payTpInfo != None:
                        bill_lst.append("TOTAL: " + '{0:,.2f}'.format(float(payTpInfo[0])))

                        bills_inBill.append("<tr><td colspan='3'><strong>TOTAL: </strong></td><td>" +
                                            '{0:,.2f}'.format(float(payTpInfo[0])) + "</td></tr>")
                    bill_lst.append("")
                    bill_lst.append("")
                    bill_lst.append(piece.paytpname)
                    bills_inBill.append("<tr><td colspan='4'><strong>" + piece.paytpname + "</strong></td></tr>")
                curpaytype = piece.ptppaytype_id

                total_paytype = 0.00
                sub_total_bill = float(piece.ptpaid)
                discount_total_bill = float(piece.billdisc)

                total_paytype += float(piece.ptpaid)
                final_amount+=total_paytype
                billStr = str(piece.billpreorder) + "  " + '{0:,.2f}'.format(sub_total_bill)
                if discount_total_bill > 0:
                    billStr += " - Descuento de: " + '{0:,.2f}'.format(discount_total_bill)
                bill_lst.append(billStr)

                billStr = "<tr><td colspan='3'>" + str(piece.billpreorder) + "</td>  <td>" + \
                          '{0:,.2f}'.format(float(piece.ptpaid)) + "</td>"

                if float(piece.billdisc) > 0:
                    billStr += "<td><strong>Descuento</strong></td><td>" + '{0:,.2f}'.format(
                        float(piece.billdisc)) + "</td>"
                else:
                    billStr += "<td>Descuento </td><td>0.00</td>"
                bills_inBill.append(billStr + "</tr>")

        payTpInfo = self.session.query(func.sum(SalesRep.ptpaid).label("total")). \
            filter_by(billcashbox=cashbox_code). \
            filter_by(billbilltp=121). \
            filter_by(ptppaytype_id=curpaytype).first()
        if payTpInfo != None:
            if payTpInfo[0] != None:
                bill_lst.append("TOTAL: " + '{0:,.2f}'.format(float(payTpInfo[0])))

                bills_inBill.append("<tr><td colspan='3'><strong>TOTAL: </strong></td><td>" +
                                    '{0:,.2f}'.format(float(payTpInfo[0])) + "</td></tr>")

        totals_cashbox = self.session.query(func.sum(salebills.subtotal).label("subtotal"),
                                            func.sum(salebills.tax).label("tax"),
                                            func.sum(salebills.discount).label("discount"),
                                            func.sum(salebills.total).label("total")). \
            filter_by(cashbox=cashbox_code). \
            filter_by(billtype=121).first()
        final_subtotal = 0.00
        final_tax = 0.00
        final_discount = 0.00
        if totals_cashbox != None:
            if totals_cashbox[0]!=None:
                final_subtotal = float(totals_cashbox[0])
                final_tax = float(totals_cashbox[1])
                final_discount = float(totals_cashbox[2])
                #final_amount = float(totals_cashbox[3])

        close_cashbox = 0
        if "close_cashbox" in inputs:
            close_cashbox = int(inputs["close_cashbox"])

        if close_cashbox == 1:
            # If the command to close the cashbox is 1
            # the system try to find any preorder pending,
            # and if has no preorders then close the cashbox.
            # Otherwise if the close_cashbox is 0,
            # or is not on the inputs then just return just the information.
            preorders = PreOrder.objects(cashbox=int(inputs["cashbox"]), status=11).first()
            self.archivePreOrders({"usercode": cashbox.objects(code=cashbox_info.cashbox).first().user_owner})
            anotherOpenBox = cashbox_open.objects(status=11, cashbox__ne=int(inputs["cashbox"])).first()

            if preorders != None and anotherOpenBox == None:
                self.msg["error"] = "Tiene mesas abiertas, no puede " \
                                    "cerrar la caja hasta que no cierre " \
                                    " todas las ordenes atachadas"

                status_cashbox = self.msg["error"]
                cashbox_open.objects(code=cashbox_info.code).update(set__status=17)
            elif preorders != None and anotherOpenBox != None:
                self.msg["msg_warning"] = "Otro usuario inicio su caja, " \
                                          "desea pasar las mesas abiertas al " \
                                          " otro usuario?"

                status_cashbox = "Caja no pudo ser cerrada por ordenes abiertas"
                cashbox_open.objects(code=cashbox_info.code).update(set__status=17)
                # Collecting the cashbox opens
                self.msg["cashboxes"] = []
                for cashbox_data in cashbox_open.objects(status=11, cashbox__ne=int(inputs["cashbox"])):
                    self.msg["cashboxes"].append(login().getProfile({"usercode":
                                                                         cashbox.objects(
                                                                             code=cashbox_data.cashbox).first().user_owner
                                                                     })["value"]["name"] + "-" + str(cashbox_data.code))


            else:
                status_cashbox = "Caja cerrada"

                cashbox_open.objects(code=cashbox_info.code).update(set__status=14,
                                                                    set__amount_close=final_amount,
                                                                    set__close_date=general().date2julian())

        self.sendCashBoxMail({"products": products_inBillMail, "bills": bills_inBill, "cxc": cxc_inBills["mail_data"],
                              "cashbox": cashbox_info, "final_amount": final_amount, "status": status_cashbox})

        self.msg["code"] = cashbox_code
        self.msg["initial"] = initial
        self.msg["dataprint"] = products_inBill + bill_lst + cxc_inBills["value"]
        self.msg["opened"] = 0
        self.msg["closed"] = 0
        self.msg["status"] = status_cashbox
        self.msg["sub_total"] = '{0:,.2f}'.format(final_subtotal)
        self.msg["final_tax"] = '{0:,.2f}'.format(final_tax)
        self.msg["final_amount"] = '{0:,.2f}'.format(final_amount)
        
        
        
        return {"status": 200,
                "value": self.msg,
                'type': 'application/json'}

    def cxcCloseCashBox(self, inputs):
        data = self.session.query(salebills). \
            filter_by(cashbox=inputs["cashbox"]). \
            filter_by(billtype=122)
        billlst = []
        totalcxc = 0.0
        billlstCxC = []
        for piece in data:
            if piece!=None:
                del piece.__dict__['_sa_instance_state']
                billlst.append(str(piece.__dict__[salebills.code.name]) + " " + str(piece.__dict__[salebills.total.name]))
                billlstCxC.append("<tr><td colspan='3'>" + str(piece.__dict__[salebills.code.name]) + "</td><td>" + '{0:,.2f}'.format(
                    float(piece.__dict__[salebills.total.name])) + "</td></tr>")
                totalcxc += float(piece.__dict__[salebills.total.name])
            else:
                print(inputs["cashbox"])
        billlst.append("Total: " + str(totalcxc))
        billlstCxC.append("<tr><td colspan='3'>Total</td><td>" + '{0:,.2f}'.format(totalcxc) + "</td></tr>")
        
        
        
        return {"status": 200, "value": billlst, "mail_data": billlstCxC, 'type': 'application/json'}

    def closeCashBoxProds(self, inputs):
        cashbox=int(inputs["cashbox"])
        products_lst=[]

        productsData=[]

        for company_info in self.session.query(company._name, company.code):
            categories = self.session.query(category.cat_name, company._name, category.code). \
                filter_by(cat_type=61).filter(category.company==company_info[1]).\
                filter(company.code == category.company).\
                filter(category.status==11).\
                order_by(category.cat_name.asc())

            company_total = 0.00

            products_lst.append("")
            products_lst.append("")

            products_lst.append("-"+company_info[0])
            productsData.append("<tr><td colspan='3' ><h4>"+company_info[0]+"</h4></td></tr>")
            for cat in categories:
                prodslst = self.session.query(Item.code,Item.item_name). \
                    filter_by(category=cat[2]).order_by(Item.item_name.asc())
                subtotal_cat=0.00
                products_lst.append(cat[0])
                products_lst.append(" ")
                productsData.append("<tr><td colspan='3'><strong>"+cat[0]+"</strong></td></tr>")
                for prod_info in prodslst:
                    if prod_info.item_name!=None:
                        product = prod_info.item_name
                        product_name = product.rjust(20) if len(product)<=20 else product[0:20]
                        amount = ProductSale.objects(cashbox=cashbox, product=prod_info[0]).sum("amount")

                        if amount > 0:

                            total_prods = ProductSale.objects(cashbox=cashbox, product=prod_info[0]).sum("subtotal")
                            subtotal_cat += total_prods

                            productsData.append("<tr><td>"+product_name+"</td><td>"+str(amount)+"</td><td>"
                                                +'{0:,.2f}'.format(total_prods)+"</td></tr>")
                            products_lst.append(product_name+" "+str(amount)+"  "+'{0:,.2f}'.format(total_prods))

                products_lst.append("Total: "+'{0:,.2f}'.format(subtotal_cat))
                productsData.append("<tr><td colspan='2'> Total:" + "</td><td span='2'>"
                                    + '{0:,.2f}'.format(subtotal_cat) + "</td></tr>")
                productsData.append("<tr></tr>")
                products_lst.append(" ")
                company_total += subtotal_cat

            products_lst.append("Total "+company_info[0]+" " + '{0:,.2f}'.format(company_total))
        return {"status": 200,
                "value": products_lst,
                "product_data":productsData,
                'type': 'application/json'}

    def _getCashBoxBills(self, inputs):
        self.msg = {}



        initial = 0.00
        final_amount = 0.00
        bill_lst = {}

        # Get all the bills with the cashbox_id.
        bills =cashbox_bills.objects(registred__gte=general().date2julian(str(inputs["from"])),
                                            registred__lte=general().date2julian(str(inputs["end"]))).order_by("paytype+")
        for piece in bills:
            if piece.total!=None:

                final_amount += piece.total


                if piece.paytype in bill_lst:
                    billLst = bill_lst[piece.paytype]
                else:
                    billLst=[]
                    bill_lst[piece.paytype]=billLst

                billLst.append({salebills.total.name:piece.total,
                                 #"order_type":piece.order_type,
                    #"order_tpname":self.session.query(Type).filter(Type.code==piece.order_type).first().tpname,
                    "paytype": piece.paytype,
                    "paytype_name": self.session.query(Type).
                        filter(Type.code == piece.paytype).first().tpname,
                    #"billtype": piece.paytype,
                    #"billtype_name": self.session.query(Type).filter(Type.code == piece.billtype).first().tpname,
                    "date":general().julian2date(str(piece.registred)),
                    "preorder":piece.preorder
                    #"time":str(piece._time.hour)+":"+str(piece._time.minute)+":"+str(piece._time.second)
                                 })



        self.msg["code"] = None
        self.msg["initial"] = initial
        self.msg["bills"] = bill_lst
        self.msg["final_amount"] = final_amount
        
        
        
        return {"status": 200,
                "value": self.msg,
                'type': 'application/json'}


    def delProdOrdered(self, inputs):
        if "code" in inputs:
            ProductPre.objects(code=int(inputs["code"])).delete()

        
        
        
        return {"status": 200,
                "value": "Borrado!",
                    'type': 'application/json'}


    
    def getActiverOrders(self, inputs):
        preorders=PreOrder.objects(status=11)
        active_orders={}

        for preorder in preorders:
            table_info=PreOrderTable.objects(preorder=preorder.code).first()
            if table_info!=None:
                active_orders[table_info.table_code]=preorder.code

        return {"status": 200,
                "value": active_orders,
                'type': 'application/json'}


    def getProductOrdered(self, inputs):
        prdstatus=31
        if "prdstatus" in inputs:
            prdstatus=int(inputs["prdstatus"])

        product_lst=ProductPre.objects(status=prdstatus).order_by('+preorder')
        products=[]

        company_info = Company().Get({})["value"][0]
        orderStr = None

        bills = {"ordercode":{}, "orders":{}}
        waiterStr=""
        comp_lst=[]
        for piece in product_lst:
            if piece.code not in comp_lst:
                storeDict = self.session.query(Item.item_name, category.type_product). \
                    filter(Item.code == piece.product).\
                    filter(Item.category == category.code).first()
                if storeDict!=None:


                    preorder = PreOrder.objects(code=piece.preorder).first()
                    if piece.created_by!=None:
                        waiter = login().getProfile({"usercode":piece.created_by})["value"]["name"]
                    else:
                        waiter=""

                    if preorder.code not in bills["ordercode"]:
                        tble_info = PreOrderTable.objects(preorder=preorder.code).first()
                        if tble_info != None:
                            bills["ordercode"][tble_info.table_code]= preorder.code
                    if orderStr == None:
                        orderStr = waiter
                    else:
                        orderStr += "\n"+waiter

                    products.append({"amount":piece.amount, "terms":piece.term, "notes":piece.notes,"companion":piece.companion,
                                 "portion":piece.portion, "product":piece.product,"status":piece.status,
                                     "discount":piece.discount,"waiter":login().getProfile({"usercode":piece.created_by})["value"]["name"],
                                 "name":storeDict[0],"prod_type":storeDict[1], "subtotal":piece.subtotal,
                                     "tax":piece.tax,"total":piece.total, "code":piece.code})

                    plate_data = str(piece.amount) + " - " + storeDict[0]
                    if len(piece.term)>0:
                        plate_data += ", termino:" + str(piece.term) + ""

                    if len(piece.notes) > 0:
                        plate_data += ", notas:" + str(piece.notes) + ""
                    if len(piece.portion) > 0:
                        plate_data += ", Porcion:" + str(piece.portion) + ""

                    if len(piece.companion)>0:
                        for piece_comp in piece.companion.split("|"):
                            companion_data = ProductPre.objects(code=int(piece_comp)).first()
                            comp_lst.append(int(piece_comp))
                            if companion_data!=None:
                                try:
                                    comp_name = self.session.query(Item.item_name). \
                                        filter(Item.code == companion_data.product).first()[0]
                                    plate_data += ", CON: "+comp_name
                                    if "prod_type" in inputs:
                                        if int(inputs["prod_type"]) == storeDict[1]:
                                            ProductPre.objects(code=int(piece_comp)).update(set__status=32)
                                    elif "prdstatus" in inputs:
                                        pass
                                        # If this happens, the user just want to check a product on that status.
                                    else:
                                        ProductPre.objects(code=int(piece_comp)).update(set__status=32)
                                except:
                                    pass



                    if storeDict[1] in bills["orders"]:
                        prodStr = bills["orders"][storeDict[1]]
                        prodStr += "\n" + plate_data+"\n"
                        bills["orders"][storeDict[1]]=prodStr
                    else:
                        bills["orders"][storeDict[1]]="\n" + plate_data+"\n"

                    code = piece.code
                    if "prod_type" in inputs:
                        if int(inputs["prod_type"]) == storeDict[1]:
                            ProductPre.objects(code=code).update(set__status=32)
                    elif "prdstatus" in inputs:
                        pass
                        # If this happens, the user just want to check a product on that status.
                    else:
                        ProductPre.objects(code=code).update(set__status=32)

        
        
        

        return {"status": 200,
                "value": bills,
                'type': 'application/json'}

    def setBill2Print(self, inputs):
        # Buscar la pre-orden y colocarla para ser impresa, adjuntarle el codigo de la caja
        # por donde saldra.
        bill = None
        preorder = int(inputs["preorder"])
        if "bill" not in inputs:
            bill = self.session.query(salebills.code).filter(salebills.preorder == preorder).first()[0]
        else:
            bill = int(inputs["bill"])

        Bill2Print(preorder=int(inputs["preorder"]), bill=bill, cashbox=General().getCashBox(inputs)).save()


    ##Sending mail
    def sendCashBoxMail(self,inputs):
        cashbox_info=inputs["cashbox"]
        bill_lst=inputs["bills"]
        products_inBill=inputs["products"]
        cxc=inputs["cxc"]
        final_amount=float(inputs["final_amount"])

        user_rootlst = login().Get({User.usrtype.name: 74})["value"]
        bodymsg = "<h2>Resumen de Cuadre de caja: %s</h2><p>" % (
            general().julian2date(str(cashbox_info.open_date)))
        bodymsg +="<table  border='1'><caption>Productos vendidos en el cuadre</caption><tbody>"

        for prod in products_inBill:
            bodymsg +=prod

        bodymsg+="</tbody></table>"
        bodymsg += "<br/> "
        bodymsg += "<table border='1'><caption>Facturas en el cuadre</caption><tbody>"

        for billField in bill_lst:
            bodymsg += billField
        bodymsg += "</tbody></table>"

        bodymsg += "<br/> <strong>Cierre total: " + '{0:,.2f}'.format(final_amount) + "</strong>"

        bodymsg += "<br/><br/><table border='1'><caption>CxC en el cuadre</caption><tbody>"

        for cxcField in cxc:
            bodymsg += cxcField
        bodymsg += "</tbody></table>"



        bodymsg += "<br/> <strong>"+inputs["status"]+"</strong>"
        for user_root in user_rootlst:
            try:
                general().sendMail('Subject: %s\n\n%s' % ("CUADRE DE CAJA, NOT-REPLY", bodymsg + "</p>"),
                                   user_root[User.username.name])
                None
            except Exception as ex:
                raise Exception(str(ex))


    def getBill2Print(self, inputs):
        # Take the bill to be print on that specific cashbox and printed.
        bill = PreOrder.objects(code=inputs["code"]).first()

        products = []
        bills = {}
        billStr=""
        tblsStr = ""
        prodStr = ""
        if bill != None:
            company_info=Company().Get({})["value"][0]
            billStr  = company_info[company._name.name]+"\n\n"
            billStr += "Telefono:"+company_info[company.telephone.name]+"\n"
            billStr += "Dirección:"+company_info[company._address.name]+"\n"
            billStr += "RNC:" + str(company_info[company.rnc.name]) + "\n"
            billStr += "\nNro Factura: "+str(bill.code)

            billStr +="\n\n-------------FACTURA-----------------\n"
            billStr += "\nCANT                        TOTAL\n"

            product_lst = ProductPre.objects(preorder=int(inputs["code"]))
            piece = product_lst.first()

            if piece.preorder in bills:
                products = bills[piece.preorder]["products"]
            else:
                bills[piece.preorder] = {"products": products,
                                         "code": piece.preorder}

                preorder = PreOrder.objects(code=piece.preorder).first()

                tblsStr+="Nro de cuenta:"+str(preorder)+"\n"
                if piece.created_by != None:
                    waiter = login().getProfile({"usercode": piece.created_by})["value"]["name"]

                    tblsStr += "MESERO:" +waiter
                else:
                    waiter = ""
                bills[piece.preorder]["waiter"] = waiter
                if preorder != None:
                    if preorder.order_type != 101:
                        bills[piece.preorder]["table"] = 0
                        bills[piece.preorder]["table_code"] = 0
                    else:
                        bills[piece.preorder]["table_code"] = PreOrderTable.objects(
                            preorder=preorder.code).first().table_code
                        bills[piece.preorder]["table"] = self.session.query(Tables). \
                            filter(Tables.code == bills[piece.preorder]["table_code"]).first().tblname

                tblsStr += "MESERO:" + waiter+"    MESA:" +bills[piece.preorder]["table"]
            for piece in product_lst:

                storeDict = self.session.query(Item.item_name, category.type_product). \
                    filter(Item.code == piece.product).\
                    filter(Item.category == category.code).first()
                if storeDict!=None:

                    prodStr+="\n"+str(piece.amount)+"   "+"  "+str(piece.tax)+"  "+str(piece.total)
                    prodStr+=storeDict[0]

                    products.append({"amount":piece.amount, "terms":piece.term, "notes":piece.notes,
                                 "portion":piece.portion, "product":piece.product,
                                 "name":storeDict[0],"prod_type":storeDict[1], "subtotal":piece.subtotal,
                                     "tax":piece.tax,"total":piece.total})

                    code = piece.code
                    if "prod_type" in inputs:
                        if int(inputs["prod_type"])==storeDict[1]:
                            ProductPre.objects(code=code).update(set__status=32)
                    else:
                        ProductPre.objects(code=code).update(set__status=32)

        billStr += "\n"+prodStr+"\n"+tblsStr+"\n"+"\n"+"\n"+"\n"


        
        
        
        return {"status": 200,
                "value": [bills, billStr],
                'type': 'application/json'}


    def cancelLastBill(self, inputs):

        code_lst =self.session.query(salebills.code).order_by(salebills.code.desc()).first()
        code = code_lst[0]
        self.session.query(salebills).filter(salebills.code == code).\
            update({salebills.status.name : 28})
        
        
        

        return {"status": 200,
                "value": "Factura cancelada",
                'type': 'application/json'}

    # Transfer product
    def trans_product(self, inputs):
        # To transfer a product, we need the id of the product and the ID of the preorder.

        for piece in inputs["product"].split("|"):
            product = ProductPre.objects(code=int(piece)).first()# Extracting the product with the pre-order.
            if product!=None:
                ProductPre.objects(code=int(piece)).update(set__preorder=int(inputs["preorder"]))
                # If the product have companion, then move the companion too
                if len(product.companion)>0 :
                    for companion in product.companion.split("|"):
                        ProductPre.objects(code=int(companion)).update(set__preorder=int(inputs["preorder"]))
        
        
        
        return {"status": 200,
                "value": {"msg": "Productos transferidos"},
                'type': 'application/json'}


        # Apply discount to products
    def resendProd(self, inputs):
        # To transfer a product, we need the id of the product and the ID of the preorder.
        product = ProductPre.objects(
            preorder=int(inputs["preorder"])).update(set__status=31)  # Extracting the product with the pre-order.

        
        
        
        return {"status": 200,
                "value": {"msg": "Orden reenviada"},
                'type': 'application/json'}



    # Assign products to client.

    def splitAccount(self, inputs):
        productLst = str(inputs["product"]).split("|")
        for orderCode in productLst:
            ProductPre.objects(code=int(orderCode)).\
                    update(set__client=str(inputs["client"]).upper())
        
        
        
        return {"status": 200,
                "value": {"msg": "Cuenta separada."},
                'type': 'application/json'}



    def getPreAccount(self, inputs):
        preorder=None
        if "preorder" in inputs:
            preorder = int(inputs["peorder"])
        else:
            return {"status": 200,
                "value": {"msg": "Debe colocar una preorden"},
                'type': 'application/json'}

        client=None
        if "client" in inputs:
            client = inputs["client"]



    def get607(self, inputs):
        from_date = general().date2julian(str(inputs["from_date"]))

        end_date = general().date2julian()
        if "end_date" in inputs:
            end_date = general().date2julian(str(inputs["end_date"]))

        details = self.session.query(SalesRep)
        if from_date == end_date:
            details = details.filter_by(billdate=from_date)
        else:

            details = details. \
                filter(SalesRep.billdate >= from_date). \
                filter(SalesRep.billdate <= end_date)

        msg = []
        details = details.order_by(SalesRep.billncf.asc())
        for piece in details:
            del piece.__dict__['_sa_instance_state']
            # if float(piece.__dict__[SalesRep.billtotal.name])>0:
            #     piece.__dict__["ncf"]=None if piece.__dict__[SalesRep.billncf.name] == None else \
            #         ncfType.objects(code=ncf_codes.objects(
            #             code=piece.__dict__[SalesRep.billncf.name]).first().ncf_type).first().header+\
            #         ncf_codes.objects(code=piece.__dict__[SalesRep.billncf.name]).first().secuence
            #     if piece.__dict__[SalesRep.client_id.name] !=None :
            #         piece.__dict__["rnc"]= ""
            #         client_info=self.session.query(Client).\
            #             filter_by(code=piece.__dict__[SalesRep.client_id.name]).first()
            #         if client_info!=None:
            #             piece.__dict__["rnc"] =client_info.rnc
            #             piece.__dict__["client_name"] =client_info.cl_name
            msg.append(piece.__dict__)

        self.msg = {"details": msg, "total_ncf": len(msg), "total": cashbox_bills.objects(registred__gte=from_date,
                                                                                          registred__lte=end_date).order_by(
            "paytype+").sum('total') / 1.28}
        # from_date = general().date2julian(str(inputs["from_date"]))
        #
        # end_date=general().date2julian()
        # if "end_date" in inputs:
        #     end_date=general().date2julian(str(inputs["end_date"]))
        #
        # self.msg=[]
        # storeDict = self.session.query(salebills._date,Client.cl_name, salebills.ncf,
        #                                salebills.subtotal, salebills.tax, salebills.total,
        #                                salebills.code, salebills.discount,Client.rnc, salebills._time,Client.rnc).\
        #     filter(Client.code == salebills.client).\
        #     filter(salebills._date >= int(from_date)).\
        #     filter(salebills._date <= int(end_date)).\
        #     order_by(salebills.ncf.asc()).\
        #     group_by(Client.cl_name,Client.rnc, salebills._date, salebills.ncf,
        #              salebills.subtotal, salebills.tax,
        #              salebills.total, salebills.code, salebills.discount, salebills._time,Client.rnc)
        #
        # for piece in storeDict:
        #     ncf_sec = ncf_codes.objects(code=piece[2])
        #     ncf = None
        #     if ncf_sec!=None:
        #         ncf=ncf_sec.first().secuence
        #         header = ncfType.objects(code=ncf_sec.first().ncf_type).first().header
        #         ncf =header+ncf
        #     self.msg.append({salebills._date.name:general().julian2date(str(piece[0])),
        #                      Client.cl_name.name:piece[1], salebills.ncf.name:ncf,
        #                      salebills.subtotal.name:str(piece[3]), salebills.tax.name:str(piece[4]),
        #                      salebills.total.name: str(piece[5]), salebills.code.name:str(piece[6]),
        #                      salebills._time.name:str(piece[9]),Client.rnc.name:str(piece[10])})
        #
        #
        #
        # return {"status": 200, "value": self.msg, 'type': 'application/json'}


    def addHappyHour(self, inputs):
        self.msg={"msg":"HappyHour guardado!"}
        start_hour = general().get_sec(inputs["start_hour"])
        end_hour = general().get_sec(inputs["end_hour"])
        if discount.objects(product=int(inputs["product"])).first()==None:
            discount(product=int(inputs["product"]), start_hour=start_hour, end_hour=end_hour, days=inputs["days"],
                 amount_disc=float(inputs["amount_disc"])).save()
        else:
            discount.objects(product=int(inputs["product"])).update(set__start_hour=start_hour, set__end_hour=end_hour, set__days=inputs["days"],
                                                                    set__amount_disc=float(inputs["amount_disc"]))
        
        
        

        return {"status": 200, "value": self.msg, 'type': 'application/json'}


    def closePreorder(self, inputs):
        # This method is for the clients that have a system just to take the pre-orders
        result = login().getUsersBy({"code":inputs["key"]})["value"][0] if "key" in \
                                                                           inputs else {"code":int(inputs["usercode"])}
        if "error" in result:
            return {"status": 200, "value": "Codigo invalido", 'type': 'application/json'}
        preorder =PreOrder.objects(code=int(inputs["preorder"])).first()
        if preorder!=None:
            if preorder.order_type==101:
                tableInfo=PreOrderTable.objects(preorder=preorder.code).first()

            PreOrder.objects(code=preorder.code).update(set__status=17)
            PreOrderTable.objects(preorder=preorder.code).update(set__status=17)
            ProductPre.objects(preorder=preorder.code).update(set__status=34)
            self.msg={"code":inputs["preorder"],"msg":"Orden Borrada"}
        
        
        

        return {"status": 200, "value": self.msg, 'type': 'application/json'}

    def archivePreOrders(self, inputs):
        result = login().getUsersBy({"code": inputs["key"]})["value"][0] if "key" in \
                                                                            inputs else {"code": int(inputs["usercode"])}
        if "error" in result:
            return {"status": 200, "value": "Codigo invalido", 'type': 'application/json'}
        if "preorder" in inputs:

            now = datetime.now()
            curHour = general().get_sec(str(now.hour) + ":" + str(now.minute) + ":" + str(now.second))
            self.msg = {"tables": []}
            preorder = PreOrder.objects(code=int(inputs["preorder"])).first()
            if len(preorder)>0:
                if ProductPre.objects(preorder=preorder.code, status__gt=30).first()!=None:
                    return {"status": 200, "value": {"error":"Hay una orden con productos, "
                                                    "debe ser eliminado todos los "
                                                    "productos antes de continuar"}, 'type': 'application/json'}


                if preorder.order_type==101:
                        tableInfo=PreOrderTable.objects(preorder=preorder.code).first()
                        if tableInfo!=None:
                            self.msg["tables"].append({"preorder":preorder.code,
                                               "table":
                                                   self.session.query(Tables.tblname).
                                              filter_by(code=tableInfo.table_code).first()[0]})
                PreOrder.objects(code=preorder.code).update(set__status=17)
                PreOrderTable.objects(preorder=preorder.code).update(set__status=17)
                reason = ""
                if "reason" in inputs:
                    reason = inputs["reason"]
                archieve_preorder(preorder=preorder.code, reason=reason, created_by=result["code"],
                                  created_hour=curHour, created_date=general().date2julian()).save()
        else:


            now = datetime.now()
            curHour = general().get_sec(str(now.hour) + ":" + str(now.minute) + ":" + str(now.second))
            self.msg={"tables":[]}
            for preorder in PreOrder.objects(status=11):
                if ProductPre.objects(preorder=preorder.code, status__gt=30).first()!=None:
                    return {"status": 200, "value": {"error":"Hay una orden con productos, "
                                                    "debe ser eliminado todos los "
                                                    "productos antes de continuar"}, 'type': 'application/json'}


                if preorder.order_type==101:
                        tableInfo=PreOrderTable.objects(preorder=preorder.code).first()
                        if tableInfo!=None:
                            info_tbl=self.session.query(Tables.tblname).filter_by(code=tableInfo.table_code).first()
                            if info_tbl!=None:
                                self.msg["tables"].append({"preorder":preorder.code,
                                               "table":
                                                   self.session.query(Tables.tblname).
                                              filter_by(code=tableInfo.table_code).first()[0]})

                PreOrder.objects(code=preorder.code).update(set__status=17)
                PreOrderTable.objects(preorder=preorder.code).update(set__status=17)
                reason=""
                if "reason" in inputs:
                    reason=inputs["reason"]
                archieve_preorder(preorder=preorder.code, reason=reason, created_by=result["code"],
                                  created_hour=curHour, created_date=general().date2julian()).save()

        self.msg["msg"] = "No hay ordenes que archivar."
        if len(self.msg["tables"])>0:
            self.msg["msg"]="Preordenes archivadas."
        
        
        

        return {"status": 200, "value": self.msg, 'type': 'application/json'}

    def rollbackCashBox(self, inputs):
        # This method will rollback the cashbox completly
        if "cashbox" in inputs:
            cashbox_data = cashbox_open.objects(code=int(inputs["cashbox"])).update(set__status=11)
            self.msg = "Caja " + cashbox_data.code + ", reversada"
        elif "usercode" in inputs:
            # This will rollback the last cashbox, of that user.
            cashbox_data = cashbox_open.objects(code=cashbox.objects(user_owner=int(inputs["usercode"])).first().code). \
                order_by('-code').first().update(set__status=11)
            self.msg = "Caja " + cashbox_data.code + ", reversada"
        
        
        

        return {"status": 200, "value": self.msg, 'type': 'application/json'}


    def getActiveDelivery(self, inputs):

        self.msg = json.loads(PreOrder.objects(order_type=102, status=11).to_json())

        return {"status": 200, "value": self.msg, 'type': 'application/json'}

    def getCashBoxByUser(self, inputs):
        cashbox_info = cashbox.objects(user_owner=int(inputs["owner"])).first()
        if cashbox_info != None:
            self.msg = json.loads(cashbox_open.objects(cashbox=cashbox_info.code).to_json())
        else:
            self.msg ={"error":"Usuario sin cajas disponibles."}

        
        
        

        return {"status": 200, "value": self.msg, 'type': 'application/json'}


    def addClientPreorder(self, inputs):
        clientFnc=Clients()
        clientID=None
        if "client_code" not in inputs:
            client_data = clientFnc.create(inputs)["value"]
            if "error" not in client_data:
                clientID=client_data[Client.code.name]
        else:
            handle_inputs=inputs
            clientID=int(inputs["client_code"])
            handle_inputs[Client.code.name]=clientID
            client_data = clientFnc.HandleClient(handle_inputs)["value"]

        client_info = clientFnc.Get({Client.code.name:clientID})["value"]
        openPreorder_inp = {"client": clientID, "billtype": 102, "key": inputs["key"],
                            "cashbox": inputs["cashbox"]}

        if len(client_info)>0:
            openPreorder_inp["client_name"]=client_info[0][Client.cl_name.name]
            openPreorder_inp["rnc"]=client_info[0][Client.rnc.name]
            openPreorder_inp["ncf"]=str(client_info[0][Client.ncf_type.name])
            openPreorder_inp["telephone"]=client_info[0][Client.telephone.name]
            openPreorder_inp["address"]=client_info[0][Client._address.name]
            openPreorder_inp["credit"]=client_info[0][Client.credit.name]
            openPreorder_inp["max_credit"]=client_info[0][Client.max_credit.name]
            openPreorder_inp["cur_credit"]=client_info[0][Client.current_credit.name]
        self.msg=self.openPreorder(openPreorder_inp)["value"]
        self.msg["client_code"]=clientID

        return {"status": 200, "value": self.msg, 'type': 'application/json'}

    def getDelProdBills(self, inputs):
        _from_date = inputs["from"]
        _to_date = inputs["end"]

        from_date = int(general().date2julian(_from_date.split(" ")[0]))
        to_date = int(general().date2julian(_to_date.split(" ")[0]))

        prod_lst=json.loads(PreOrderProdDel.objects(created_date__gte=from_date, created_date__lte=to_date).to_json())
        for piece in prod_lst:
            piece["text_date"]=general().julian2date(str(piece["created_date"]))
            piece["waiter"] =login().getProfile({"usercode":piece["created_by"]})["value"]["name"]
            status_text=self.session.query(Status.description).filter(Status.code==piece["status"]).first()
            if status_text!=None:
                piece["status_text"] = status_text[0]
            productpre_info=ProductPre.objects(code=piece["product"]).first()
            if productpre_info!=None:
                status_text = self.session.query(Item.item_name).filter(Item.code == ProductPre.objects(code=piece["product"]).first().product).first()
                if status_text != None:
                    piece["product_name"] = status_text[0]
        
        
        
        return {"status": 200, "value": prod_lst, 'type': 'application/json'}

    def getProdBills(self, inputs):
        _from_date = inputs["from"]
        _to_date = inputs["end"]

        from_date = int(general().date2julian(_from_date.split(" ")[0]))
        to_date = int(general().date2julian(_to_date.split(" ")[0]))

        prod_lst=json.loads(ProductPre.objects(created_date__gte=from_date,
                                               created_date__lte=to_date).order_by("+code").to_json())

        for piece in prod_lst:
            piece["text_date"]=general().julian2date(str(piece["created_date"]))
            status_text=self.session.query(Status.description).filter(Status.code==piece["status"]).first()
            if status_text!=None:
                piece["status_text"] = status_text[0]

        
        
        
        return {"status": 200, "value": prod_lst, 'type': 'application/json'}


    def getCXCBills(self, inputs):
        _from_date = inputs["from"]
        _to_date = inputs["end"]


        from_date = int(general().date2julian(_from_date.split(" ")[0]))
        to_date = int(general().date2julian(_to_date.split(" ")[0]))

        bills = self.session.query(salebills).\
            filter(salebills.billtype == 122).\
            filter(salebills._date >= from_date).\
            filter(salebills._date <= to_date)

        #if "client" in inputs:
        #    bills =bills.filter_by(SalesRep.bill)

        data = bills.order_by(salebills.preorder.asc())
        self.msg = []
        for piece in data:
            if piece!=None:
                del piece.__dict__['_sa_instance_state']
                piece.__dict__[salebills.tax.name]=float(piece.__dict__[salebills.tax.name])
                piece.__dict__[salebills.discount.name]=float(piece.__dict__[salebills.discount.name])
                piece.__dict__[salebills.subtotal.name]=float(piece.__dict__[salebills.subtotal.name])
                piece.__dict__[salebills.total.name]=float(piece.__dict__[salebills.total.name])
                piece.__dict__[salebills._time.name] = general().getTimeFormat(piece.__dict__[salebills._time.name])
                self.msg.append(piece.__dict__)

        
        
        
        return {"status": 200, "value": self.msg, 'type': 'application/json'}


    def getBillsBy(self, inputs):
        bills = self.session.query(SalesRep)
        if "cashbox" in inputs:
            bills = bills.filter(SalesRep.billcashbox == int(inputs["cashbox"]))

        if "billtp" in inputs:
            bills = bills.filter(SalesRep.billbilltp == int(inputs["billtp"]))

        if SalesRep.client_id.name in inputs:
            bills = bills.filter(SalesRep.client_id == int(inputs[SalesRep.client_id.name]))

        if SalesRep.client_name.name in inputs:
            bills = bills.filter(SalesRep.client_name.
                                 ilike("%"+str(inputs[SalesRep.client_name.name])+"%"))

        data = bills.order_by(SalesRep.billcode.asc())
        self.msg = []
        for piece in data:
            if piece!=None:
                del piece.__dict__['_sa_instance_state']
                piece.__dict__[SalesRep.ptptotal.name]=float(piece.__dict__[SalesRep.ptptotal.name])
                piece.__dict__[SalesRep.ptpextra.name]=float(piece.__dict__[SalesRep.ptpextra.name])
                piece.__dict__[SalesRep.ptptax.name]=float(piece.__dict__[SalesRep.ptptax.name])
                piece.__dict__[SalesRep.ptpdesc.name]=float(piece.__dict__[SalesRep.ptpdesc.name])
                piece.__dict__[SalesRep.ptpsubtotal.name]=float(piece.__dict__[SalesRep.ptpsubtotal.name])
                piece.__dict__[SalesRep.ptpaid.name]=float(piece.__dict__[SalesRep.ptpaid.name])
                self.msg.append(piece.__dict__)

        
        
        
        return {"status": 200, "value": self.msg, 'type': 'application/json'}


    def getBillsDebt(self, inputs):
        bills = self.session.query(SalesDebt).filter(SalesDebt.billbilltp == 122)

        if SalesDebt.client_id.name in inputs:
            bills = bills.filter(SalesDebt.client_id ==int(inputs[SalesDebt.client_id.name]))

        if Client.cl_name.name in inputs:
            bills = bills.filter(Client.cl_name.
                                 ilike("%"+str(inputs[Client.cl_name.name])+"%")).\
                filter(SalesDebt.client_id==Client.code)

        data = bills.order_by(SalesDebt.billcode.asc())
        self.msg = []
        for piece in data:
            del piece.__dict__['_sa_instance_state']
            piece.__dict__[SalesDebt.billtotal.name]=float(piece.__dict__[SalesDebt.billtotal.name])
            piece.__dict__[SalesDebt.billdisc.name]=float(piece.__dict__[SalesDebt.billdisc.name])
            piece.__dict__[SalesDebt.billtax.name]=float(piece.__dict__[SalesDebt.billtax.name])
            piece.__dict__[SalesDebt.billsubtotal.name]=float(piece.__dict__[SalesDebt.billsubtotal.name])
            if piece.__dict__[SalesDebt.ptpaid.name]!=None:
                piece.__dict__[SalesDebt.ptpaid.name]=float(piece.__dict__[SalesDebt.ptpaid.name])
            else:
                piece.__dict__[SalesDebt.ptpaid.name] =0.00
            piece.__dict__[SalesDebt.billtime.name]=piece.__dict__[SalesDebt.billtime.name]
            self.msg.append(piece.__dict__)

        
        
        
        return {"status": 200, "value": self.msg, 'type': 'application/json'}

    def addPaymentCXC(self, inputs):
        paylst = json.dumps(str(inputs["bills"])) if isinstance(inputs["bills"], str) \
            else inputs["bills"]

        for piece in paylst:
            data={}
            data["billcode"] = int(paylst[piece]["billcode"])
            data["preorder"] = piece
            data["billtype"] = int(paylst[piece]["billtype"])
            data["_date"] = general().date2julian()
            data["total"] = float(paylst[piece]["total"])
            data["subtotal"] = float(paylst[piece]["subtotal"])
            data["tax"] = float(paylst[piece]["tax"])
            data["billtp_extra"] = float(paylst[piece]["billtp_extra"])
            data["discount"] = float(paylst[piece]["discount"])
            data["client"] = int(paylst[piece]["client"])
            data["paytypelst"] =paylst[piece]["paytypelst"]
            data["cashbox"] = int(inputs["cashbox"])
            self.addPayment2Bill(data)

        
        
        
        self.msg={"msg":"Envio exitoso"}
        return {"status": 200, "value": self.msg, 'type': 'application/json'}


    def getProductsBilled(self, inputs):
        self.msg=[]
        data=ProductSale.objects(cashbox=int(inputs["cashbox"])).distinct(field="product")
        for piece in data:
            self.msg.append({"product":piece, "product_name":ProductSale.objects(product=piece).first().product_name})

        return {"status": 200, "value": self.msg
            , 'type': 'application/json'}



    def getOrdersByClient(self, inputs):
        orders = PreOrder.objects(client=inputs["client"], status=11)
        return {"status": 200, "value": orders.to_json()
            , 'type': 'application/json'}

    def getCashBoxInfo(self, inputs):

        '''
        Find all the cashbox.
        :param inputs:
        :return:
        List of all cashboxes
        '''

        data =self.session.query(CashBox)

        msg=[]
        for piece in data:
            del piece.__dict__['_sa_instance_state']

            msg.append(piece.__Publish__())
        return {"status": 200, "value": msg, 'type': 'application/json'}




if __name__ == '__main__':
    None

__author__ = 'hidura'
