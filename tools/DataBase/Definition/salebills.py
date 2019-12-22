import datetime
from sqlalchemy import Column, BIGINT, MetaData, Table
from sqlalchemy.dialects.postgresql.base import NUMERIC
from sqlalchemy.sql.sqltypes import DateTime

from tools.DataBase.Connect import conection
from tools.DataBase.Definition.Base import db
from sqlalchemy.sql.schema import ForeignKey
from tools.DataBase.Definition.Client import Client
from tools.DataBase.Definition.Type import Type
import sqlalchemy as sa


class salebills(db.Model):
    metadata = MetaData()

    __tablename__ = "salebills_reg"

    __table_args__ = {"useexisting": True}

    id = Column('id', BIGINT, primary_key=True)
    code = Column("code", BIGINT, nullable=False, default=sa.text("setcode('supplierorder_reg'::text, 'code'::text, (0)::bigint)"))
    client = Column("client", BIGINT, ForeignKey(Client.code), nullable=True)
    waiter = Column("waiter", BIGINT, nullable=True)
    order_type = Column("order_type", ForeignKey(Type.code), nullable=True)#Delivery, Take out, consume there
    subtotal = Column("subtotal", NUMERIC(20,2), nullable=True, default=0.00)
    tax = Column("tax", NUMERIC(20,2), nullable=True, default=0.00)
    discount = Column("discount", NUMERIC(20,2), nullable=True, default=0.00)
    total = Column("total", NUMERIC(20,2), nullable=True, default=0.00)
    preorder = Column("preorder", BIGINT, nullable=True)#The code of the pre-order.
    ncf = Column("ncf", BIGINT, nullable=True)
    status = Column("status", BIGINT, nullable=True, default=21)
    _date = Column("_date", BIGINT, nullable=True)
    paytype = Column("paytype", BIGINT, nullable=True, default=111)
    billtype = Column("billtype", BIGINT, nullable=True, default=121)
    _time = Column("_time", DateTime(timezone=True), nullable=True, onupdate=datetime.datetime.now)
    cashbox=Column("cashbox", BIGINT)

    salebills_tbl = Table(__tablename__, metadata, id, code, client,
                          waiter, order_type, subtotal,
                          tax, discount, total, ncf, status, preorder,
                          _date, _time, paytype, billtype,cashbox)

    def __repr__(self):
        return "<salebills (id='%s',code='%s', waiter='%s', " \
               "order_type='%s', subtotal='%s', " \
               "tax='%s', discount='%s', total='%s', " \
               "ncf='%s', status='%s', preorder='%s', " \
               "_date='%s',_time='%s', paytype='%s', billtype='%s', cashbox='%s')>" % \
               (self.id, self.code, self.client,
                self.waiter, self.order_type,
                self.subtotal, self.tax, self.total, self.ncf,
                self.status, self.preorder, self._date, self._time,
                self.paytype, self.billtype, self.cashbox)

    def __Publish__(self):
        data={}
        for column in self.__table__.columns.keys():
            value=self.__dict__[self.__table__.columns[column].name]
            print(value,)
            if self.__table__.columns[column].type =="BIGINT":
                data[self.__table__.columns[column].name]=int(value)
            elif self.__table__.columns[column].type =="Integer":
                data[self.__table__.columns[column].name]=int(value)

            elif self.__table__.columns[column].type=="NUMERIC":
                data[self.__table__.columns[column].name] = float(value)
            elif self.__table__.columns[column].type=="Decimal":
                data[self.__table__.columns[column].name] = float(value)

            elif self.__table__.columns[column].type=="time":
                data[self.__table__.columns[column].name] = str(value.strftime('%H:%M:%S'))
            elif self.__table__.columns[column].type=="datetime":
                data[self.__table__.columns[column].name] = str(value.strftime('%H:%M:%S'))
            else:
                data[self.__table__.columns[column].name] = str(value)
        return data

    @staticmethod
    def get_all():
        s = db.session.query(salebills)

        return s.__dict__

    def exist(self):
        exists = db.session.query(
            db.session.query(salebills).filter_by(id=self.id).exists()
        ).scalar()

        return exists

    @staticmethod
    def insert(data):
        db.session.add(salebills(**data))
        db.session.commit()

    @staticmethod
    def bulk_insert(data):
        db.session.bulk_save_objects(data)
        db.session.commit()


class pending_bills(db.Model):
    metadata = MetaData()

    __tablename__ = "peding_bills"

    __table_args__ = {"useexisting": True}

    bill = Column('bill', BIGINT, primary_key=True)

    salebills_tbl = Table(__tablename__, metadata, bill)

    def __repr__(self):
        return "<salebills (bill='%s')>" % \
               (self.bill)





if __name__ == '__main__':
    salebills()

__author__ = 'hidura'
