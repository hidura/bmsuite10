
from tools.DataBase.Definition.Client import Client

from tools.main import general

__maintainer__ = 'Diego Hidalgo'
__email__ = 'diego@sugelico.com'
__date__ = '2/13/19'

from sqlalchemy import Column, BIGINT, Text, MetaData, Table
from sqlalchemy.dialects.mysql.base import NUMERIC
from tools.DataBase.Definition.Base import db
from sqlalchemy.orm import relationship, backref
from sqlalchemy.sql.schema import ForeignKey

import sqlalchemy as sa
from tools.DataBase.Definition.Status import Status



class SupplierBill(db.Model):
    metadata = MetaData()

    __tablename__ = "supplierorder_reg"

    __table_args__ = {"useexisting": True}

    id = Column('id', BIGINT, primary_key=True, autoincrement=True)
    code = Column("code", BIGINT, nullable=True, default=sa.text("setcode('supplierorder_reg'::text, 'code'::text, (0)::bigint)"))
    commerce_client = Column("commerce_client", BIGINT, ForeignKey(Client.code), nullable=True)
    commerce_name = Column("commerce_name", Text, nullable=True)
    status = Column("status", BIGINT, ForeignKey(Status.code), nullable=True, default=10)
    _date = Column("_date", NUMERIC(20,2), nullable=True, default=general().date2julian())
    reception_date = Column("reception_date", NUMERIC(20,2), nullable=True)
    contact_name = Column("contact_name", Text, nullable=False)
    contact_email = Column("contact_email", Text, nullable=False)
    reference = Column("reference", Text, nullable=True)
    created_by = Column("created_by", Text, nullable=False)
    key_uuid = Column("key_uuid", Text, nullable=False)
    _address = Column("_address", Text) # To be delivered
    telephone = Column("telephone", Text) # Telephone of the contact
    discount = Column("discount", NUMERIC, nullable=False, default=0.00)
    supplier_name = Column("supplier_name", Text)

    #Relationship
    sta_conbill_rel = relationship(Status,  backref=backref("SupplierOrder"))
    con_conbill_rel = relationship(Client,  backref=backref("SupplierOrder"))

    SupplierOrder_tbl = Table(__tablename__, metadata, id, code, commerce_client,
                          contact_email, status,
                          _date, contact_name,reference, _address,
                             telephone,supplier_name, created_by,key_uuid,commerce_name)

    def __repr__(self):
        return "<SupplierBill(id='%s',code='%s', " \
               "contact_email='%s', commerce_client='%s',," \
               "status='%s'" \
               "_date='%s', " \
               "reference='%s'," \
               "_address='%s', supplier_name='%s'," \
               "telephone='%s',contact_name='%s', created_by='%s', " \
               "key_uuid='%s',commerce_name='%s')>" % \
               (self.id, self.code,
                self.contact_email, self.commerce_client,
                self.status, self._date,
                self.reference, self._address,
                self.supplier_name, self.telephone,
                self.contact_name, self.created_by,self.key_uuid,self.commerce_name)



    @staticmethod
    def insert(data):
        supplier_order=SupplierBill(**data)
        db.session.add()
        db.session.commit()
        return supplier_order
    @staticmethod
    def bulk_insert(data):
        db.session.bulk_save_objects(data)
        db.session.commit()

    @staticmethod
    def handle(data,code):

        db.session.query(SupplierBill).filter_by(code=code).update(data)
        db.session.commit()


if __name__ == '__main__':
    SupplierBill()


