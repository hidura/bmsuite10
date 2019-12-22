import json
from sqlalchemy.orm.session import sessionmaker

from tools.DataBase.CodeGenerator import CodeGen
from tools.DataBase.Connect import conection
from tools.DataBase.Definition import db
from tools.DataBase.Definition.AccountsTbl import AccountsTbl
from tools.DataBase.Definition.Status import Status
from tools.DataBase.Definition.Type import Type
from tools.DataBase.Definition.Views.getaccounts import getaccounts
from tools.DataBase.ODM.DataModelODM import account_movement, ncfType, tax, paytype_det, billtype_det, ncf_codes
from tools.DataBase.Process import DBProcess
from tools.main.general import general
from tools.main.process.General import General
from tools.main.process.Types import Types


class Accounts:
    def __init__(self):

        self.status = 200
        self.msg = None
        self.type = "text/plain"

        self.session = db.session


    def create(self, inputs):
        # This method will create an expense.
        self.code = CodeGen().GenCode({"table": AccountsTbl.__tablename__, "column": AccountsTbl.code.name})
        # Generating the code.

        start_amount = 0.00
        if AccountsTbl.current_amount.name in inputs:
            start_amount=float(inputs[AccountsTbl.current_amount.name])

        acc_type=1481
        if AccountsTbl.account_type.name in inputs:
            acc_type = str(inputs[AccountsTbl.account_type.name])

        classification = 1481
        if AccountsTbl.classification.name in inputs:
            classification = str(inputs[AccountsTbl.classification.name])

        position=""
        if AccountsTbl.position.name in inputs:
            position = str(inputs[AccountsTbl.position.name])
        self.session.add(AccountsTbl(code=self.code, status=11,
                                     account_name=inputs[AccountsTbl.account_name.name],
                                     current_amount=start_amount, position=position,
                                     account_type=acc_type, classification=classification))
        # Saving

        self.session.commit()
        
        return {"status": 200, "value": {AccountsTbl.code.name: self.code}, 'type': 'application/json'}

    def Handle(self, inputs):
        # This method will modify an expanse.
        item = int(inputs[AccountsTbl.code.name])

        storeDict = {}
        for column in DBProcess(AccountsTbl.Accounts_tbl).getColumnDefinition:
            if column["name"] in inputs:
                storeDict[column["expr"]] = DBProcess(AccountsTbl.Accounts_tbl).parse(column, inputs[column["name"]])

        self.session.query(AccountsTbl).filter_by(code=item).update(storeDict)

        self.session.commit()

        return {"status": 200, "value": {AccountsTbl.code.name: item}, 'type': 'application/json'}

    def Get(self, inputs):
        # This method gets the data, from the db.
        storeDict = self.session.query(AccountsTbl, Status.description).\
            filter(Status.code == AccountsTbl.status)

        if AccountsTbl.code.name in inputs:
            storeDict = storeDict.filter(AccountsTbl.code == int(inputs[AccountsTbl.code.name]))

        if AccountsTbl.account_type.name in inputs:
            storeDict = storeDict.filter(AccountsTbl.acc_type == int(inputs[AccountsTbl.account_type.name]))

        if AccountsTbl.account_name.name in inputs:
            storeDict = storeDict.filter(AccountsTbl.account_name.ilike("%" + str(inputs[AccountsTbl.account_name.name]) + "%"))


        # The next area is in charge to extract the information,
        # from the store Dict and add it to the dataCol to be returned

        dataCol = []
        for dataLst in storeDict:
            dicStore = {"status_name": dataLst._asdict()[Status.description.name]}

            for key in DBProcess(AccountsTbl.Accounts_tbl).getColumnDefinition:
                dataDict = dataLst._asdict()[AccountsTbl.__name__].__dict__  # Getting the dictionary of the list.
                colname = key["name"]  # Getting the column name.
                if colname in dataDict:  # Just if the column name is on the dictionary, add it to the dictStore.

                    dicStore[colname] = DBProcess(AccountsTbl.Accounts_tbl).parse2publish(dataDict[colname])

            dataCol.append(dicStore)
            # Appending everything to be returned
        if "wrap_to" in inputs:
            dataCol = General().WrapInfo(inputs, dataCol,
                                         [{AccountsTbl.code.name: "id"},
                                          {AccountsTbl.account_name.name: "text"}])
        return {"status": 200, "value": dataCol, 'type': 'application/json'}

    def transfer(self, inputs):
        account_from = None
        if "account_from" in inputs:
            account_from = int(inputs["account_from"])
        account_to = int(inputs["account_to"])
        notes = ""
        if "notes" in inputs:
            notes = str(inputs["notes"])

        amount = float(inputs["amount"])
        code = CodeGen().GenCode({"table": "account_movement", "column": "code"})

        acc_from_info = self.session.query(getaccounts). \
            filter(getaccounts.code == account_from)
        acc_to_info = self.session.query(getaccounts). \
            filter(getaccounts.code == account_to)

        account_movement(credit=account_from, debit=account_to, credit_name=acc_from_info.account_name,
                         credit_code=int(acc_from_info.position_account),
                         debit_name=acc_to_info.account_name,
                         debit_code=int(acc_to_info.position_account),
                         amount=amount, register_date=general().date2julian(), code=code, notes=notes).save()

        cur_amount = self.session.query(AccountsTbl.current_amount). \
            filter(AccountsTbl.code == account_to)

        if (cur_amount != None):
            new_amount = amount + float(cur_amount.first()[0])
            self.session.query(AccountsTbl).filter(AccountsTbl.code == account_to) \
                .update({AccountsTbl.current_amount.name: new_amount})
            self.session.commit()

        if account_from != None:
            cur_amount = float(self.session.query(AccountsTbl.current_amount). \
                               filter(AccountsTbl.code == account_from).first()[0])

            cur_amount -= amount
            self.session.query(AccountsTbl).filter(AccountsTbl.code == account_from) \
                .update({AccountsTbl.current_amount.name: cur_amount})

            self.session.commit()

        return {"status": 200, "value": {"code": code}, 'type': 'application/json'}

    def getNCFTypes(self, inputs):
        self.msg=ncfType.objects(name__icontains=inputs["name"]).to_json()
        return {"status": 200, "value": json.loads(self.msg), 'type': 'application/json'}

    def getAccountsBy(self, inputs):

        query = self.session.query(getaccounts)
        if getaccounts.account_type.name in inputs:
            query=query.filter(getaccounts.account_type==str(inputs[getaccounts.account_type.name]))
        self.msg = []
        for piece in query:
            del piece.__dict__['_sa_instance_state']
            self.msg.append(piece.__Publish__())
        return {"status": 200, "value": json.dumps({"data":self.msg}), 'type': 'application/json'}

    def getBalanceSheet(self, inputs):
        from_date = general().date2julian(inputs['from'])
        to_date = general().date2julian(inputs['to'])
        msg={}
        for account_info in self.session.query(getaccounts).order_by(getaccounts.position_account.asc()):
            debit = account_movement.objects(register_date__gte=from_date,
                                            register_date__lte=to_date, debit=account_info.code).\
                sum('amount')

            credit = account_movement.objects(register_date__gte=from_date,
                                             register_date__lte=to_date, credit=account_info.code). \
                sum('amount')
            msg[account_info.position_account]={
                "acc_name":account_info.account_name,
                "balance":debit-credit,
                "level_name":account_info.level_name,
                "classification":account_info.classification}

        return {"status": 200, "value": json.dumps(msg), 'type': 'application/json'}
    def HandlePayType(self, inputs):

        if "code" in inputs:
            code=int(inputs["code"])
            tpinputs={Type.tpname.name:inputs[Type.tpname.name],
                      "code":code}
            Types().Handle(tpinputs)
            paytype_det.objects(code=code).delete()
        else:
            tpinputs = {Type.tpname.name: inputs[Type.tpname.name],
                        "level": 11}
            code=Types().create(tpinputs)["value"][Type.code.name]
        paytplst=json.loads(inputs["paytplst"])
        reference=False
        if int(inputs["reference"])==1:
            reference=True
        percent=int(inputs["percent"])
        paytype_det.objects(typid=code).delete()
        paytype_det(typid=code, denomination=paytplst, reference=reference,percent_extra=percent ).save()
        self.msg={"msg":"Salvado exitosamente", "code":code}

        return {"status": 200, "value": self.msg, 'type': 'application/json'}

    def getPayType(self, inputs):
        self.msg=[]
        _query = self.session.query(Type).filter_by(level=11)
        if "code" in inputs:
            _query=_query.filter_by(code=int(inputs["code"]))
        for piece in _query:
            del piece.__dict__['_sa_instance_state']
            paydetails=json.loads(paytype_det.objects(typid=piece.__dict__["code"]).to_json())
            piece.__dict__["paydetails"] ={}# By default the dictionary is empty
            if len(paydetails)>1:
                piece.__dict__["paydetails"]=paydetails[0]

            self.msg.append(piece.__dict__)

        return {"status": 200, "value": self.msg, 'type': 'application/json'}


    def HandleBillType(self, inputs):

        if "code" in inputs:
            code=int(inputs["code"])

            tpinputs={"code":code}
            if Type.tpname.name in inputs:
                tpinputs[Type.tpname.name]=inputs[Type.tpname.name]
            Types().Handle(tpinputs)
            paytype_det.objects(code=code).delete()
        else:
            tpinputs = {Type.tpname.name: inputs[Type.tpname.name],
                        "level": 10}
            code=Types().create(tpinputs)["value"][Type.code.name]


        reference=False
        if int(inputs["reference"])==1:
            reference=True
        percent=int(inputs["percent"])
        billtype_det.objects(typid=code).delete()
        billtype_det(typid=code, reference=reference,percent_extra=percent ).save()
        self.msg={"msg":"Salvado exitosamente", "code":code}
        return {"status": 200, "value": self.msg, 'type': 'application/json'}

    def getBillType(self, inputs):
        self.msg=[]
        _query = self.session.query(Type).filter_by(level=10)
        if "code" in inputs:
            _query=_query.filter_by(code=int(inputs["code"]))
        for piece in _query:
            del piece.__dict__['_sa_instance_state']
            billdetails=json.loads(billtype_det.objects(typid=piece.__dict__["code"]).to_json())
            piece.__dict__["billdetails"] ={}
            if len(billdetails)>0:
                piece.__dict__["billdetails"]=billdetails[0]
            self.msg.append(piece.__dict__)

        return {"status": 200, "value": self.msg, 'type': 'application/json'}

    def addTax(self, inputs):
        if tax.objects(name__icontains=str(inputs["name"]).upper()).first()!=None:
            return {"status": 200, "value": {"error":"No puede crear un impuesto con el mismo nombre"}, 'type': 'application/json'}
        else:
            code = CodeGen().GenCode({"table": "tax", "column": "code"})
            tax(name=str(inputs["name"]).upper(), percent=float(inputs["percent"]), code=code).save()
            return {"status": 200, "value": {"code":code}, 'type': 'application/json'}

    def getTax(self, inputs):
        self.msg= json.loads(tax.objects(name__icontains=str(inputs["name"]).lower()).to_json())
        return {"status": 200, "value":  self.msg, 'type': 'application/json'}

    def HandleTax(self, inputs):
        tax.objects(code=int(inputs["code"])).\
            update(set__name=str(inputs["name"]).upper(), set__percent=float(inputs["percent"]))
        return {"status": 200, "value": {"code":inputs["code"]}, 'type': 'application/json'}

    def addNCF(self, inputs):
        # Connecting terms with products.
        ncf_initial=int(inputs["ncf_initial"])
        ncf_last = int(inputs["ncf_last"])
        exp = str(inputs["exp"])

        ncfLst = []
        ncfRet = []
        for ncf in range(ncf_initial, ncf_last):
            code = CodeGen().GenCode({"table": "ncf_codes", "column": "code"})
            header = ncfType.objects(code=int(inputs["ncf_type"])).first().header
            ncfRet.append(header+str(ncf).zfill(8))
            ncfLst.append(ncf_codes(code=code, secuence=str(ncf).zfill(8),exp=exp,
                                    ncf_type=int(inputs["ncf_type"]), status=11))
        if len(ncfLst) > 0:
            ncf_codes.objects.insert(ncfLst)

        return {"status": 200, "value": ncfRet, 'type': 'application/json'}

if __name__ == '__main__':
    Accounts()

__author__ = 'hidura'
