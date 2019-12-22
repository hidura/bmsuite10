
from sqlalchemy.orm.session import sessionmaker
from sqlalchemy.sql.expression import and_

from tools.DataBase.CodeGenerator import CodeGen
from tools.DataBase.Connect import conection
from tools.DataBase.Definition import db
from tools.DataBase.Definition.Area import Area
from tools.DataBase.Definition.Status import Status
from tools.DataBase.ODM.DataModelODM import UserArea
from tools.DataBase.Process import DBProcess
from tools.main.process.login import login


class TableArea:
    def __init__(self):
        self.status = 200
        self.msg = None
        self.type = "text/plain"

        self.session = db.session

    def create(self, inputs):
        # This method will create an expense.
        self.code = CodeGen().GenCode({"table": Area.__tablename__, "column": Area.code.name})
        # Generating the code.
        self.session.add(Area(code=self.code, status=12))
        # Saving with the name, at least.
        self.session.commit()
        return {"status": 200, "value": {Area.code.name: self.code}, 'type': 'application/json'}

    def Handle(self, inputs):
        # This method will modify an expanse.
        area = int(inputs[Area.code.name])
        storeDict = {}
        #Defining the status
        status = 12
        if "status" in inputs:
            if str(inputs["status"]).lower() =="on":
                status = 11
        inputs["status"] = status

        for column in DBProcess(Area.Area_tbl).getColumnDefinition:
            if column["name"] in inputs:
                storeDict[column["expr"]] = DBProcess(Area.Area_tbl).parse(column,inputs[column["name"]])

        self.session.query(Area).filter_by(code=area).update(storeDict)
        self.session.commit()
        return {"status": 200, "value": {Area.code.name: area}, 'type': 'application/json'}

    def Get(self, inputs):
        # This method gets the data, from the db.
        storeDict = []
        if Area.code.name in inputs:
            storeDict = self.session.query(Area, Status.description). \
                filter(and_(Status.code == Area.status, Area.code
                            == int(inputs[Area.code.name])))
        elif Area.area_name.name in inputs:
            storeDict = self.session.query(Area, Status.description). \
                filter(and_(Status.code == Area.status, Area.area_name.like("%"+inputs[Area.area_name.name]+"%")))
        # The next area is in charge to extract the information,
        # from the store Dict and add it to the dataCol to be returned
        dataCol = []
        for dataLst in storeDict:

            dicStore = {"status_name": dataLst._asdict()[Status.description.name]}

            for key in DBProcess(Area.Area_tbl).getColumnDefinition:
                dataDict = dataLst._asdict()[Area.__name__].__dict__  # Getting the dictionary of the list.
                colname = key["name"]  # Getting the column name.
                if colname in dataDict:  # Just if the column name is on the dictionary, add it to the dictStore.
                    dicStore[colname] = dataDict[colname]
            dicStore["users"] =list(UserArea.objects(area=dicStore[Area.code.name]).values_list('user_code'))

            dataCol.append(dicStore)
            # Appending everything to be returned

        self.session.close()
        return {"status": 200, "value": dataCol, 'type': 'application/json'}



    #Custom methods
    def setUserArea(self, inputs):
        # This method receive the
        # usertype: just the 73 user type will be the one
            # that can be added to a specific area, the 3 ones can access to any area,
            # if the user isn't a 73 will be ignored.
        # the usercode and the area.
        usertype = 0
        usercode=int(inputs["usercode"])
        if "usertype" in inputs:
            usertype = int(inputs["usertype"])
        else:
            usertype = login().getProfile(inputs)["value"]["type"]
        if usertype == 73:
            if UserArea.objects(user_code = usercode, area=int(inputs["area"])).first() == None:
                UserArea(user_code=usercode, area=int(inputs["area"])).save()
        else:
            if usertype in [71,74]:
                areaLst = self.session.query(Area)
            elif usertype in [72]:
                areaLst = self.session.query(Area).filter_by(status = 11)
            for areas_info in areaLst:
                if UserArea.objects(user_code=usercode, area=areas_info.code).first() == None:
                    UserArea(user_code=usercode, area=areas_info.code).save()
        self.msg={"msg":"Salvado"}
        return {"status": 200, "value": self.msg, 'type': 'application/json'}



    def getUserArea(self, inputs):
        usercode=int(inputs["usercode"])
        areaLst = UserArea.objects(user_code=usercode)
        self.msg = []
        for area_info in areaLst:
            data_area = self.Get({Area.code.name:area_info.area})["value"]
            if len(data_area)>0:
                self.msg.append(data_area[0])

        return {"status": 200, "value": self.msg, 'type': 'application/json'}

if __name__ == '__main__':
    # print(TableArea().Handle({"_name": "Terraza","area": 3,
    #                           "description":"En las afueras del comercio."}))
    print(TableArea().setUserArea({"usercode":11, "area":3}))
__author__ = 'hidura'
