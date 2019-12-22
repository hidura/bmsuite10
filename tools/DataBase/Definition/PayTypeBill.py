__maintainer__ = 'Diego Hidalgo'
__email__ = 'diego@sugelico.com'
__date__ = '5/12/2018'

from sqlalchemy import Column, BIGINT, Text, MetaData, Table
from sqlalchemy.dialects.mysql.base import NUMERIC

from tools.DataBase.Definition.Base import db


class PayTypeBill(db.Model):
    metadata = MetaData()

    __tablename__ = "paytypebill_reg"

    __table_args__ = {"useexisting": True}

    id = Column('id', BIGINT, primary_key=True, autoincrement=True)
    paytype_id = Column('paytype_id', BIGINT, nullable=False)
    cashbox = Column('cashbox', BIGINT, nullable=False)
    registred = Column('registred', BIGINT, nullable=False)
    paytype = Column('paytype', Text, nullable=True)
    ncf = Column('ncf', Text, nullable=True)
    client_rnc = Column('client_rnc', Text, nullable=True, default="")
    client = Column("client", Text, nullable=True, default="")
    total = Column('total', NUMERIC(20,2), nullable=False)
    total_paid = Column('total_paid', NUMERIC(20,2), nullable=False)
    subtotal = Column('subtotal', NUMERIC(20,2), nullable=False)
    extra = Column('extra', NUMERIC(20,2), nullable=False)
    tax = Column('tax', NUMERIC(20, 2), nullable=False)
    desc = Column('desc', NUMERIC(20, 2), nullable=False)
    bill = Column('bill', BIGINT, primary_key=True)

    PayTypeBill_tbl = Table(__tablename__, metadata, id, paytype, paytype_id,
                            ncf,client, client_rnc, total,subtotal,
                            extra, tax, desc, bill,cashbox, registred,total_paid)

    def __repr__(self):
        return "<PayTypeBill(id='%s', paytype='%s',paytype_id='%s',ncf='%s',client_rnc='%s'," \
               "client='%s',total='%s',subtotal='%s',extra='%s',tax='%s',desc='%s'," \
               "bill='%s',cashbox='%s', registred='%s', total_paid='%s')>" % \
               (self.id, self.paytype, self.paytype_id, self.ncf, self.client_rnc,self.client,
                self.total, self.subtotal,
                self.extra, self.tax, self.desc, self.bill,self.cashbox,
                self.registred, self.total_paid)

    def __Publish__(self):
        data={}
        for column in self.__table__.columns.keys():
            value=self.__dict__[self.__table__.columns[column].name]
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
        s = db.session.query(PayTypeBill)

        return s.__dict__

    def exist(self):
        exists = db.session.query(
            db.session.query(PayTypeBill).filter_by(bill=self.bill).exists()
        ).scalar()

        return exists

    @staticmethod
    def insert(data):
        db.session.add(PayTypeBill(**data))
        db.session.commit()

    @staticmethod
    def bulk_insert(data):
        db.session.bulk_save_objects(data)
        db.session.commit()
if __name__ == '__main__':
    PayTypeBill()


