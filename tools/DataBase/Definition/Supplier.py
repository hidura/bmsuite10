from sqlalchemy import Column, BIGINT, Text, MetaData, Table
from tools.DataBase.Definition.Base import db
from sqlalchemy.orm import relationship, backref
from sqlalchemy.sql.schema import ForeignKey

from tools.DataBase.Definition.Contact import Contact
from tools.DataBase.Definition.Status import Status
import sqlalchemy as sa
import sqlalchemy as sa

class Supplier(db.Model):
    metadata = MetaData()

    __tablename__ = "supplier_reg"

    __table_args__ = {"useexisting": True}

    id = Column("id", BIGINT, primary_key=True, autoincrement=True)
    code = Column("code", BIGINT, nullable=False, unique=True, default=sa.text("setcode('supplierorder_reg'::text, 'code'::text, (0)::bigint)"))
    contact = Column('contact', BIGINT, ForeignKey(Contact.code), nullable=True)
    status = Column('status', BIGINT, ForeignKey(Status.code), nullable=False, default=12)
    user_code=Column("user_code", BIGINT, nullable=True)
    sup_name = Column("sup_name", Text, nullable=True)
    telephone = Column("telephone", Text, nullable=True)
    _address = Column("_address", Text, nullable=True)
    rnc = Column("rnc", Text, nullable=True)
    # Relationship
    status_rel_cmp = relationship(Status, backref=backref("Supplier"))
    contact_rel_cmp = relationship(Contact, backref=backref("Supplier"))

    def __repr__(self):
        return "<Supplier(id='%s',code='%s', contact='%s', status='%s', " \
               "sup_name='%s', rnc='%s',user_code='%s',telephone='%s',_address='%s')>" \
               % (self.id, self.code, self.contact, self.status,
                  self.sup_name, self.rnc,self.user_code,self.telephone,self._address)

    supplier_tbl = Table(__tablename__, metadata, id, code, telephone,
                         contact, status, sup_name, rnc, user_code,_address)

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
        s = db.session.query(Supplier)

        return s.__dict__

    def exist(self):
        exists = db.session.query(
            db.session.query(Supplier).filter_by(id=self.id).exists()
        ).scalar()

        return exists

    @staticmethod
    def insert(data):
        db.session.add(Supplier(**data))
        db.session.commit()

    @staticmethod
    def bulk_insert(data):
        db.session.bulk_save_objects(data)
        db.session.commit()

if __name__ == '__main__':
    Supplier()

__author__ = 'hidura'
