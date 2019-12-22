import os

from werkzeug.utils import secure_filename

from tools.DataBase.CodeGenerator import CodeGen
from tools.DataBase.Definition import db
from tools.DataBase.Definition.Status import Status
from tools.DataBase.Definition.Type import Type
from tools.DataBase.Definition.category import category
from tools.DataBase.Definition.company import company
from tools.DataBase.ODM.DataModelODM import printer_reg, product_type
from tools.DataBase.Process import DBProcess
from tools.main import general
from tools.main.process.General import General
from tools.main.process.Types import Types


class Categories:
    def __init__(self):
        self.status = 200
        self.msg = None
        self.type = "text/plain"

        self.session = db.session

    def create(self, inputs):
        # This method will create a category.
        self.code = CodeGen().GenCode({"table": category.__tablename__, "column": category.code.name})
        # Generating the code.
        cat_type = 61
        if category.cat_type.name in inputs:
            cat_type = int(inputs[category.cat_type.name])
        status=12
        if category.status.name in inputs:
            status=inputs[category.status.name]
        prod_type=131
        if category.type_product.name in inputs:
            prod_type =int(inputs[category.type_product.name])
        printer=""
        if category.printer.name in inputs:
            printer = printer_reg.objects(code=int(inputs[category.printer.name])).first().name

        logo_path = ""
        logo_file = "".encode()
        if "avatar" in inputs:
            from app import app
            file = inputs['avatar']
            if file.filename == '':
                mgs = "No file has been selected"
            if file and general().allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                file_dst = app.config['UPLOAD_FOLDER'] + "/" + filename
                del inputs['avatar']
                inputs['avatar'] = file_dst
            else:

                del inputs["avatar"]



        self.session.add(category(code=self.code, status=int(status),avatar=logo_path,
                                  company=int(inputs[category.company.name]),
                                  cat_name=inputs[category.cat_name.name],type_product=prod_type,
                                  cat_type=cat_type, printer=printer))
        # Saving
        self.session.commit()
        return {"status": 200, "value": {category.code.name: self.code}, 'type': 'application/json'}

    def Handle(self, inputs):
        # This method will modify an expanse.
        item = int(inputs[category.code.name])
        category_info=self.session.query(category).filter_by(code=item).first()
        logo_path=category_info.avatar
        if category.avatar.name in inputs:

            if "avatar" in inputs:

                from app import app
                file = inputs['avatar']
                if file.filename == '':
                    mgs = "No file has been selected"
                if file and general().allowed_file(file.filename):
                    filename = secure_filename(file.filename)
                    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                    file_dst = app.config['UPLOAD_FOLDER'] + "/" + filename
                    del inputs['avatar']
                    inputs['avatar'] = file_dst
                else:

                    del inputs["avatar"]

        storeDict = {}
        printer = category_info.printer
        if category.printer.name in inputs:
            printer = printer_reg.objects(code=int(inputs[category.printer.name])).first().name

        inputs[category.printer.name]=printer
        for column in DBProcess(category.category_tbl).getColumnDefinition:
            if column["name"] in inputs:
                storeDict[column["expr"]] = DBProcess(category.category_tbl).parse(column, inputs[column["name"]])



        self.session.query(category).filter_by(code=item).update(storeDict)

        self.session.commit()
        return {"status": 200, "value": {category.code.name: item}, 'type': 'application/json'}

    def Get(self, inputs):
        # This method gets the data, from the db.
        storeDict = self.session.query(category, Status.description, company._name).\
            filter(Status.code == category.status,Type.code==category.cat_type).\
            filter(company.code == category.company)

        if category.code.name in inputs:
            storeDict = storeDict.filter(category.code == int(inputs[category.code.name]))

        if category.cat_type.name in inputs:
            storeDict = storeDict.filter(category.cat_type == int(inputs[category.cat_type.name]))

        if category.cat_name.name in inputs:
            storeDict = storeDict.filter(category.cat_name.ilike("%" + str(inputs[category.cat_name.name]) + "%"))


        # The next area is in charge to extract the information,
        # from the store Dict and add it to the dataCol to be returned

        dataCol = []
        for dataLst in storeDict:
            dicStore = {"status_name": dataLst._asdict()[Status.description.name],
                        "company_name":dataLst._asdict()[company._name.name]}

            for key in DBProcess(category.category_tbl).getColumnDefinition:
                dataDict = dataLst._asdict()[category.__name__].__dict__  # Getting the dictionary of the list.
                colname = key["name"]  # Getting the column name.
                if colname in dataDict:  # Just if the column name is on the dictionary, add it to the dictStore.

                    dicStore[colname] = DBProcess(category.category_tbl).parse2publish(dataDict[colname])

            product_type = self.session.query(Type).filter_by(code=dicStore[category.type_product.name]).first()
            if product_type!=None:
                dicStore["product_type_name"] = product_type.tpname

            category_type = self.session.query(Type).filter_by(code=dicStore[category.cat_type.name]).first()
            if category_type != None:
                dicStore["categorytp_name"] = category_type.tpname
            if printer_reg.objects(name=dicStore["printer"]).first()!=None:
                dicStore["printer_id"]=printer_reg.objects(name=dicStore["printer"]).first().code
            dataCol.append(dicStore)
            # Appending everything to be returned
        if "wrap_to" in inputs:
            dataCol = General().WrapInfo(inputs, dataCol,
                                         [{category.code.name: "id"},
                                          {category.cat_name.name: "text"}])

        return {"status": 200, "value": dataCol, 'type': 'application/json'}


    def create_type(self, inputs):
        # This method will create a category type.
        inputs[Type.level.name]=13# Fixing the level to the
        self.code = Types().create(inputs)["value"][Type.code.name]

        logo_path = "dinner.png"
        if category.tp_avatar.name in inputs:
            logo_path = inputs[category.tp_avatar.name]["filename"]
            logo_file = inputs[category.tp_avatar.name]["value"]
            storeDir = inputs["__documentroot__"] + "/resources/site/" + "products/"
            inputs[category.avatar.name] = logo_path
            file = open(storeDir + logo_path, "w", encoding="ISO-8859-1")
            file.write(logo_file.decode("ISO-8859-1"))
            file.close()
        product_type(prod_type=self.code, avatar=logo_path).save()

        # Saving
        self.session.commit()
        return {"status": 200, "value": {category.code.name: self.code}, 'type': 'application/json'}


    def handle_type(self, inputs):
        # This method will create a category type.
        inputs[Type.level.name]=13# Fixing the level to the
        self.code = Types().create(inputs)["value"][Type.code.name]

        logo_path = product_type.objects(prod_type=self.code).first().avatar

        if category.tp_avatar.name in inputs:
            logo_path = inputs[category.tp_avatar.name]["filename"]
            logo_file = inputs[category.tp_avatar.name]["value"]
            storeDir = inputs["__documentroot__"] + "/resources/site/" + "products/"
            inputs[category.avatar.name] = logo_path
            file = open(storeDir + logo_path, "w", encoding="ISO-8859-1")
            file.write(logo_file.decode("ISO-8859-1"))
            file.close()

        product_type.objects(prod_type=self.code).update(set__avatar=logo_path)
        storeDict={category.tp_avatar.name:logo_path}
        self.session.query(category).filter_by(type_product=self.code).update(storeDict)

        # Saving
        self.session.commit()
        return {"status": 200, "value": {category.code.name: self.code}, 'type': 'application/json'}

    def getSaleCategory(self, inputs):

        storeDict = self.session.query(category.cat_name, category.avatar, category.code, category.printer). \
            filter(category.cat_type == 61).order_by(category.cat_name.asc())

        if category.type_product.name in inputs:
            storeDict=storeDict.filter(category.type_product==int(inputs[category.type_product.name]))


        self.msg = []
        for dataLst in storeDict:
            dictStore = {category.cat_name.name: dataLst[0], category.avatar.name: dataLst[1],
                         category.code.name: dataLst[2] , category.printer.name: dataLst[3]}

            self.msg.append(dictStore)

        return {"status": 200, "value": self.msg, 'type': 'application/json'}

if __name__ == '__main__':
    None
    #print(Categories().Get({category.cat_name.name:""}))

__author__ = 'hidura'
