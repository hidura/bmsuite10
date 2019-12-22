__maintainer__ = 'Diego Hidalgo'
__email__ = 'dhidalgo@codeservicecorp.com'
__date__ = '5/14/2018'

from sqlalchemy import Column, BIGINT, Text, MetaData, Table
from tools.DataBase.Definition.Base import db

class BuyItemsRep(db.Model):
    metadata = MetaData()

    __tablename__ = "buyitems_rep"

    __table_args__ = {"useexisting": True}

    billid = Column('billid', BIGINT, primary_key=True)
    billcode=Column("billcode", BIGINT)
    billncf=Column("billncf", Text)
    billsupplier=Column("billsupplier",BIGINT)
    whname=Column("whname", Text)
    billdate=Column("billdate", Text)
    billpayalert=Column("billpayalert", Text)
    billexpires=Column("billexpires", Text)
    billtotal=Column("billtotal", Text)
    billstatus=Column("billstatus", Text)
    billsubtotal=Column("billsubtotal", Text)
    billtax=Column("billtax", Text)
    billdisc=Column("billdisc", Text)
    billothercosts=Column("billothercosts", Text)
    billdescription=Column("billdescription", Text)
    status_name=Column("status_name", Text)
    paytpname=Column("paytpname", Text)
    sup_name=Column("sup_name",Text)
    sup_rnc=Column("sup_rnc", Text)
    or_billdate=Column("or_billdate", BIGINT)
    or_billpayalert=Column("or_billpayalert", BIGINT)
    or_billexpires=Column("or_billexpires", BIGINT)


    GetProducts_tbl = Table(__tablename__, metadata, billid,billcode,billncf, billsupplier,whname,billdate,billpayalert,
                            billexpires,billtotal,billstatus,billsubtotal,billtax,billdisc,billothercosts,status_name,
                            paytpname,sup_name,sup_rnc,or_billdate,or_billpayalert, or_billexpires)

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
