__maintainer__ = 'Diego Hidalgo'
__email__ = 'diego@sugelico.com'
__date__ = '7/2/2018'

from sqlalchemy import Column, BIGINT, Text, MetaData, Table
from sqlalchemy.dialects.mysql.base import NUMERIC
from tools.DataBase.Definition.Base import db

class SalesDebt(db.Model):
    def __init__(self, name):
        self.name = name

    __tablename__ = "sales_debt"
    metadata = MetaData()



    __table_args__ = {"useexisting": True}
    billid = Column("billid", BIGINT)
    billcode = Column('billcode', BIGINT)
    billncf = Column('billncf', BIGINT)
    billdate = Column('billdate', BIGINT)
    billuser = Column('billuser', BIGINT)
    billtime = Column('billtime', Text)
    billpaytp = Column('billpaytp', Text)

    billstatus = Column('billstatus', Text)
    billordertp = Column('billordertp', Text)
    billpreorder = Column('billpreorder', BIGINT,primary_key=True)
    billbilltp = Column('billbilltp', Text)

    billsubtotal = Column('billsubtotal', Text)
    billtax = Column('billtax', Text)
    billdisc = Column('billdisc', Text)

    billtotal = Column('billtotal', Text)
    billcashbox = Column('billcashbox', BIGINT)

    client_id = Column('client_id', Text)
    client_name = Column('client_name', Text)

    ptpaid = Column('ptpaid', NUMERIC)

    SalesRep_tbl = Table(__tablename__, metadata, billid, billcode, billncf,
                         billdate, billtime, billpaytp, billstatus,
                         billordertp, billbilltp, billsubtotal, billtax, billdisc, billtotal,
                         billcashbox, ptpaid,client_name)