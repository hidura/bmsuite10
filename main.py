
class main:
    def callObjects(self, inputs, environ):
        self.result = ""
        inputs["__documentroot__"]=environ["DOCUMENT_ROOT"]
        if "md" in inputs:

            self.result = {"status":200,
                                  "value": self.getPage(inputs["md"], inputs, environ).getResult(),
                                  "type":"text/html"
                                  }
        elif "classname" in inputs and "md" not in inputs:

            codeName = inputs["classname"]
            inputs.pop("classname", None)
            self.result = self.exec_code(codeName, inputs, environ)


    def getResult(self):

        return self.result

    def exec_code(self, classname, method, inputs):

        if classname =="general":
            from tools.main.general import general as classtarget
        elif classname =="Company":
            from tools.main.process.Company import Company as classtarget
        elif classname =="Accounts":
            from tools.main.process.Accounts import Accounts as classtarget
        elif classname == "General":
            from tools.main.process.General import General as classtarget
        elif classname == "login":
            from tools.main.process.login import login as classtarget
        elif classname == "ManContact":
            from tools.main.process.manContact import ManContact as classtarget
        elif classname == "Accounting":
            from tools.main.process.Accounting import Accounting as classtarget
        elif classname == "Bills":
            from tools.main.process.Bills import Bills as classtarget
        elif classname == "Items":
            from tools.main.process.Items import Items as classtarget
        elif classname == "Accounts":
            from tools.main.process.Accounts import Accounts as classtarget
        elif classname == "WareHouse":
            from tools.main.process.Warehouse import warehouse as classtarget
        elif classname == "Bills":
            from tools.main.process.Bills import Bills as classtarget
        elif classname == "Clients":
            from tools.main.process.Clients import Clients as classtarget
        elif classname == "Recepie":
            from tools.main.process.Recepie import Recepie as classtarget
        elif classname == "supplier":
            from tools.main.process.supplier import supplier as classtarget
        elif classname == "Table":
            from tools.main.process.Table import Table as classtarget
        elif classname == "TableArea":
            from tools.main.process.TableArea import TableArea as classtarget
        elif classname == "Level":
            from tools.main.process.Level import LevelProc as classtarget
        elif classname == "Types":
            from tools.main.process.Types import Types as classtarget
        elif classname == "Status":
            from tools.main.process.Status import StatusProc as classtarget
        elif classname == "Categories":
            from tools.main.process.Categories import Categories as classtarget
        elif classname == "Messages":
            from tools.main.process.General import MessagesCls as classtarget
        elif classname == "Notifications":
            from tools.main.process.General import NotificationsCls as classtarget
        elif classname == "Widget":
            from tools.main.process.General import Widgets as classtarget
        elif classname == "BuyOrder":
            from tools.main.process.BuyOrder import BuyOrder as classtarget
        elif classname == "Rules":
            from tools.main.process.RulesProc import RulesProc as classtarget

        try:
            retVal = getattr(classtarget(), method)(inputs)
            return retVal
        except Exception as ex:
            raise Exception(str(ex))