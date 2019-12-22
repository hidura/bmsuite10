import hashlib
from mongoengine import Q
import json
from sqlalchemy.sql.expression import and_

from tools.DataBase.CodeGenerator import CodeGen
from tools.DataBase.Definition import db
from tools.DataBase.Definition.Area import Area

from tools.DataBase.Definition.Contact import Contact
from tools.DataBase.Definition.RulesUser import RulesUser
from tools.DataBase.Definition.Status import Status
from tools.DataBase.Definition.Type import Type
from tools.DataBase.Definition.User import User
from tools.DataBase.Definition.cashboxOpen import cashboxOpen
from tools.DataBase.ODM.DataModelODM import SessionUser, Module, waiterKey, PreOrder, \
    PreOrderTable, Group_module, group_module_asc, UserModule, cashbox, cashbox_open, UserCompany, rule_user, \
    ModulesFields
from tools.DataBase.Process import DBProcess
from tools.main import general

from tools.main.process.Accounts import Accounts
from tools.main.process.manContact import ManContact
from os import listdir
from os.path import isfile, join

class login:
    def __init__(self):
        self.status = 200
        self.msg = None
        self.type = "text/plain"

        self.session = db.session

    def UserRegistration(self, inputs):
        """The module, register users that
        going to be added to the system."""

        validation={"status":0}

        if validation["status"] == 0:

            #Crate the function that create the codes of the tables.

            status_code = 12

            userCode =0

            if "contact" not in inputs:
                inputs["code"]=ManContact().create({})["value"]["code"]
                inputs["contact"]= ManContact().Handle(inputs)["value"]["code"]
                inputs.pop("code", None)

            if User.code.name not in inputs:
                userCode = CodeGen().GenCode({"table": User.__tablename__})

                #If the user type is 22, the information just will be save as an user.
                userIns = User(username=inputs[User.username.name],
                               passwd=hashlib.md5(inputs[User.passwd.name].encode()).hexdigest(),
                               status=int(status_code), avatar="unknown.png",
                               usrtype=int(inputs[User.usrtype.name]),
                                           code=userCode, contact=inputs[User.contact.name])
                self.session.add(userIns)

            else:
                userCode = int(inputs[User.code.name])

                if inputs["passwd"]!='':
                    dataInsert={User.username:inputs[User.username.name],
                                User.passwd:hashlib.md5(inputs[User.passwd.name].encode()).hexdigest(),
                      User.status:int(status_code), User.avatar:"unknown.png",
                      User.usrtype:int(inputs[User.usrtype.name]),
                      User.code:userCode, User.contact:inputs[User.contact.name]}
                else:
                    dataInsert={User.username:inputs[User.username],
                      User.status:int(status_code), User.avatar:"unknown.png",
                      User.usrtype:int(inputs[User.usrtype.name]),
                      User.code:userCode, User.contact:inputs[User.contact.name]}
                #If the user type is 22, the information just will be save as an user.
                self.session.query(User).filter_by(code=int(inputs[User.code.name])).update\
                    (dataInsert)

            self.session.commit()
            inputs["log_type"]=1
            if "waiter_code" in inputs:
                #Means that the user will be created a key for the waiter.
                waiterKey.objects(user_code=userCode).update(set__status=12)
                waiterKey(user_code=userCode, status=11, key=inputs["waiter_code"],
                          created_by=self.decLoginKey(inputs["key"]), created_date=general().date2julian()).save()

            
            return {"status":200,  "value":self.LoginSys(inputs)["value"], 'type':'application/json'}

        else:
            
            return {"status":500,  "value":validation['msg'], 'type':'application/json'}

    def confirmUsername(self, inputs):
        # Basically this confirm the existnace of any username registred
        user_info=self.session.query(User).filter_by(username=inputs[User.username.name]).first()
        self.msg = {"response": 0}

        if user_info!=None:
            self.msg["response"]=1
            self.msg[User.username.name]=inputs[User.username.name]
        
        return {"status": 200, "value": self.msg, 'type': 'application/json'}


    def LoginWaiter(self, inputs):
        waiterinfo = waiterKey.objects(key=inputs["waiter_code"], status=11).first()
        if waiterinfo != None:
            ###First Close the session
            self.closeAllSession(waiterinfo.user_code)

            meta = {"db_alias": "default"}
            sessionUserID = CodeGen().GenCode({"table": "SessionUser"})

            UserSess = SessionUser(userCode=waiterinfo.user_code, code=sessionUserID,
                                   login=general().date2julian(), created_by=waiterinfo.user_code,
                                   created_date=general().date2julian())

            UserSess.save()
            sessionID = str(UserSess.id)
            profile = self.getProfile({"key": sessionID})["value"]
            profile["key"] = sessionID
            profile["orders"]=self.getOrdersByUser({"usercode":waiterinfo.user_code})["value"]
            profile["modules"]=[]

            

            return {"status": 200, "value": profile, 'type': 'application/json'}
        else:
            

            return {"status": 200, "value": {"error": 0}, 'type': 'application/json'}

    def getOrdersByUser(self, inputs):
        profile={0: []}
        preorders = list(PreOrder.objects(status=11).values_list('code'))
        for orders in preorders:
            preorder_data = PreOrderTable.objects(preorder=orders).first()
            if preorder_data != None:
                # Attaching the order to the table.
                profile[preorder_data.table_code] = [orders, preorder_data.tbl_name]
            else:
                # When there's no table, all the orders will be attach to the first area.
                profile[0].append([orders])
        
        return {"status": 200, "value": profile, 'type': 'application/json'}



    def checkPassword(self, inputs):
        waiterinfo = waiterKey.objects(key=inputs["waiter_code"], status=11).first()
        if waiterinfo != None:
            ###First Close the session

            meta = {"db_alias": "default"}
            profile = self.getProfile({"usercode": waiterinfo.user_code})["value"]

            
            return {"status": 200, "value": profile, 'type': 'application/json'}
        else:

            
            return {"status": 200, "value": {"error": 0}, 'type': 'application/json'}


    def create(self, inputs):
        # This method will create an expense.
        self.code = CodeGen().GenCode({"table": User.__tablename__, "column": User.code.name})
        # Generating the code.
        self.session.add(User(code=self.code, status=12))
        # Saving
        self.session.commit()
        
        return {"status": 200, "value": {User.code.name: self.code}, 'type': 'application/json'}

    def Handle(self, inputs):
        # This method will modify an expanse.
        item = int(inputs[User.code.name])

        if User.passwd.name in inputs: #Just if the passwd
            inputs[User.passwd.name] = hashlib.md5(inputs[User.passwd.name].
                                                     encode()).hexdigest()


        storeDict = {}
        for column in DBProcess(User.user_tbl).getColumnDefinition:
            if column["name"] in inputs:
                storeDict[column["expr"]] = DBProcess(User.user_tbl).parse(column, inputs[column["name"]])

        self.session.query(User).filter_by(code=item).update(storeDict)

        self.session.commit()
        
        if "waiter_code" in inputs:
            if len(inputs["waiter_code"])>=4:
                # Means that the user will be created a key for the waiter.
                waiterKey.objects(user_code=item).update(set__status=12)
                waiterCode= CodeGen().GenCode({"table": "waiterKey", "column": "code"})
                waiterKey(code=waiterCode, user_code=item, status=11, key=inputs["waiter_code"],
                          created_by=self.decLoginKey(inputs["key"]), created_date=general().date2julian()).save()


        return {"status": 200, "value": {User.code.name: item}, 'type': 'application/json'}

    def Get(self, inputs):
        # This method gets the data, from the db.
        storeDict = []
        main_query = self.session.query(User, Status.description, Type.tpname,
                                        Contact.contact_name,Contact.lastname).\
            filter(and_(Status.code == User.status, Type.code == User.usrtype)).\
            filter(Contact.code==User.contact)
        if User.username.name in inputs:
            main_query = main_query.\
                filter(User.username.like("%" + inputs[User.username.name] + "%"))

        if User.code.name in inputs:
            main_query = main_query.\
                    filter(User.code == int(inputs[User.code.name]))

        if User.status.name in inputs:
            main_query = main_query.\
                filter(Status.code == int(inputs[User.status.name]))

        if User.usrtype.name in inputs:
            main_query = main_query. \
                filter(Type.code == int(inputs[User.usrtype.name]))


        # The next area is in charge to extract the information,
        # from the store Dict and add it to the dataCol to be returned
        storeDict=main_query
        dataCol = []
        for dataLst in storeDict:
            dicStore = {"status_name": dataLst._asdict()[Status.description.name],
                        Type.tpname.name: dataLst._asdict()[Type.tpname.name]}

            for key in DBProcess(User.user_tbl).getColumnDefinition:
                dataDict = dataLst._asdict()[User.__name__].__dict__  # Getting the dictionary of the list.
                colname = key["name"]  # Getting the column name.
                if colname in dataDict and colname != User.passwd.name:  # Just if the column name is on the dictionary, add it to the dictStore.

                    dicStore[colname] = DBProcess(User.user_tbl).parse2publish(dataDict[colname])

            for key in DBProcess(Contact.Contact_tbl).getColumnDefinition:
                dataDict = dataLst._asdict() # Getting the dictionary of the list.
                colname = key["name"]  # Getting the column name.
                if colname in dataDict:  # Just if the column name is on the dictionary, add it to the dictStore.

                    dicStore[colname] = DBProcess(Contact.Contact_tbl).parse2publish(dataDict[colname])

            dataCol.append(dicStore)
            # Appending everything to be returned

        return {"status": 200, "value": dataCol, 'type': 'application/json'}

    def closeAllSession(self, idUser):
        meta = {"db_alias": "default"}
        #This module will close all the sessions if there is one open.
        SessionUser.objects(userCode=idUser).update(set__status=32)

    def getProfile(self, inputs):
        # Method that retrives the profile of a user.

        userData = {}
        meta = {"db_alias": "default"}
        key = ""
        if "key" in inputs:
            userData["id"] = self.decLoginKey(inputs["key"])
        elif "usercode" in inputs:
            userData["id"] = int(inputs["usercode"])

        getUserID = self.session.query(User.code, User.avatar, User.usrtype, Contact.email, Contact.contact_name). \
            filter(User.code == userData["id"]).filter(Contact.code == User.contact). \
            first()

        if getUserID != None:
            userData["type"] = getUserID.usrtype
            userData["cashbox"] = None  # By default is None
            cashbox_info = cashbox.objects(user_owner=getUserID.code).first()
            if cashbox_info != None:
                cashBoxcur = self.session.query(cashboxOpen).filter(cashboxOpen.status==11).first()
                if cashBoxcur != None:
                    userData["cashbox"] = cashBoxcur.code

            userData["code"] = getUserID.code
            userData["avatar"] = getUserID.avatar
            userData["email"] = getUserID.email
            userData["copies"]=0
            userData["companies"] = json.loads(UserCompany.objects(user_code=getUserID.code).to_json())
            userData["areas"] =[]
            for company in userData["companies"]:

                data = self.session.query(Area).filter(Area.company == company["company"])
                for piece in data:
                    del piece.__dict__['_sa_instance_state']
                    userData["areas"].append(piece.__dict__)



            userData["paytypes"] = Accounts().getPayType({})["value"]
            userData["billtypes"] = Accounts().getBillType({})["value"]
            userData["name"] = getUserID.contact_name
            userData["rules"]=json.loads(rule_user.objects(user_code=getUserID.code).to_json())
        else:
            userData["type"] = ""
            userData["avatar"] = ""
            userData["paytypes"] = []
            userData["rules"]=[]
            userData["billtypes"] = []
            userData["email"] = ""
            userData["name"] = ""

        

        return {"status": 200, "value": userData, 'type': 'application/json'}


    def syncUsers(self, inputs):
        '''
        Method that syncronize the users on the
        database.
        :param inputs:
        branch int
        :return:
        list of dictionaries
        '''
        users = self.session.query(User.code, User.avatar, User.usrtype, Contact). \
            filter(User.branch == int(inputs['branch'])).\
            filter(Contact.code == User.contact)
        self.msg=[]
        for piece in users:
            waiter_info=waiterKey.objects(user_code=piece[0]).first()

            user_info={"code":piece[0],"avatar":piece[1],
                             "usertype":piece[2], "contact_info":piece[3].__Publish__(),
                             "rules":[], "waiterkey":waiter_info.key if waiter_info != None else None}
            for rule in self.session.query(RulesUser).filter(RulesUser.user_code==piece[0]):
                user_info['rules'].append(rule.__Publish__())
            self.msg.append(user_info)
        return {"status":200,  "value":self.msg, 'type':'application/json'}


    def LoginSys(self, inputs):
        sessionID = 0
        validation = {"status":0}


        #When all the validations, are passed now the work.
        ###Close the session.



        if validation["status"] > 0:
            return {"status":500,  "value":validation['msg'], 'type':'application/json'}
        userData={}
        #This means that login with the system.
        getUserID = self.session.query(User.code, User.avatar, User.usrtype, Contact.email, Contact.contact_name).\
            filter(User.username == inputs["username"]).filter(
                        User.passwd == hashlib.
                        md5(inputs["passwd"].encode()).hexdigest()).filter(Contact.code == User.contact).\
            first()
        if getUserID ==None:
            return {"status":200,  "value":{"error":0}, 'type':'application/json'}




        ###First Close the session
        self.closeAllSession(getUserID.code)

        meta = {"db_alias": "default"}
        sessionUserID = CodeGen().GenCode({"table": "SessionUser"})

        UserSess = SessionUser(userCode=getUserID.code, code=sessionUserID,
                               login=general().getJulian(), created_by=getUserID.code,
                               created_date=general().getJulian())

        UserSess.save()
        sessionID = str(UserSess.id)
        profile=self.getProfile({"key": sessionID})
        profile["key"] = sessionID

        
        return {"status":200, "value":profile, 'type':'application/json'}


    def LoginRoot(self, inputs):
        #The login to verify if the owner of the account is this person.
        sessionID = 0
        validation = {"status":0}


        #When all the validations, are passed now the work.
        ###Close the session.



        if validation["status"] > 0:
            return {"status":500,  "value":validation['msg'],
                    'type':'application/json'}
        userData={}
        #This means that login with the system.
        getUserID = self.session.query(User.code, User.avatar,
                                       User.usrtype, Contact.email,
                                       Contact.contact_name, User.owner).\
            filter(User.username == inputs["username"]).filter(
                        User.passwd == hashlib.
                        md5(inputs["passwd"].encode()).hexdigest()).\
            filter(Contact.code == User.contact).\
            filter(User.owner == True).\
            first()

        if getUserID ==None:
            return {"status":200,  "value":{"error":0}, 'type':'application/json'}




        ###First Close the session
        self.closeAllSession(getUserID.code)

        meta = {"db_alias": "default"}
        sessionUserID = CodeGen().GenCode({"table": "SessionUser"})

        UserSess = SessionUser(userCode=getUserID.code, code=sessionUserID,
                               login=general().getJulian(), created_by=getUserID.code,
                               created_date=general().getJulian())

        UserSess.save()
        sessionID = str(UserSess.id)
        profile=self.getProfile({"key": sessionID})
        profile["key"] = sessionID

        
        return {"status":200, "value":profile, 'type':'application/json'}

    def decLoginKey(self, key):

        meta = {"db_alias": "default"}

        UserSess = SessionUser.objects(id=key, logout=None).first()

        if UserSess!=None:
            return UserSess.userCode
        else:
            return None

    def getUsersBy(self, inputs):
        meta = {"db_alias": "default"}

        userData = self.session.query(User.code, User.username,
                                      Contact.contact_name, Contact.lastname, Contact.email, User.usrtype). \
            filter(User.contact == Contact.code)
        if "usertype" in inputs:
            userData=userData.filter(User.usrtype==int(inputs["usertype"]))

        elif "user" in inputs:
            userData = userData.filter(User.code==int(inputs["user"]))


        userLst =[]
        for piece in userData:
            lastname=""
            if piece.lastname!=None:
                lastname=piece.lastname
            name=""
            if piece.contact_name!=None:
                name=piece.contact_name
            userLst.append({"name":name+" "+lastname, "code":piece.code, "username":piece.username,
                            "email":piece.email,"type":piece.usrtype})

        
        return {"status":200, "value":userLst, 'type':'application/json'}

    def getuserModule(self, inputs):
        #Get the menu from a profile
        meta = {"db_alias": "default"}
        profile=self.getProfile(inputs)["value"]
        dtype="text/html" # Data Type.
        if "datatype" in inputs:
            dtype = inputs["datatype"]
        self.type = dtype

        menu = None
        for piece in group_module_asc.objects(group=int(inputs["group"])):
            if UserModule.objects(user=profile["code"], module=piece.module).first()!=None:
                item = Module.objects(code=piece.module, status=11).first()
                if item!=None:
                    if dtype == "text/html":
                        if menu==None:
                            menu = ""
                        menu += "<a href='"+str(item.path)+"' class='module_container'>"


                        menu += "<img src='/resources/site/"+str(item.icon)+"'>"
                        menu += "<p>"+item.name+"</p></a>"
                    elif dtype =="application/json":
                        if menu == None:
                            menu = []
                        menu.append({"icon":item.icon, "name":item.name, "path":item.path})
        
        if menu==None:
            menu=""
        return {"status": 200, "value": menu, 'type': self.type}

    def getuserGroupModule(self, inputs):
        #Get the menu from a profile
        meta = {"db_alias": "default"}
        profile = self.getProfile(inputs)["value"]
        dtype="text/html" # Data Type.
        if "datatype" in inputs:
            dtype = inputs["datatype"]
        self.type = dtype

        menu = None

        grLst=[]
        for piece in UserModule.objects(user=profile["code"], status=11):

            group_mdl_asc = group_module_asc.objects(module=piece.module).first()
            if group_mdl_asc !=None:
                if group_mdl_asc.group not in grLst:
                    group_mdl=Group_module.objects(code=group_mdl_asc.group, status=11).first()
                    grLst.append(group_mdl_asc.group)
                    if group_mdl !=None:
                        if dtype == "text/html":
                            if menu==None:
                                menu = ""
                            menu += "<a " \
                                    "href='/?md=modules_list&group="+str(group_mdl.code)+"' class='dropdown-item " \
                                                                                         "'>"+group_mdl.name+"</a>"


                        elif dtype =="application/json":
                            if menu == None:
                                menu = []

                            menu.append({"icon":group_mdl.icon, "name":group_mdl.name, "path":group_mdl.path})

        
        if menu == None:
            menu = ""
        return {"status": 200, "value": menu, 'type': self.type}

    def HandleModule(self, inputs):
        #Create a new menu item
        code=0
        userkey = inputs["__usercode__"]
        meta = {"db_alias": "default"}

        status=11
        if "status" in inputs:
            status=int(inputs["status"])

        if "code" in inputs:
            code = int(inputs["code"])
            moduleInfo = Module.objects(code=code).first()
            if moduleInfo !=None:
                mdl_name=moduleInfo.name
                if "name" in inputs:
                    mdl_name=inputs["name"]

                mdl_path = moduleInfo.path
                if "path" in inputs:
                    mdl_path=inputs["path"]

                mdl_icon = moduleInfo.icon
                if "icon" in inputs:
                    mdl_icon=inputs["icon"]

                Module.objects(code=code).update(set__name=mdl_name, set__path=mdl_path,
                                             set__icon=mdl_icon, set__status=status, set__created_by=userkey,
                                             set__created_date=general().date2julian())
                UserModule.objects(module=code).update(set__status=status)
        else:

            code =CodeGen().GenCode({"table": "module", "column": "code"})

            moduleInfo = Module(code=code, name=inputs["name"], path=inputs["path"],
                                icon=inputs["icon"], created_by=userkey,
                                created_date=general().date2julian()).save()
        fields=json.loads(inputs['fields'])
        for piece in fields:
            ModulesFields(module=code,field_name=piece['field_name'],
                          field_type=piece['field_type']).save()
        group = 0
        if "group" in inputs:
            for group in str(inputs["group"]).split("|"):

                if group_module_asc.objects(module=code, group=group).first()!=None:
                    group_module_asc.objects(module=code, group=group).delete()

                group_module_asc(module=code, group=group).save()

        
        return {"status": 200, "value": {"code":code}, 'type': 'application/json'}


    def HandlegroupMenu(self, inputs):
        #Create a new menu item
        code=0
        userkey = self.decLoginKey(inputs["key"])
        meta = {"db_alias": "default"}
        if "code" in inputs:
            code = int(inputs["code"])
            gr_info=Group_module.objects(code=code).first()
            if gr_info!=None:
                gr_name=gr_info.name
                if "name" in inputs:
                    gr_name=inputs["name"]

                Group_module.objects(code=code).update(set__name=gr_name, set__created_by=userkey,
                                             set__created_date=general().date2julian())
        else:
            code = CodeGen().GenCode({"table": "module", "column": "code"})
            groupInfo = Group_module(code=code, name=inputs["name"], created_by=userkey,
                                             created_date=general().date2julian()).save()

        
        return {"status": 200, "value": {"code": code}, 'type': 'application/json'}

    def getModules(self, inputs):
        #Get the modules, by code or name.
        moduleLst=[]
        modules =[]
        if "name" in inputs:
            modules = Module.objects(name__icontains=str(inputs["name"]).lower())
        if "code" in inputs:
            modules = Module.objects(code=int(inputs["code"]))
        for module in modules:
            group=None
            if group_module_asc.objects(module = module.code).first()!=None:
                group = group_module_asc.objects(module = module.code).first().group

            moduleLst.append({"name" : module.name, "group" : group,
                              "code" : module.code, "path": module.path,
                              "icon" : module.icon})
        if "group" in inputs:
            modules = group_module_asc.objects(group=int(inputs["group"]))

            for moduleGR in modules:
                module = Module.objects(code=moduleGR.module).first()

                if module!=None:
                    moduleLst.append({"name": module.name, "group": int(inputs["group"]),
                                  "code": module.code, "path": module.path,
                                  "icon": module.icon})

        self.session.close()
        
        return {"status":200, "value":moduleLst, "type":"application/json"}

    def getGroupModules(self, inputs):
        #Get the modules, by code or name.
        groupLst=[]
        gmodules =[]
        if "name" in inputs:
            gmodules = Group_module.objects(name__icontains=str(inputs["name"]).lower())
        if "code" in inputs:
            gmodules = Group_module.objects(code=inputs["code"])

        for piece in gmodules:
            data = piece.to_mongo()
            del data['_id']
            groupLst.append(data)

        return {"status":200, "value": groupLst, "type": "application/json"}


    def getGroups(self, inputs):
        #Get the modules, by code or name.
        groupLst=[]
        gmodules =[]
        if "name" in inputs:
            gmodules = Group_module.objects(name__icontains=str(inputs["name"]).lower())
        if "code" in inputs:
            gmodules = Group_module.objects(code=inputs["code"])

        for piece in gmodules:
            data =piece.to_mongo()
            del data['_id']
            groupLst.append(data)

        return {"status":200, "value": groupLst, "type": "application/json"}

    def addUserModule(self, inputs):
        meta = {"db_alias": "default"}
        #Associating module to UserType
        usermodule_asoc=[]
        for piece in inputs["modules"]:

            usermodule_asoc.append(UserModule(user=int(inputs["user"]), module=int(piece),
                                              group_name=inputs["group_name"],
                     created_by=inputs["__usercode__"], group=int(inputs["group"]),
                       module_name=inputs["modules"][str(piece)],
                     created_date=general().date2julian()))
        if len(usermodule_asoc) > 0:
            UserModule.objects.insert(usermodule_asoc)

        
        return {"status": 200, "value": {"response": 0}, 'type': 'application/json'}


    def addWaiter(self, inputs):

        usercode=None #The user that will have the key.
        if "user_code" in inputs:
            usercode = int(inputs["user_code"])

        passwd = None  # The user that will have the key.
        if "passwd" in inputs:
            passwd= inputs["passwd"]
        created_by = self.decLoginKey(inputs["key"])
        code = CodeGen().GenCode({"table": "waiterKey", "column":"code"})

        waiterKey(code=code, user_code=usercode, key=passwd,created_by=created_by,
                  created_date=general().date2julian()).save()

        
        return {"status": 200, "value": {"code": code}, 'type': 'application/json'}


    def addGroupMenu(self, inputs):
        code = CodeGen().GenCode({"table":"Group_module", "column": "code"})
        Group_module(code=code, name=inputs["group_name"],icon="fa "+str(inputs["icon"]).replace(".", ""),
                     created_by=inputs["__usercode__"],
                     created_date=general().date2julian()).save()


        
        return {"status": 200, "value": {"code": code}, 'type': 'application/json'}

    def getIconModule(self, inputs):
        

        onlyfiles = [f for f in listdir(inputs["__documentroot__"] + "/resources/site/images") if isfile(join("/resources/site/images/", f))]
        return {"status": 200, "value": [onlyfiles, inputs["__documentroot__"]], 'type': 'application/json'}



    def addCompanyUser(self, inputs):
        UserCompany.objects(user_code=int(inputs["user"])).delete()
        usercompany = []
        for data_company in json.loads(inputs["companies"]):
            company = json.loads(inputs["companies"])[data_company]

            usercompany.append(UserCompany(
                user_code=int(inputs["user"]), company=company["company_id"],
            name_cmp=company["name_cmp"], telephone_cmp=company["telephone_cmp"],
            address_cmp=company["address_cmp"], rnc_cmp=company["rnc_cmp"],
                otherfields_cmp=company["otherfields_cmp"]))

        if len(usercompany) > 0:
            UserCompany.objects.insert(usercompany)
        

        return {"status": 200, "value": {"code": int(inputs["user"])}, 'type': 'application/json'}

    def getWaiters(self, inputs):
        self.msg=[]
        for piece in self.session.query(User, Contact).\
                filter_by(branch=int(inputs['branch'])).filter(User.contact==Contact.code):
            user_info=piece[0].__Publish__()
            contact_info=piece[1].__Publish__()


            data =json.loads(waiterKey.objects(user_code=user_info['code']).to_json())
            if len(data)>0:
                data[0]['user_name']=user_info['username']
                data[0]['name']=contact_info["contact_name"]+" "+contact_info["lastname"]
                self.msg.append(data)
        return {"status": 200, "value": self.msg, 'type': 'application/json'}
if __name__ == '__main__':
    login().addWaiter({"user_code":15, "passwd":"5653", "key":"57b8939f8f01b97f9e79f9f3"})


    None