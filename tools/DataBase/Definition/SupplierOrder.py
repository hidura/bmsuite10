
from tools.DataBase.Definition.Client import Client

from tools.main import general

__maintainer__ = 'Diego Hidalgo'
__email__ = 'diego@sugelico.com'
__date__ = '2/13/19'

from sqlalchemy import Column, BIGINT, Text, MetaData, Table, FLOAT
from tools.DataBase.Definition.Base import db
from sqlalchemy.orm import relationship, backref
from sqlalchemy.sql.schema import ForeignKey

import sqlalchemy as sa
from tools.DataBase.Definition.Status import Status


class SupplierOrder(db.Model):
    metadata = MetaData()

    __tablename__ = "supplierorder_reg"

    __table_args__ = {"useexisting": True}

    id = Column('id', BIGINT, primary_key=True, autoincrement=True)
    code = Column("code", BIGINT, nullable=True, default=sa.text("setcode('supplierorder_reg'::text, 'code'::text, (0)::bigint)"))
    status = Column("status", BIGINT, ForeignKey(Status.code), nullable=True, default=10)
    _date = Column("_date", FLOAT, nullable=False)
    created_by = Column("created_by", BIGINT, nullable=False)
    key_uuid = Column("key_uuid", Text, nullable=False)
    bill_id_int = Column("bill_id_int", BIGINT)
    supplier_name = Column("supplier_name", Text)
    supplier_id = Column("supplier_id", BIGINT)


    #Relationship
    sta_conbill_rel = relationship(Status,  backref=backref("SupplierOrder"))

    SupplierOrder_tbl = Table(__tablename__, metadata, id, code, supplier_id,
                              supplier_name, created_by,key_uuid,status,_date,bill_id_int)

    def __repr__(self):
        return "<SupplierOrder(id='%s',code='%s', " \
               "status='%s'" \
               "_date='%s', " \
               "supplier_name='%s'," \
               "supplier_id='%s', created_by='%s', " \
               "key_uuid='%s',bill_id_int='%s')>" % \
               (self.id, self.code,
                self.status, self._date,
                self.supplier_name, self.supplier_id,
                self.created_by,self.key_uuid,self.bill_id_int)



    @staticmethod
    def insert(data):
        supplier_order=SupplierOrder(**data)
        db.session.add(supplier_order)
        db.session.commit()
        return supplier_order
    @staticmethod
    def bulk_insert(data):
        db.session.bulk_save_objects(data)
        db.session.commit()

    @staticmethod
    def handle(data,code):

        db.session.query(SupplierOrder).filter_by(key_uuid=code).update(data)
        db.session.commit()


if __name__ == '__main__':
    SupplierOrder()


