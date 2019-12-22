from sqlalchemy.orm.session import sessionmaker
from tools.DataBase.Connect import conection
from tools.DataBase.Definition import db


class DBProcess:
    def __init__(self, table):

        self.status = 200
        self.msg = None
        self.type = "text/plain"
        self.table = table
        self.session = db.session

    @property
    def getColumnDefinition(self):
        # Property that extract the definition of the column
        dataCol=[piece for piece in self.session.query(self.table).column_descriptions]
        return dataCol

    def parse(self, column, value):

        if str(column["type"]) == "Integer" or str(column["type"]) == "BIGINT":
            return int(value)
        elif str(column["type"]) == "NUMERIC":
            newVal=float(value)
            return newVal
        else:
            return value

    def parse2publish(self, value):
        if str(type(value).__name__) in ["Integer","BIGINT"]:
            return int(value)
        elif str(type(value).__name__) in ["NUMERIC", "Decimal"]:
            newVal = str(value)
            return newVal
        elif str(type(value).__name__) in ["NUMERIC", "Decimal"]:
            newVal = str(value)
            return newVal
        elif str(type(value).__name__) in ["time", "datetime"]:
            newVal = str(value.strftime('%H:%M:%S'))
            return newVal
        else:
            return value

if __name__ == '__main__':

    #d = DBProcess(Supplier.supplier_tbl).getColumnDefinition
    #print(Item.__name__)
    pass
__author__ = 'hidura'
