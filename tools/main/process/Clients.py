from mongoengine.connection import disconnect
from sqlalchemy import or_
from sqlalchemy.orm.session import sessionmaker

from tools.DataBase.CodeGenerator import CodeGen
from tools.DataBase.Connect import conection
from tools.DataBase.Definition import db
from tools.DataBase.Definition.Client import Client
from tools.DataBase.Definition.Contact import Contact
from tools.DataBase.Definition.Status import Status
from tools.DataBase.ODM.DataModelODM import PreOrder
from tools.DataBase.Process import DBProcess
from tools.main.process.Company import Company
from tools.main.process.manContact import ManContact


class Clients:
    def __init__(self):
        self.status = 200
        self.msg = None
        self.type = "text/plain"

        self.session = db.session

    def loadData(self, webPage, inputs, environ):
        dataCol=Company().getCallClients(inputs)["value"]
        tbd = webPage.find(id="tblregster")
        ul = webPage.find(id="pagination")
        for piece in range(1, 20):
            li = webPage.new_tag("li")
            if piece==1:
                li["class"]="active"
            li["onClick"]="getCurrent(this);"
            a=webPage.new_tag('a')
            a["href"]="#"
            a.string=str(piece)
            li.append(a)
            ul.append(li)

        for piece in dataCol["data"]:
            tr=webPage.new_tag("tr")

            td=webPage.new_tag("td")
            tr.append(td)
            td["style"]="display:none;"
            td.string=str(piece["code"])

            td=webPage.new_tag("td")
            tr.append(td)
            td.string=piece["name"]

            td=webPage.new_tag("td")
            tr.append(td)
            td.string=piece["telephone"]

            td=webPage.new_tag("td")
            tr.append(td)
            td.string=piece["address"]

            td=webPage.new_tag("td")
            tr.append(td)
            if piece["contact"]!=None:
                td.string=piece["contact"]
            button=webPage.new_tag("button")
            button["class"]="fa fa-user btn btn-info"
            button["onClick"]="setContact(this);"
            td.append(button)


            td=webPage.new_tag("td")
            tr.append(td)
            button=webPage.new_tag("button")
            button["class"]="fa fa-check btn btn-info"
            button["onClick"]="dispDate(this);"
            td.append(button)

            td=webPage.new_tag("td")
            tr.append(td)
            button=webPage.new_tag("button")
            button["class"]="fa fa-minus btn btn-danger"
            button["onClick"]="reject(this);"
            td.append(button)

            td=webPage.new_tag("td")
            tr.append(td)
            button=webPage.new_tag("button")
            button["class"]="fa fa-sticky-note btn btn-success"
            button["onClick"]="addComment(this);"
            td.append(button)


            tbd.append(tr)
            


    def create(self, inputs):
        client_name=""
        if Client.cl_name.name in inputs:
            client_name = inputs[Client.cl_name.name]
        rnc = ""
        if Client.rnc.name in inputs:
            rnc= inputs[Client.rnc.name]

        _address = ""
        if Client._address.name in inputs:
            _address = inputs[Client._address.name]
        telephone = ""
        if Client.telephone.name in inputs:
            telephone = inputs[Client.telephone.name]
        # price = 0
        # if Client.price.name in inputs:
        #     price = int(inputs[Client.price.name])
        ncf_type = 2
        if Client.ncf_type.name in inputs:
            ncf_type = int(inputs[Client.ncf_type.name])



        status=11
        if Client.status.name in inputs:
            status=int(inputs[Client.status.name])
        client = CodeGen().GenCode({"table": Client.__tablename__, "column": Client.code.name})
        self.session.add(Client(cl_name=client_name, code=client,ncf_type=ncf_type,
                                rnc=rnc, status=status, telephone=telephone,_address=_address,
                                #price=price
                                ))
        self.session.commit()

        self.type = "application/json"
        self.msg = {Client.code.name: client}
        self.status = 200
        return {"status": self.status, "value": self.msg, "type": self.type}

    def HandleClient(self, inputs):
        client = int(inputs[Client.code.name])
        clientCol = self.session.query(Client).filter_by(code=client).first()
        contactCol = []
        idCon=0
        if clientCol.contact == None and Client.cl_name.name not in inputs:
            # Means that the contact is not created.
            idCon = ManContact().create(inputs)["value"][Contact.code.name]
            inputs[Client.contact.name] = idCon
            ManContact().Handle(inputs)
        elif clientCol.contact == None and Client.contact.name in inputs:

            # Means that the contact is created and going to be updated
            if inputs[Client.contact.name] == 0:
                #This safe zone is because C#, when creates the structure, the default value of the int is 0 and well C#
                #is generating a big mistake.
                idCon = ManContact().create(inputs)["value"][Contact.code.name]
                inputs[Client.contact.name]=idCon
            ManContact().Handle(inputs)
            idCon=int(inputs[Client.contact.name])
        elif clientCol.contact == None and Contact.contact_name.name in inputs:
            idCon = ManContact().create(inputs)["value"][Contact.code.name]
            inputs[Client.contact.name] = idCon
            ManContact().Handle(inputs)
        storeDict = {}
        for column in DBProcess(Client.clients_tbl).getColumnDefinition:
            if column["name"] in inputs:
                storeDict[column["expr"]] = DBProcess(Client.clients_tbl).parse(column, inputs[column["name"]])

        self.session.query(Client).filter_by(code=client).update(storeDict)
        self.session.commit()


        self.type = "application/json"
        self.msg = {Client.code.name: client}

        self.status = 200
        return {"status": self.status, "value": self.msg, "type": self.type}

    def Get(self, inputs):
        dataCol = []
        """The module of find the information of a Client."""
        storeDict = []
        limit = 100
        if "limit" in inputs:
            limit=int(inputs["limit"])
        main_query=self.session.query(Client, Status.description, Contact).\
            outerjoin(Contact, Contact.code==Client.contact)

        if Client.cl_name.name in inputs:
            main_query =main_query.\
                filter(Client.cl_name.ilike("%" + inputs[Client.cl_name.name] + "%"))

        if Client.code.name in inputs:
            main_query =main_query. \
                filter(Client.code == int(inputs[Client.code.name]))

        if Client.rnc.name in inputs:
            main_query =main_query. \
                filter(Client.rnc.ilike("%" + inputs[Client.rnc.name] + "%"))

        if Client.telephone.name in inputs:
            if inputs[Client.telephone.name]!=None and inputs[Client.telephone.name]!="null":
                main_query = main_query. \
                filter(Client.telephone.ilike("%" + inputs[Client.telephone.name] + "%"))

        if Client.contact.name in inputs:
            main_query = main_query.\
                filter(Client.code == int(inputs[Client.contact.name]))
        storeDict=main_query.\
                filter(Status.code == Client.status).limit(limit)

        for dataLst in storeDict:
            dicStore = {"status_name": dataLst._asdict()["description"]}
            for keys in DBProcess(Client.clients_tbl).getColumnDefinition:
                dataDict = dataLst._asdict()[Client.__name__].__dict__  # Getting the dictionary of the list.

                colname = keys["name"]  # Getting the column name.
                if colname in dataDict:  # Just if the column name is on the dictionary, add it to the dictStore.
                    if colname == Client.contact.name and dataDict[colname] ==None:
                        dataDict[colname] = 0
                    dicStore[colname] =  DBProcess(Client.clients_tbl).parse2publish(dataDict[colname])

            if dataLst._asdict()[Client.__name__].__dict__ [Client.contact.name] >0:
                for keys in DBProcess(Contact.Contact_tbl).getColumnDefinition:
                    dataDict = dataLst._asdict()[Contact.__name__].__dict__  # Getting the dictionary of the list.

                    colname = keys["name"]  # Getting the column name.
                    if colname in dataDict and colname != Contact.code.name:  # Just if the column name is on the dictionary, add it to the dictStore.
                        dicStore[colname] = DBProcess(Client.clients_tbl).parse2publish(dataDict[colname])
            dataCol.append(dicStore)
            # Appending everything to be returned

        return {"status": 200, "value": dataCol, 'type': 'application/json'}


    def getClients(self, inputs):
        main_query = self.session.query(Client). \
            filter(or_(Client.cl_name.ilike("%" + inputs["infoclient"] + "%"),
                       Client.telephone.ilike("%" + inputs["infoclient"] + "%"),
                       Client.rnc.ilike("%" + inputs["infoclient"] + "%"))).\
            filter(Client.status==11)
        self.msg = []
        for piece in main_query:
            del piece.__dict__['_sa_instance_state']
            if piece.__dict__[Client.price.name]!=None:
                piece.__dict__[Client.price.name] = float(piece.__dict__[Client.price.name])
            if piece.__dict__[Client.current_credit.name] != None:
                piece.__dict__[Client.current_credit.name]=float(piece.__dict__[Client.current_credit.name])
            if piece.__dict__[Client.max_credit.name] != None:
                piece.__dict__[Client.max_credit.name]=float(piece.__dict__[Client.max_credit.name])
            client_order =PreOrder.objects(client=piece.__dict__[Client.code.name], status=11).first()
            if client_order!=None:
                piece.__dict__["order"]=client_order.code
            else:
                piece.__dict__["order"] =None

            self.msg.append(piece.__dict__)

        return {"status": 200, "value": self.msg, 'type': 'application/json'}


    def loadFromDGII(self, inputs):
        with open(inputs["path"], "r", encoding="ISO-8859-1") as file:
            rnclst = str(file.read()).split("\n")[2043122:]
            insertsLst=[]
            cont=0
            for piece in rnclst:
                rnc_info = piece.split("|")
                insertsLst.append({Client.cl_name.name:rnc_info[1],
                                          Client.rnc.name:rnc_info[0], Client.status.name:11,
                                   Client.code.name:CodeGen().GenCode({"table": Client.__tablename__,
                                                                       "column": Client.code.name})})
            self.session.bulk_insert_mappings(Client, insertsLst)
            self.session.commit()




if __name__ == '__main__':
    print(Clients().HandleClient({"client":1, "name":"CodeService, SRL",
                                  "con_name":"Diego Hidalgo","telephone":"849-868-9937",
                                  "cellphone":"829-639-9937","email":"hidura@gmail.com",
                                  "rnc":"131353096","address":"Paseo de Los Reyes Catolicos #11, Arroyo Hondo"}))
__author__ = 'hidura'
