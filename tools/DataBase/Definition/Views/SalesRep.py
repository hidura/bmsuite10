__maintainer__ = 'Diego Hidalgo'
__email__ = 'diego@sugelico.com'
__date__ = '1/23/2018'

from sqlalchemy import Column, BIGINT, Text, MetaData, Table, FLOAT
from sqlalchemy.dialects.mysql.base import NUMERIC

from tools.DataBase.Definition.Base import db

class SalesRep(db.Model):
    def __init__(self, name):
        self.name = name

    __tablename__ = "sales_rep"
    metadata = MetaData()



    __table_args__ = {"useexisting": True}
    billid = Column("billid", BIGINT)
    billcode = Column('billcode', BIGINT)
    billncf = Column('billncf', BIGINT)
    payid = Column('payid', BIGINT, primary_key=True)
    billdate = Column('billdate', BIGINT)
    billuser = Column('billuser', BIGINT)
    billtime = Column('billtime', Text)
    billpaytp=Column('billpaytp', Text)

    billstatus = Column('billstatus', Text)
    billordertp = Column('billordertp', Text)
    billpreorder = Column('billpreorder', BIGINT)
    billbilltp = Column('billbilltp', Text)

    billsubtotal = Column('billsubtotal', Text)
    billtax = Column('billtax', Text)
    billdisc = Column('billdisc', Text)

    billtotal = Column('billtotal', Text)
    billcashbox = Column('billcashbox', BIGINT)
    billtype_name = Column('billtype_name', Text)

    ordertype_name = Column('ordertype_name', Text)
    status_name = Column('status_name', Text)
    paytpname = Column('paytpname', Text)

    client_name = Column('client_name', Text)
    client_id = Column('client_id', Text)

    ptptotal = Column('ptptotal', NUMERIC)
    ptpaid = Column('ptpaid', NUMERIC)
    ptpsubtotal = Column('ptpsubtotal', NUMERIC)
    ptpncf = Column('ptpncf', Text)
    ptpayname =Column('ptpayname', Text)
    ptpextra = Column('ptpextra', NUMERIC)
    ptptax= Column('ptptax', NUMERIC)
    ptpdesc = Column('ptpdesc', NUMERIC)
    ptpcashbox= Column('ptpcashbox', Text)
    ptpregistred = Column('ptpregistred', Text)
    ptppaytype_id = Column('ptppaytype_id', Text)
    open_amount = Column('open_amount', FLOAT)
    open_date = Column('open_date', FLOAT)
    close_date = Column('close_date', FLOAT)
    close_amount = Column('close_amount', FLOAT)
    status_cashbox = Column('status_cashbox', BIGINT)
    status_cashbox_name = Column('status_cashbox_name', Text)

    SalesRep_tbl = Table(__tablename__, metadata,billid, billcode, billncf, billdate, billtime, billpaytp, billstatus,
                         billordertp, billbilltp, billsubtotal, billtax, billdisc, billtotal, billcashbox, billtype_name,
                         ordertype_name, status_name, paytpname, client_name, client_id,billuser,ptptotal,ptpsubtotal,
                         ptpncf,ptpextra,ptptax,ptpdesc,ptpcashbox,ptpregistred,ptppaytype_id,ptpayname,
                         ptpaid,payid,open_amount,
                         open_date,close_date,close_amount,status_cashbox,status_cashbox_name)