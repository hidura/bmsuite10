__maintainer__ = 'Diego Hidalgo'
__email__ = 'dhidalgo@codeservicecorp.com'
__date__ = '11/5/2018'

from sqlalchemy import Column, BIGINT, Text, MetaData, Table
from sqlalchemy.dialects.mysql.base import NUMERIC
from tools.DataBase.Definition.Base import db


class BuyOrderRep(db.Model):
    metadata = MetaData()

    __tablename__ = "buyorder_rep"

    __table_args__ = {"useexisting": True}

    buyprdordid = Column('buyprdordid', BIGINT, primary_key=True)
    billid = Column('billid', BIGINT)
    billname = Column('billname', Text )
    billcode = Column('billcode', BIGINT)
    billsupplier = Column('billsupplier', BIGINT)
    whname = Column('whname', Text)
    billregistred = Column('billregistred', BIGINT)
    billtime = Column('billtime', Text)
    receive_date = Column('receive_date ', BIGINT)
    billrecivetime = Column('billrecivetime', Text)
    billstatus =Column("billstatus", BIGINT)
    billwarehouse = Column("billwarehouse", BIGINT)
    status_name = Column("status_name", Text)
    sup_name = Column("sup_name", Text)
    product_id = Column("product_id", BIGINT)
    prod_name =Column("prod_name", Text)
    amount = Column("amount", NUMERIC)
    notes = Column("notes", Text)


    BuyOrderRep_tbl = Table(__tablename__, metadata, buyprdordid, billid,billname, billcode,billsupplier,
                            whname,billregistred,billtime,receive_date,billrecivetime,billstatus,
                            billwarehouse,status_name,sup_name,
                            product_id,prod_name,amount,notes)



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
    BuyOrderRep()


