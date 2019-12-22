import json
import os

from sqlalchemy.sql.expression import and_
from werkzeug.utils import secure_filename

from tools.DataBase.CodeGenerator import CodeGen
from tools.DataBase.Connect import conection
from tools.DataBase.Definition import db
from tools.DataBase.Definition.Item import Item
from tools.DataBase.Definition.Status import Status
from tools.DataBase.Definition.Supplier import Supplier
from tools.DataBase.Definition.Type import Type
from tools.DataBase.Definition.WareHouse import WareHouse
from tools.DataBase.Definition.category import category
from tools.DataBase.ODM.DataModelODM import recipe_items, products_move, \
    product_additional, product_term, terms, product_optionals, product_compounds, discount, ProductTax, item_buy, \
    ProductPre
from tools.DataBase.Process import DBProcess
from tools.main.general import general
from tools.main.process.Categories import Categories
from tools.main.process.General import General
from tools.main.process.Types import Types

from tools.main.process.supplier import supplier
from decimal import Decimal


class Items:
        def __init__(self):

            self.status = 200
            self.msg = None
            self.type = "text/plain"

            self.db=db
            self.session = db.session
            self.general_tools=general()

        def Get(self, inputs):
            # This method gets the data, from the db.
            storeDict = self.session.query(Item, Status.description,
                                           Type.tpname, category.cat_name).\
                filter(Status.code == Item.status).\
                filter(Type.code == Item.item_type).\
                filter(category.code== Item.category)



            if Item.code.name in inputs:
                storeDict =storeDict. \
                    filter(Item.code == int(inputs[Item.code.name]))

            elif Item.item_name.name in inputs:
                storeDict = storeDict.filter(Item.item_name.
                                             ilike("%"+str(inputs[Item.item_name.name]).lower()+"%"))


            elif Item.item_type.name in inputs and Item.category.name not in inputs:
                storeDict = storeDict. \
                    filter(Item.item_type == int(inputs[Item.item_type.name]))

            elif Item.category.name in inputs and Item.item_type.name not in inputs:
                storeDict = storeDict. \
                    filter(Item.category == int(inputs[Item.category.name]))

            elif Item.category.name in inputs and Item.item_type.name in inputs:
                storeDict = storeDict.\
                    filter(Status.code == Item.status)

                if int(inputs[Item.category.name]) > 0:
                    storeDict = storeDict.\
                        filter(and_(category.code == Item.category,Item.category == int(inputs[Item.category.name])))
                else:
                    storeDict = storeDict.\
                        filter(and_(category.code == Item.category,Item.category > 0))

                storeDict=storeDict.\
                    filter(Type.code == Item.item_type).\
                    filter(Type.code == int(inputs[Item.item_type.name]))
            if Item.supplier.name in inputs:
                storeDict= storeDict.\
                        filter(Item.supplier==int(inputs[Item.supplier.name]))
            # The next area is in charge to extract the information,
            # from the store Dict and add it to the dataCol to be returned
            storeDict=storeDict.order_by(category.cat_name.asc())
            storeDict=storeDict.group_by(Item.item_name,category.cat_name,Item.id,  Status.description, Type.tpname)
            dataCol = []
            for dataLst in storeDict:

                tpname=dataLst._asdict()["tpname"]
                dicStore = {"status_name": dataLst._asdict()[Status.description.name],
                            "tpname":tpname,"unit_name":self.session.query(Type.tpname).
                        filter_by(code=dataLst._asdict()[Item.__name__].__dict__["unit"]).first()[0]}
                if category.cat_name.name in dataLst._asdict():
                    dicStore[category.cat_name.name]=dataLst._asdict()[category.cat_name.name]

                for key in DBProcess(Item.Item_tbl).getColumnDefinition:
                    dataDict = dataLst._asdict()[Item.__name__].__dict__  # Getting the dictionary of the list.
                    colname = key["name"]  # Getting the column name.
                    if colname in dataDict:  # Just if the column name is on the dictionary, add it to the dictStore.

                        dicStore[colname] = DBProcess(Item.Item_tbl).parse2publish(dataDict[colname])
                        if colname == Item.item_name.name:
                            new_name=dicStore[colname]
                            dicStore[colname]=new_name
                dicStore["taxes"]=json.loads(ProductTax.objects(product=dicStore[Item.code.name]).to_json())

                dataCol.append(dicStore)
                # Appending everything to be returned


            if "wrap_to" in inputs:

                dataCol = General().WrapInfo(inputs, dataCol,
                                             [{Item.code.name:"id"},
                                              {Item.item_name.name:"text"},
                                              {"tpname":"tpname"}])

            return {"status": 200, "value": dataCol, 'type': 'application/json'}

        def create(self, inputs):
            # This method will create an expense.
            self.code = CodeGen().GenCode({"table": Item.__tablename__, "column": Item.code.name})
            # Generating the code.

            price = float(inputs["price"])
            price1=price
            price2=price
            price3=price
            price4=price

            # if Item.price1.name in inputs:
            #     price1=float(inputs[Item.price1.name])
            # if Item.price2.name in inputs:
            #     price2=float(inputs[Item.price2.name])
            # if Item.price3.name in inputs:
            #     price3=float(inputs[Item.price3.name])
            # if Item.price4.name in inputs:
            #     price4=float(inputs[Item.price4.name])

            self.session.add(Item(code=self.code, status=int(inputs["status"]), amount=float(inputs["amount"]),
                                  category=int(inputs["category"]), unit=int(inputs["unit"]),barcode=inputs["barcode"],
                                 # price1=price1,price2=price2,
                                 # price3=price3,price4=price4,
                                  price=price, item_type=int(inputs["item_type"]),subtotal=float(inputs["subtotal"]),
                                  description=inputs["description"], item_name=inputs["item_name"],
                                  tax=float(inputs["tax"]), supplier=int(inputs["supplier"])))

            if float(inputs["initial_cost"])>0:
                real_cost = float(inputs["initial_cost"])/float(inputs["amount"])
                item_buy(amount=float(inputs["amount"]),
                         item=self.code, bill=0,# Bill has to be zero becuase is the first time.
                         price=real_cost).save()

            warehouse_info = self.session.query(WareHouse).filter_by(mainwarehouse=True).first()
            if warehouse_info !=None:
                warehose=warehouse_info

                connection = self.db.engine.raw_connection()
                cursor = connection.cursor()

                cursor.callproc('products_movement',[self.code,Decimal(inputs["amount"]),
                                warehose.code,0])
                cursor.close()
            # Saving
            self.session.commit()

            ProductTax.objects(product=self.code).delete()
            if "taxes" in inputs:
                if "," in inputs["taxes"][len(inputs["taxes"]) - 1]:
                    # This is because the fucking form send the list as a string separated by comma as last value
                    del inputs["taxes"][-1]
                for tax in inputs["taxes"]:
                    ProductTax(product=self.code, tax=int(tax)).save()

            if "terms" in inputs:
                self.add2term({"terms":inputs["terms"],"product":self.code})

            if "additional" in inputs:
                self.newAdditionals({"additional":inputs["additional"],"product":self.code})

            if "compounds" in inputs:
                self.newCompounds({"compounds":inputs["compounds"],"product":self.code})

            if "optionals" in inputs:
                self.newOptionals({"optionals":inputs["optionals"],"product":self.code})

            if "recipe" in inputs:
                self.newRecipe({"recipe": inputs["recipe"], "product": self.code})

            return {"status": 200, "value": {Item.code.name: self.code}, 'type': 'application/json'}

        def create_massive(self, inputs):
            # This method will create a product comming from a CSV file.


            # Generating the code.
            price = float(inputs["price"])
            price1=price
            price2=price
            price3=price
            price4=price

            if Item.price1.name in inputs:
                price1=float(inputs[Item.price1.name])
            if Item.price2.name in inputs:
                price2=float(inputs[Item.price2.name])
            if Item.price3.name in inputs:
                price3=float(inputs[Item.price3.name])
            if Item.price4.name in inputs:
                price4=float(inputs[Item.price4.name])

            category_name = str(inputs["category"]).upper()
            supplier_name = str(inputs["supplier"]).upper()

            category_info = self.session.query(category).filter(category.cat_name == category_name).first()
            category_code = 0
            if category_info == None:
                category_code = Categories().create({category.cat_name.name: category_name,
                                                     category.cat_type.name: 61})["value"][category.code.name]
            else:
                category_code = category_info.code

            supplier_info = self.session.query(Supplier).filter(
                Supplier.sup_name == supplier_name).first()
            supplier_code = 0
            if supplier_info == None:
                supplier_code = supplier().create({Supplier.sup_name.name: supplier_name})["value"][Supplier.code.name]
            else:
                supplier_code = supplier_info.code
            if self.session.query(Item.code).filter_by(barcode=str(inputs["barcode"]).strip("'")).first()==None:
                self.code = CodeGen().GenCode({"table": Item.__tablename__, "column": Item.code.name})
                self.session.add(Item(code=self.code, status=11, amount=0.00,
                                  category=category_code, unit=517,
                                  #price1=price1,price2=price2,
                                  #price3=price3,price4=price4,
                                  #    initial_cost=float(inputs["initial_cost"]),
                                  barcode=str(inputs["barcode"]).strip("'"),
                                  price=price, item_type=41,subtotal=float(inputs["subtotal"]),
                                  description=inputs["description"], item_name=inputs["item_name"],
                                  tax=float(inputs["tax"]), supplier=supplier_code))

                self.session.commit()
            else:
                self.code=self.session.query(Item.code).filter_by(barcode=str(inputs["barcode"]).strip("'")).first().code
                storeDict={Item.code.name:self.code, Item.status.name:11,
                           Item.amount.name:0.00,Item.category.name:category_code,
                           Item.unit.name:517,
                           #Item.price1.name:price1,
                           #Item.price2.name:price2,
                           #Item.initial_cost.name:float(inputs["initial_cost"]),
                           #Item.price3.name:price3,Item.price4.name:price4,
                           Item.barcode.name:str(inputs["barcode"]).strip("'"),
                           Item.price.name:price, Item.item_type.name:41,Item.subtotal.name:0.00,
                           Item.description.name:inputs["description"], Item.item_name.name:inputs["item_name"],
                           Item.tax.name:0.00, Item.supplier.name:supplier_code}
                self.Handle(storeDict)
            # Saving

            return {"status": 200, "value": {Item.code.name: self.code}, 'type': 'application/json'}

        def Handle(self, inputs):
            # This method will modify an expanse.
            item = int(inputs[Item.code.name])

            from app import app

            logo_path = ""
            logo_file = "".encode()
            self.msg={}
            if "avatar" in inputs:
                file = inputs['avatar']
                if file.filename == '':
                    mgs = "No file has been selected"
                if file and general().allowed_file(file.filename):
                    filename = secure_filename(file.filename)
                    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                    file_dst = app.config['UPLOAD_FOLDER'] + "/" + filename
                    del inputs['avatar']
                    inputs['avatar']=file_dst
                else:

                    del inputs["avatar"]
            storeDict = {}

            public_prod = False if "public" not in inputs else inputs["public"]

            for column in DBProcess(Item.Item_tbl).getColumnDefinition:
                if column["name"] in inputs:
                    storeDict[column["expr"]] = DBProcess(Item.Item_tbl).parse(column,inputs[column["name"]])

            self.session.query(Item).filter_by(code=item).update(storeDict)
            self.session.commit()

            self.msg[Item.code.name] = item
            if "taxes_info" in inputs:

                ProductTax.objects(product=item).delete()

                for tax in json.loads(inputs["taxes_info"]):
                    ProductTax(product=item, tax=int(tax)).save()
            if "terms" in inputs:
                self.add2term({"terms": inputs["terms"], "product": item})

            if "additional" in inputs:
                self.newAdditionals({"additional": inputs["additional"], "product": item})

            if "compounds" in inputs:
                self.newCompounds({"compounds": inputs["compounds"], "product": item})

            if "optional" in inputs:
                self.newOptionals({"optionals": inputs["optional"], "product": item})

            if "recipe" in inputs:
                self.newRecipe({"recipe": inputs["recipe"], "product": item})

            return {"status": 200, "value": self.msg, 'type': 'application/json'}

        def get2Report(self, inputs):
            # This method gets the data, from the db.
            storeDict = self.session.query(Item.code, Item.item_name, Item.amount, Item.price, Item.barcode,
                                           # Item.price2, Item.price3,Item.price4,Item.price1,Item.initial_cost,
                                           Status.description,
                                           Type.tpname, category.cat_name, Supplier.sup_name). \
                filter(Status.code == Item.status). \
                filter(Type.code == Item.item_type). \
                filter(category.code == Item.category). \
                filter(Supplier.code == Item.supplier)

            if Item.code.name in inputs:
                storeDict = storeDict. \
                    filter(Item.code == int(inputs[Item.code.name]))

            elif Item.item_name.name in inputs:
                storeDict = storeDict.filter(Item.item_name.
                                             ilike("%" + str(inputs[Item.item_name.name]).lower() + "%"))


            elif Item.item_type.name in inputs and Item.category.name not in inputs:
                storeDict = storeDict. \
                    filter(Item.item_type == int(inputs[Item.item_type.name]))

            elif Item.category.name in inputs and Item.item_type.name not in inputs:
                storeDict = storeDict. \
                    filter(Item.category == int(inputs[Item.category.name]))

            elif Item.category.name in inputs and Item.item_type.name in inputs:
                storeDict = storeDict. \
                    filter(Status.code == Item.status)

                if int(inputs[Item.category.name]) > 0:
                    storeDict = storeDict. \
                        filter(and_(category.code == Item.category, Item.category == int(inputs[Item.category.name])))
                else:
                    storeDict = storeDict. \
                        filter(and_(category.code == Item.category, Item.category > 0))

                storeDict = storeDict. \
                    filter(Type.code == Item.item_type). \
                    filter(Type.code == int(inputs[Item.item_type.name]))

            # The next area is in charge to extract the information,
            # from the store Dict and add it to the dataCol to be returned
            storeDict = storeDict.order_by(category.cat_name.asc())
            storeDict = storeDict.group_by(Item.item_name, Item.amount, Item.price,
                                           # Item.price1,
                                           Item.barcode,
                                           # Item.price2, Item.price3,Item.price4,Item.initial_cost,
                                           category.cat_name, Item.code, Status.description, Type.tpname,
                                           Supplier.sup_name)
            dataCol = []
            for dataLst in storeDict:

                tpname = dataLst._asdict()["tpname"]
                dicStore = {"status_name": dataLst._asdict()[Status.description.name],
                            "tpname": tpname, "sup_name": dataLst._asdict()[Supplier.sup_name.name]}
                if category.cat_name.name in dataLst._asdict():
                    dicStore[category.cat_name.name] = dataLst._asdict()[category.cat_name.name]
                for key in DBProcess(Item.Item_tbl).getColumnDefinition:
                    colname = key["name"]  # Getting the column name.
                    if colname in dataLst._asdict():
                        dicStore[colname] = DBProcess(Item.Item_tbl).parse2publish(dataLst._asdict()[colname])

                dataCol.append(dicStore)
                # Appending everything to be returned
            if "wrap_to" in inputs:
                dataCol = General().WrapInfo(inputs, dataCol,
                                             [{Item.code.name: "id"},
                                              {Item.item_name.name: "text"},
                                              {"tpname": "tpname"}])

            return {"status": 200, "value": dataCol, 'type': 'application/json'}

        def newRecipe(self, inputs):
            _recipe_ = json.loads(inputs["recipe"]) if isinstance(inputs["recipe"], str) \
                else inputs["recipe"]
            if len(_recipe_) > 0:
                recipe_items.objects(recipe=int(inputs["product"])).delete()

                recipeLst = []
                for recipe in _recipe_:
                    if recipe != None:
                        code = CodeGen().GenCode({"table": recipe_items.__name__, "column": "code"})
                        recipeLst.append(recipe_items(code=code, item=int(recipe["product"]),
                                                      recipe=int(inputs["product"]), unit=int(recipe["unit"]),
                                                      amount=float(recipe["amount"]), unit_name=recipe["unit_name"],
                                                      item_name=recipe["item_name"]))

                if len(recipeLst) > 0:
                    recipe_items.objects.insert(recipeLst)

            return {"status": 200, "value": {"code": inputs["product"]}, 'type': 'application/json'}

        def delItemRecipe(self, inputs):
            recipe_items.objects(code=int(inputs["code"])).update(set__status=13)

            return {"status": 200, "value": {"code": int(inputs["code"])}, 'type': 'application/json'}

        def getItemRecipe(self, inputs):
            if "recipe" in inputs:
                # Searching a single recipe
                items = recipe_items.objects(item=int(inputs["recipe"]), status__lte=12)
            else:
                # Searching for a item inside a recipe
                items = recipe_items.objects(recipe=int(inputs["item"]), status__lte=12)

            itemLst = []
            for piece in items:
                unit_name = "Unidad"
                unit_ = Types().Get({"code": piece.unit})["value"]
                if len(unit_) > 0:
                    unit_name = unit_[0]["tpname"]
                prodname = None
                prodinfo = self.Get({Item.code.name: piece.item})["value"]
                if len(prodinfo) > 0:
                    prodname = prodinfo[0][Item.item_name.name]
                itemLst.append({"code": piece.code, "product": piece.item, "amount": piece.amount,
                                "item_name": prodname,
                                "unit_name": unit_name, "unit": piece.unit})

            return {"status": 200, "value": itemLst, 'type': 'application/json'}

        def RecipeProds(self, inputs):
            storeDict = self.session.query(Item.item_name, Item.code, Status.name, category.cat_name). \
                filter(Status.code == Item.status). \
                filter(Type.code == Item.item_type). \
                filter(category.code == Item.category). \
                filter(category.code == int(inputs[Item.category.name]))

            self.msg = []
            for piece in storeDict:
                dataDict = {Item.item_name.name: piece[0], Item.code.name: piece[1],
                            "status_name": piece[2], "category": piece[3],
                            "recipe": self.getItemRecipe({"item": int(piece[1])})["value"]}
                self.msg.append(dataDict)

            return {"status": 200, "value": self.msg, 'type': 'application/json'}

        def getSaleProdsByCat(self, inputs):
            storeDict = self.session.query(Item.item_name, Item.code, Item.price, Item.status, Item.category,
                                           Status.description, Type.tpname, Item.item_type, Item.avatar,
                                           category.cat_name, category.cat_type, category.type_product). \
                filter(Status.code == Item.status).filter(Type.code == Item.item_type). \
                filter(category.code == Item.category). \
                filter(Item.category == int(inputs[Item.category.name])) \
                .order_by(Item.item_name.asc())
            self.msg = []
            for dataLst in storeDict:

                cat_typename = Types().Get({Type.code.name: dataLst._asdict()[category.type_product.name]})["value"][0][
                    Type.tpname.name]
                category_name = dataLst._asdict()[category.cat_name.name]
                dicStore = {"status_name": dataLst._asdict()[Status.description.name],
                            "tpname": dataLst._asdict()["tpname"],
                            category.cat_name.name: category_name,
                            category.type_product.name:
                                Types().Get({Type.code.name: dataLst._asdict()[category.type_product.name]})
                                ["value"][0][Type.tpname.name],
                            "cat_typename": cat_typename}

                for key in DBProcess(Item.Item_tbl).getColumnDefinition:
                    colname = key["name"]  # Getting the column name.
                    if colname in dataLst._asdict():  # Just if the column name is on the dictionary, add it to the dictStore.
                        dicStore[colname] = DBProcess(Item.Item_tbl).parse2publish(dataLst._asdict()[colname])

                ###Getting the companion and the terms if the product have it.

                # Additional
                addLst = []
                dicStore["companions"] = addLst
                additionals = product_additional.objects(product=dicStore[Item.code.name])
                for piece in additionals:
                    additional_info = self.session.query(Item.code, Item.item_name, Item.price, Item.subtotal,
                                                         Item.tax). \
                        filter_by(code=piece.additional).first()
                    addLst.append({"name": additional_info[1], "code": additional_info[0],
                                   "price": str(additional_info[2]),
                                   "subtotal": str(additional_info[3]),
                                   "tax": str(additional_info[4])})

                # Terms
                termsLst = []
                dicStore["terms"] = termsLst
                terms_data = product_term.objects(product=dicStore[Item.code.name])
                for piece in terms_data:
                    termsLst.append({"term": piece.term, "name": terms.objects(term=piece.term)._name})

                # Optionals
                optLst = []
                dicStore["optionals"] = optLst
                optionals = product_optionals.objects(product=dicStore[Item.code.name])
                for piece in optionals:
                    optional_info = self.session.query(Item.code, Item.item_name, Item.price, Item.subtotal,
                                                       Item.tax). \
                        filter_by(code=piece.optional).first()
                    optLst.append({"name": optional_info[1], "code": optional_info[0],
                                   "price": str(optional_info[2]),
                                   "subtotal": str(optional_info[3]),
                                   "tax": str(optional_info[4])})

                # Compounds
                cmpLst = []
                dicStore["compounds"] = cmpLst
                compoundlst = product_compounds.objects(product=dicStore[Item.code.name])
                for piece in compoundlst:
                    compound_info = self.session.query(Item.code, Item.item_name, Item.price, Item.subtotal,
                                                       Item.tax). \
                        filter_by(code=piece.compound).first()
                    cmpLst.append({"name": compound_info[1], "code": compound_info[0],
                                   "price": str(compound_info[2]),
                                   "subtotal": str(compound_info[3]),
                                   "tax": str(compound_info[4])})
                self.msg.append(dicStore)

            return {"status": 200, "value": self.msg, 'type': 'application/json'}

        def getSaleProdsByCode(self, inputs):

            storeDict = self.session.query(Item.item_name, Item.item_type, Item.avatar,
                                           Item.description, Item.code, Item.price,
                                           Item.status, Item.category,
                                           Item.subtotal, Item.tax, Status.description). \
                filter(Item.code == int(inputs[Item.code.name]))
            self.msg = []
            dataLst = storeDict.first()

            dicStore = {"status_name": dataLst._asdict()[Status.description.name]}

            for key in DBProcess(Item.Item_tbl).getColumnDefinition:
                colname = key["name"]  # Getting the column name.
                if colname in dataLst._asdict():  # Just if the column name is on the dictionary, add it to the dictStore.
                    dicStore[colname] = DBProcess(Item.Item_tbl).parse2publish(dataLst._asdict()[colname])

            ###Getting the companion and the terms if the product have it.

            # Additional
            addLst = []
            dicStore["companions"] = addLst
            additionals = product_additional.objects(product=dicStore[Item.code.name])
            for piece in additionals:
                additional_info = self.session.query(Item.code, Item.item_name, Item.price, Item.subtotal,
                                                     Item.tax). \
                    filter_by(code=piece.additional).first()
                addLst.append({"name": additional_info[1], "code": additional_info[0], "price": str(additional_info[2]),
                               "subtotal": str(additional_info[3]), "tax": str(additional_info[4])})

            # Terms
            termsLst = []
            dicStore["terms"] = termsLst
            terms_data = product_term.objects(product=dicStore[Item.code.name])
            for piece in terms_data:
                termsLst.append({"term": piece.term, "name": terms.objects(code=piece.term).first()._name})

            # Optionals
            optLst = []
            dicStore["optionals"] = optLst
            optionals = product_optionals.objects(product=dicStore[Item.code.name])
            for piece in optionals:
                optional_info = self.session.query(Item.code, Item.item_name, Item.price, Item.subtotal,
                                                   Item.tax, Item.avatar). \
                    filter_by(code=piece.optional).first()

                optLst.append({"name": optional_info[1], "code": optional_info[0], "price": str(optional_info[2]),
                               "subtotal": str(optional_info[3]), "tax": str(optional_info[4]),
                               "avatar": optional_info[5]})

            # Compounds
            cmpLst = []
            dicStore["compounds"] = cmpLst
            compoundlst = product_compounds.objects(product=dicStore[Item.code.name])
            for piece in compoundlst:
                compound_info = self.session.query(Item.code, Item.item_name, Item.price, Item.subtotal,
                                                   Item.tax, Item.avatar). \
                    filter_by(code=piece.compound).first()
                cmpLst.append({"name": compound_info[1], "code": compound_info[0], "price": str(compound_info[2]),
                               "subtotal": str(compound_info[3]), "tax": str(compound_info[4]),
                               "avatar": compound_info[5]})
            self.msg = dicStore

            return {"status": 200, "value": self.msg, 'type': 'application/json'}

        def getSaleProdsByOrd(self, inputs):

            category_lst = self.session.query(category.code, category.cat_name). \
                filter(category.type_product >= 131). \
                order_by(category.cat_name.name).all()
            cat_code = 0
            cat_name = ""
            if len(category_lst) - 1 >= int(inputs["pos"]):
                cat_code = category_lst[int(inputs["pos"])][0]
                cat_name = category_lst[int(inputs["pos"])][1]
            else:
                cat_code = category_lst[len(category_lst) - 1][0]
                cat_name = category_lst[len(category_lst) - 1][1]

            storeDict = self.session.query(Item.item_name, Item.avatar, Item.description,
                                           Item.code, Item.price, Item.tax, Item.subtotal,
                                           category.cat_name). \
                filter(Item.status == 11). \
                filter(Item.category == category.code). \
                filter(category.type_product >= 131). \
                order_by(category.cat_name.asc()).all()
            self.msg = {}
            for dataLst in storeDict:

                category_name = dataLst._asdict()[category.cat_name.name]
                if category_name != cat_name:
                    prodlst = [{Item.item_name.name: "", Item.avatar.name: "",
                                Item.description.name: "", Item.price.name: "",
                                Item.tax.name: "", Item.subtotal.name: "",
                                Item.code.name: 0, category.cat_name.name: category_name}]
                    self.msg[category_name] = prodlst
                    cat_name = category_name
                else:
                    prodlst = self.msg[cat_name]
                dicStore = {category.cat_name.name: category_name}

                for key in DBProcess(Item.Item_tbl).getColumnDefinition:
                    colname = key["name"]  # Getting the column name.
                    if colname in dataLst._asdict():  # Just if the column name is on the dictionary, add it to the dictStore.
                        dicStore[colname] = DBProcess(Item.Item_tbl).parse2publish(dataLst._asdict()[colname])

                prodlst.append(dicStore)

            return {"status": 200, "value": self.msg, 'type': 'application/json'}

        def getSaleProducts(self, inputs):
            storeDict = self.session.query(Item.item_name, Item.code, Item.price, Item.status, Item.category,
                                           Status.description, Type.tpname, Item.item_type,
                                           category.cat_name, category.cat_type, category.type_product). \
                filter(Status.code == Item.status).filter(Type.code == Item.item_type).filter(
                category.code == Item.category).filter(Type.code <= 41)
            if Item.category.name in inputs:
                storeDict = storeDict.filter(category.code == int(inputs[Item.category.name]))
            storeDict = storeDict.order_by(category.code)
            self.msg = {}
            produs = {}

            for dataLst in storeDict:

                cat_typename = Types().Get({Type.code.name: dataLst._asdict()[category.type_product.name]})["value"][0][
                    Type.tpname.name]
                category_name = dataLst._asdict()[category.cat_name.name]
                dicStore = {"status_name": dataLst._asdict()[Status.description.name],
                            "tpname": dataLst._asdict()["tpname"],
                            category.cat_name.name: category_name,
                            category.type_product.name:
                                Types().Get({Type.code.name: dataLst._asdict()[category.type_product.name]})
                                ["value"][0][Type.tpname.name],
                            "cat_typename": cat_typename}

                for key in DBProcess(Item.Item_tbl).getColumnDefinition:
                    colname = key["name"]  # Getting the column name.
                    if colname in dataLst._asdict():  # Just if the column name is on the dictionary, add it to the dictStore.
                        dicStore[colname] = DBProcess(Item.Item_tbl).parse2publish(dataLst._asdict()[colname])
                if category_name not in produs:
                    produs[category_name] = [dicStore]
                    self.msg[cat_typename] = [produs]
                else:
                    retLst = produs[category_name]
                    retLst.append(dicStore)
                    produs[category_name] = retLst

                ###Getting the companion and the terms if the product have it.

                # Additional
                addLst = []
                dicStore["companions"] = addLst
                additionals = product_additional.objects(product=dicStore[Item.code.name])
                for piece in additionals:
                    additional_info = self.session.query(Item.code, Item.item_name, Item.price, Item.subtotal,
                                                         Item.tax). \
                        filter_by(code=piece.additional).first()
                    addLst.append({"name": additional_info[1], "code": additional_info[0],
                                   "price": str(additional_info[2]),
                                   "subtotal": str(additional_info[3]),
                                   "tax": str(additional_info[4])})

                # Terms
                termsLst = []
                dicStore["terms"] = termsLst
                terms_data = product_term.objects(product=dicStore[Item.code.name])
                for piece in terms_data:
                    termsLst.append({"term": piece.term, "name": terms.objects(code=piece.term).first()._name})

                # Optionals
                optLst = []
                dicStore["optionals"] = optLst
                optionals = product_optionals.objects(product=dicStore[Item.code.name])
                for piece in optionals:
                    optional_info = self.session.query(Item.code, Item.item_name, Item.price, Item.subtotal,
                                                       Item.tax). \
                        filter_by(code=piece.optional).first()
                    optLst.append({"name": optional_info[1], "code": optional_info[0],
                                   "price": str(optional_info[2]),
                                   "subtotal": str(optional_info[3]),
                                   "tax": str(optional_info[4])})

                # Compounds
                cmpLst = []
                dicStore["compounds"] = cmpLst
                compoundlst = product_compounds.objects(product=dicStore[Item.code.name])
                for piece in compoundlst:
                    compound_info = self.session.query(Item.code, Item.item_name, Item.price, Item.subtotal,
                                                       Item.tax). \
                        filter_by(code=piece.compound).first()
                    cmpLst.append({"name": compound_info[1], "code": compound_info[0],
                                   "price": str(compound_info[2]),
                                   "subtotal": str(compound_info[3]),
                                   "tax": str(compound_info[4])})
            return {"status": 200, "value": self.msg, 'type': 'application/json'}

        def getHappyHour(self, inputs):
            # This method gets the data, from the db.
            storeDict = self.session.query(Item.code, Item.item_name, Item.subtotal). \
                filter(Item.category == int(inputs["category"]))
            dataCol = []

            for dataLst in storeDict:
                dicStore = {}
                for key in DBProcess(Item.Item_tbl).getColumnDefinition:
                    colname = key["name"]  # Getting the column name.
                    if colname in dataLst._asdict():  # Just if the column name is on the dictionary,
                        # add it to the dictStore.
                        dicStore[colname] = DBProcess(Item.Item_tbl).parse2publish(dataLst._asdict()[colname])
                        if colname == Item.item_name.name:
                            new_name = dicStore[colname]
                            dicStore[colname] = new_name

                disc_info = discount.objects(product=dicStore[Item.code.name]).first()
                if disc_info != None:
                    dicStore["discount"] = disc_info.amount_disc
                    dicStore["start_hour"] = disc_info.start_hour
                    dicStore["end_hour"] = disc_info.end_hour
                    dicStore["days"] = disc_info.days
                    dicStore["status_disc"] = disc_info.status
                else:
                    dicStore["discount"] = 0.00
                    dicStore["start_hour"] = None
                    dicStore["end_hour"] = None
                    dicStore["days"] = ''
                    dicStore["status_disc"] = 12
                dataCol.append(dicStore)
            return {"status": 200, "value": dataCol, 'type': 'application/json'}

        def getInvertoryUsed(self, inputs):
            # Retrivve the products used on the inventory.
            productsUsed = self.session.query(ProductPre.product).filter(cashbox=int(inputs["cashbox"])).distinct()
            self.msg = []
            for piece in productsUsed:
                del piece.__dict__['_sa_instance_state']
                piece.__dict__[ProductPre.subtotal.name] = float(piece.__dict__[ProductPre.subtotal.name])
                piece.__dict__[ProductPre.tax.name] = float(piece.__dict__[ProductPre.tax.name])
                piece.__dict__[ProductPre.discount.name] = float(piece.__dict__[ProductPre.discount.name])
                piece.__dict__[ProductPre.total.name] = float(piece.__dict__[ProductPre.total.name])
                self.msg.append(piece.__dict__)

            return {"status": 200, "value": self.msg, 'type': 'application/json'}

        def getCatalog(self, inputs):
            storeDict = self.session.query(Item.item_name, Item.code, Item.price, Item.status, Item.category,
                                           Status.description, Type.tpname, Item.item_type, Item.subtotal, Item.tax,
                                           category.cat_name, category.printer, category.avatar, category.cat_type,
                                           category.type_product, Item.avatar, category.tp_avatar). \
                filter(Status.code == Item.status). \
                filter(Type.code == Item.item_type). \
                filter(category.status == 11). \
                filter(Item.status == 11). \
                filter(category.code == Item.category). \
                filter(Type.code <= 41). \
                order_by(category.code.asc())
            self.msg = []
            produs = {}

            for dataLst in storeDict:
                cat_typename = self.session.query(Type.tpname). \
                    filter(Type.code == dataLst._asdict()
                [category.type_product.name]).first()
                category_name = dataLst._asdict()[category.cat_name.name]
                dicStore = {"status_name": dataLst._asdict()[Status.description.name],
                            "tpname": dataLst._asdict()[Type.tpname.name],

                            "cat_" + category.avatar.name: dataLst._asdict()[category.avatar.name],

                            category.cat_name.name: category_name,
                            category.type_product.name: dataLst._asdict()[category.type_product.name],
                            category.printer.name: dataLst._asdict()[category.printer.name]}
                if (cat_typename != None):
                    dicStore["cat_typename"] = cat_typename[0]

                for key in DBProcess(Item.Item_tbl).getColumnDefinition:
                    colname = key["name"]  # Getting the column name.
                    if colname in dataLst._asdict():  # Just if the column name is
                        #  on the dictionary, add it to the dictStore.
                        if colname == "avatar":
                            dicStore["item_" + colname] = DBProcess(Item.Item_tbl).parse2publish(
                                dataLst._asdict()[colname])
                        else:
                            dicStore[colname] = DBProcess(Item.Item_tbl).parse2publish(dataLst._asdict()[colname])
                ###Getting the companion and the terms if the product have it.

                #  #Terms
                termsLst = []
                dicStore["terms"] = termsLst
                terms_data = product_term.objects(product=dicStore[Item.code.name])
                for piece in terms_data:
                    termsLst.append({"term": piece.term, "name": terms.objects(code=piece.term).first()._name})

                self.msg.append(dicStore)
            # raise Exception(str(self.msg))

            return {"status": 200, "value": self.msg, 'type': 'application/json'}

        def moveProduct(self, inputs):
            move = CodeGen().GenCode({"table": "products_move", "column": "code"})

            products_move(code=move, product=int(inputs["product"]), amount=float(inputs["amount"])).save()

            return {"status": 200, "value": {"code": move}, 'type': 'application/json'}

        def newTerm(self, inputs):
            code = CodeGen().GenCode({"table": "terms", "column": "code"})

            terms(code=code, _name=inputs["name"],
                  notes=inputs["notes"]).save()

            return {"status": 200, "value": {"code": code}, 'type': 'application/json'}

        def modTerm(self, inputs):
            code = int(inputs["code"])

            terms.objects(code=code).update(set___name=inputs["name"],
                                            set__notes=inputs["notes"])

            return {"status": 200, "value": {"code": code}, 'type': 'application/json'}

        def add2term(self, inputs):
            # Connecting terms with products.
            _terms_ = json.loads(inputs["terms"]) if isinstance(inputs["terms"], str) else inputs["terms"]
            if len(_terms_) > 0:
                product_term.objects(product=int(inputs["product"])).delete()
                for term in _terms_:
                    if isinstance(inputs["terms"], str):
                        if term != None:
                            product_term(product=int(inputs["product"]), term=int(term["code"]),
                                         name=term["name"]).save()
                    else:
                        product_term(product=int(inputs["product"]), term=term,
                                     name=terms.objects(code=term).first()._name).save()

            return {"status": 200, "value": {"code": int(inputs["product"])}, 'type': 'application/json'}

        def getTerm(self, inputs):
            if "_name" in inputs:
                termslst = json.loads(terms.objects(_name__icontains=inputs["_name"]).to_json())
            elif "code" in inputs:
                termslst = json.loads(terms.objects(code=int(inputs["code"])).to_json())
            else:
                termslst = json.loads(terms.objects().to_json())
            return {"status": 200, "value": termslst, 'type': 'application/json'}

        def delTermProduct(self, inputs):
            product_term(product=int(inputs["product"]), term=int(inputs["term"])).delete()

            return {"status": 200, "msg": "Termino y producto eliminado", 'type': 'application/json'}

        def newAdditionals(self, inputs):
            # Connecting terms with products.
            _additional_ = json.loads(inputs["additional"]) if isinstance(inputs["additional"], str) \
                else inputs["additional"]
            product_additional.objects(product=int(inputs["product"])).delete()

            additionalLst = []
            for additional in _additional_:
                if additional != None:
                    additionalLst.append(product_additional(
                        product=int(inputs["product"]), additional=int(additional["code"]),
                        status=11, cycle=additional["cycle"],
                        name=additional["name"], price=float(additional["price"])))
            if len(additionalLst) > 0:
                product_additional.objects.insert(additionalLst)

            return {"status": 200, "value": {"code": int(inputs["product"])}, 'type': 'application/json'}

        def addAdditional(self, inputs):
            # Connecting terms with products.
            _additional_ = json.loads(inputs["additional"]) if isinstance(inputs["additional"], str) \
                else inputs["additional"]
            product_additional.objects(product=int(inputs["product"])).delete()

            for additional in _additional_:
                if additional != '':
                    product_additional(product=int(inputs["product"]),
                                       additional=int(additional)).save()

            return {"status": 200, "value": {"code": int(inputs["product"])}, 'type': 'application/json'}

        def getAdditional(self, inputs):
            addlst = []
            if "product" in inputs:
                addlst = json.loads(product_additional.objects(product=int(inputs["product"])).to_json())
            else:
                addlst = json.loads(product_additional.objects().to_json())

            return {"status": 200, "value": addlst, 'type': 'application/json'}

        def addOptional(self, inputs):
            # Connecting terms with products.
            product_optionals.objects(product=int(inputs["product"])).delete()
            _optionals_ = str(inputs["optionals"]).split(",")
            for optional in _optionals_:
                product_optionals(product=int(inputs["product"]),
                                  optional=int(optional)).save()

            return {"status": 200, "value": {"code": int(inputs["product"])}, 'type': 'application/json'}

        def newOptionals(self, inputs):
            # Connecting terms with products.
            _optionals_ = json.loads(inputs["optionals"]) if isinstance(inputs["optionals"], str) \
                else inputs["optionals"]
            product_optionals.objects(product=int(inputs["product"])).delete()

            optionalsLst = []
            for optionals in _optionals_:
                if optionals != None:
                    optionalsLst.append(product_optionals(
                        product=int(inputs["product"]), optional=int(optionals["code"]),
                        status=11, cycle=optionals["cycle"],
                        name=optionals["name"], price=float(optionals["price"])))
            if len(optionalsLst) > 0:
                product_optionals.objects.insert(optionalsLst)

            return {"status": 200, "value": {"code": int(inputs["product"])}, 'type': 'application/json'}

        def getOptional(self, inputs):
            optlst = []
            if "product" in inputs:
                optlst = json.loads(product_optionals.objects(product=int(inputs["product"])).to_json())
            else:
                optlst = json.loads(product_optionals.objects().to_json())

            return {"status": 200, "value": optlst, 'type': 'application/json'}

        def addCompound(self, inputs):
            # Connecting terms with products.

            product_compounds(product=int(inputs["product"]),
                              compound=int(inputs["compound"])).save()

            return {"status": 200, "value": {"code": int(inputs["product"])}, 'type': 'application/json'}

        def newCompounds(self, inputs):
            # Connecting terms with products.
            _compounds_ = json.loads(inputs["compounds"]) if isinstance(inputs["compounds"], str) \
                else inputs["compounds"]
            if len(_compounds_) > 0:
                product_compounds.objects(product=int(inputs["product"])).delete()

                compoundsLst = []
                for compounds in _compounds_:
                    if compounds != None:
                        compoundsLst.append(product_compounds(
                            product=int(inputs["product"]), compound=int(compounds["code"]),
                            status=11, cycle=compounds["cycle"],
                            name=compounds["name"], price=float(compounds["price"])))
                if len(compoundsLst) > 0:
                    product_compounds.objects.insert(compoundsLst)
            return {"status": 200, "value": {"code": int(inputs["product"])}, 'type': 'application/json'}

        def getCompounds(self, inputs):
            cmplst = json.loads(product_compounds.objects().to_json())
            return {"status": 200, "value": cmplst, 'type': 'application/json'}

        def getCompound(self, inputs):
            cmplst = []
            for piece in product_compounds.objects(product=int(inputs["product"])):
                cmplst.append({"product": piece.product,
                               "compound": piece.optional})

            return {"status": 200, "value": cmplst, 'type': 'application/json'}


if __name__ == '__main__':
    None
__author__ = 'hidura'
