__maintainer__ = 'Diego Hidalgo'
__email__ = 'dhidalgo@codeservicecorp.com'
__date__ = '5/14/2018'

from sqlalchemy import Column, BIGINT, Text, MetaData, Table, NUMERIC
from tools.DataBase.Definition.Base import db

class getaccounts(db.Model):
    metadata = MetaData()

    __tablename__ = "getaccounts"

    __table_args__ = {"useexisting": True}


    level_name=Column("level_name", Text)
    acc_type=Column("acc_type", Text)
    account_name= Column("account_name", Text)
    position_account=Column("position_account", Text)
    cur_balance = Column("cur_balance", NUMERIC)
    code=Column("code", BIGINT, primary_key=True)
    account_type=Column("account_type", BIGINT)
    classification=Column("classification", BIGINT)
    GetProducts_tbl = Table(__tablename__, metadata, level_name,acc_type,account_name,
                            cur_balance,code,position_account,account_type,classification)

    def __Publish__(self):
        data = {}
        for column in self.__table__.columns.keys():
            value = self.__dict__[self.__table__.columns[column].name]
            if self.__table__.columns[column].type == "BIGINT":
                data[self.__table__.columns[column].name] = int(value)
            elif self.__table__.columns[column].type == "Integer":
                data[self.__table__.columns[column].name] = int(value)
            elif self.__table__.columns[column].type == "NUMERIC":
                data[self.__table__.columns[column].name] = float(value)
            elif self.__table__.columns[column].type == "Decimal":
                data[self.__table__.columns[column].name] = float(value)
            elif self.__table__.columns[column].type == "time":
                data[self.__table__.columns[column].name] = str(value.strftime('%H:%M:%S'))
            elif self.__table__.columns[column].type == "datetime":
                data[self.__table__.columns[column].name] = str(value.strftime('%H:%M:%S'))
            else:
                data[self.__table__.columns[column].name] = str(value)
        return data
