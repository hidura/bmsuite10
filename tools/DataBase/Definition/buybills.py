from sqlalchemy import Column, BIGINT, Text, MetaData, Table, BOOLEAN
from sqlalchemy.dialects.postgresql.base import NUMERIC
from tools.DataBase.Definition.Base import db
from sqlalchemy.orm import relationship, backref
from sqlalchemy.sql.schema import ForeignKey
from tools.DataBase.Definition.Status import Status
import sqlalchemy as sa


class buybills(db.Model):
    metadata = MetaData()

    __tablename__ = "buybills_reg"

    __table_args__ = {"useexisting": True}

    id = Column('id', BIGINT, primary_key=True)
    code = Column("code", BIGINT, nullable=False, default=sa.text("setcode('supplierorder_reg'::text, 'code'::text, (0)::bigint)"))
    supplier = Column("supplier", BIGINT, nullable=True)
    ncf = Column("ncf", Text)
    generated = Column("generated", BIGINT, nullable=True)
    credit = Column("credit", BOOLEAN, nullable=True, )
    subtotal = Column("subtotal", NUMERIC(20,2), nullable=True)
    total_tax = Column("total_tax", NUMERIC(20,2), nullable=True)
    total = Column("total", NUMERIC(20,2), nullable=True)
    other_costs = Column("other_costs", NUMERIC(20,2), nullable=True, default=0.00)
    pay_type = Column("paytype", BIGINT, nullable=True)
    discount = Column("discount", NUMERIC(20,2), nullable=True, default=0.0)
    payalert = Column("payalert", BIGINT, nullable=True)
    expires = Column("expires", BIGINT, nullable=True)
    status = Column('status', BIGINT, ForeignKey(Status.code), nullable=False, default=12)
    description = Column("description", Text)
    warehouse=Column("warehouse", BIGINT)

    #Relationship
    status_rel_cmp = relationship(Status, backref=backref("buybills"))

    buybills_tbl = Table(__tablename__, metadata, id, code, supplier,
                         ncf, generated, total, total_tax, pay_type,
                         expires, status, other_costs, discount,
                         subtotal, payalert, description, warehouse,credit)

    def __repr__(self):
        return "<buybills (id='%s', code='%s', supplier='%s', " \
               "ncf='%s', generated='%s', total_tax='%s'," \
               "total='%s', pay_type='%s', expires='%s', " \
               "status='%s', other_costs='%s', discount='%s', " \
               "subtotal='%s', payalert='%s', description='%s', warehouse='%s',credit='%s')>" % \
               (self.id, self.code, self.supplier, self.ncf,
                self.generated,self.total_tax, self.total,
                self.pay_type, self.expires, self.status,
                self.other_costs, self.discount, self.subtotal,
                self.payalert, self.description, self.warehouse,self.credit)

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
        s = db.session.query(buybills)

        return s.__dict__

    def exist(self):
        exists = db.session.query(
            db.session.query(buybills).filter_by(code=self.code).exists()
        ).scalar()

        return exists

    @staticmethod
    def insert(data):
        db.session.add(buybills(**data))
        db.session.commit()

    @staticmethod
    def bulk_insert(data):
        db.session.bulk_save_objects(data)
        db.session.commit()
if __name__ == '__main__':
    buybills()

__author__ = 'hidura'
