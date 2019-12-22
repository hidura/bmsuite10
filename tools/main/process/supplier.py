from sqlalchemy.orm.session import sessionmaker

from tools.DataBase.CodeGenerator import CodeGen
from tools.DataBase.Connect import conection
from tools.DataBase.Definition import db
from tools.DataBase.Definition.Contact import Contact
from tools.DataBase.Definition.Status import Status
from tools.DataBase.Definition.Supplier import Supplier
from tools.DataBase.Process import DBProcess
from tools.main.process.manContact import ManContact


class supplier:
    def __init__(self):
        self.status = 200
        self.msg = None
        self.type = "text/plain"

        self.session = db.session

    def create(self, inputs):
        supplier_name = None
        if Supplier.sup_name.name in inputs:
            supplier_name =inputs[Supplier.sup_name.name]

        supplier = CodeGen().GenCode({"table": Supplier.__tablename__, "column": Supplier.code.name})
        self.session.add(Supplier(sup_name=supplier_name, code=supplier))
        self.session.commit()
        self.type = "application/json"
        self.msg = {"code": supplier}
        self.status = 200
        return {"status": self.status, "value": self.msg, "type": self.type}


    def Handle(self, inputs):
        supplier_code = int(inputs[Supplier.code.name])
        supplierCol = self.session.query(Supplier).filter_by(code=supplier_code).first()
        contactCol = []
        idCon = 0
        if supplierCol.contact == None and Supplier.contact.name in inputs:
            # Means that the contact is created and going to be updated
            ManContact().Handle(inputs)
            idCon = int(inputs[Supplier.contact.name])
        else:
            # Means that the contact is not created.
            idCon = ManContact().create(inputs)["value"][Contact.code.name]
            inputs[Supplier.contact.name] = idCon
            ManContact().Handle(inputs)

        storeDict = {}
        for column in DBProcess(Supplier.supplier_tbl).getColumnDefinition:
            if column["name"] in inputs:
                storeDict[column["expr"]] = DBProcess(Supplier.supplier_tbl).parse(column, inputs[column["name"]])

        self.session.query(Supplier).filter_by(code=supplier_code).update(storeDict)
        self.session.commit()

        self.type = "application/json"
        self.msg = {"code": supplier_code}
        self.status = 200
        return {"status": self.status, "value": self.msg, "type": self.type}


    def Get(self, inputs):
        dataCol = []
        """The module of find the information of a Client."""
        storeDict = []
        if Supplier.sup_name.name in inputs:
            storeDict = self.session.query(Supplier, Status.description).\
                filter(Supplier.sup_name.ilike("%" + inputs[Supplier.sup_name.name] + "%")).\
                filter(Supplier.status == Status.code)

        elif Supplier.code.name in inputs:
            storeDict = self.session.query(Supplier, Status.description).\
                filter(Supplier.status == Status.code).\
                filter(Supplier.code == int(inputs[Supplier.code.name]))

        storeDict = storeDict.order_by(Supplier.sup_name.asc())
        for dataLst in storeDict:
            dicStore = {"status_name": dataLst._asdict()[Status.description.name]}

            for buyBillKey in DBProcess(Supplier.supplier_tbl).getColumnDefinition:
                billDict = dataLst._asdict()[Supplier.__name__].__dict__  # Getting the dictionary of the list.
                colname = buyBillKey["name"]  # Getting the column name.
                if colname in billDict:  # Just if the column name is on the dictionary, add it to the dictStore.
                    dicStore[colname] = billDict[colname]

            dataCol.append(dicStore)
            # Appending everything to be returned
        return {"status": 200, "value": dataCol, 'type': 'application/json'}

if __name__ == '__main__':
    None

__author__ = 'hidura'
