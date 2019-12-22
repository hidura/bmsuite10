__maintainer__ = 'Diego Hidalgo'
__email__ = 'dhidalgo@codeservicecorp.com'
__date__ = '10/13/2018'

from sqlalchemy import Column, BIGINT, Text, MetaData, Table
from sqlalchemy.dialects.mysql.base import NUMERIC
from tools.DataBase.Definition.Base import db


class ItemMins(db.Model):
    metadata = MetaData()

    __tablename__ = "item_min"

    __table_args__ = {"useexisting": True}

    item_id = Column('item_id', BIGINT, primary_key=True)
    item_code=Column("item_code", BIGINT, nullable=False)
    item_name=Column("item_name", Text, nullable=False)
    item_type = Column("item_type", Text, nullable=False)
    wh_name = Column("wh_name", Text, nullable=False)
    amount = Column("amount", NUMERIC, nullable=False)
    unit_name = Column("unit_name", NUMERIC, nullable=False)
    buyamount = Column("buyamount", NUMERIC, nullable=False)
    wh_code = Column("wh_code", BIGINT, nullable=False)
    ItemMins_tbl = Table(__tablename__, metadata, item_id, item_code,item_name,
                         item_type,wh_name,amount,wh_code,buyamount,unit_name)



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


if __name__ == '__main__':
    ItemMins()


