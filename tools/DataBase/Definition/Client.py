from sqlalchemy.sql.sqltypes import NUMERIC

from tools.DataBase.Definition.Contact import Contact

__author__ = 'Created by dhidalgo.'
__copyright__ = "Copyright 8/20/2015, CodeService."

from sqlalchemy import Column, BIGINT, ForeignKey, Text, MetaData, Table
from sqlalchemy.orm import relationship, backref
from tools.DataBase.Definition.Status import Status
from sqlalchemy.sql.sqltypes import BOOLEAN
from tools.DataBase.Definition.Base import db
import sqlalchemy as sa

class Client(db.Model):
    __tablename__= "client_reg"

    __table_args__ = {"useexisting": True}

    id = Column("id", BIGINT, primary_key=True, autoincrement=True)
    code = Column("code", BIGINT, nullable=False, unique=True, default=sa.text("setcode('supplierorder_reg'::text, 'code'::text, (0)::bigint)"))
    contact = Column('contact', BIGINT, ForeignKey(Contact.code), nullable=True)
    _address = Column("_address", Text, nullable=True)
    telephone = Column('telephone', Text, nullable=True)
    status = Column('status', BIGINT, ForeignKey(Status.code), nullable=False, default=11)
    price = Column('price',  BIGINT, nullable=True, default=1)
    cl_name = Column("cl_name", Text, nullable=False)
    rnc = Column("rnc", Text, nullable=True)
    ncf_type = Column("ncf_type", Text, nullable=True)
    credit = Column("credit", BOOLEAN, default=False)
    discount = Column("discount", NUMERIC(20,2), default=0.00)
    max_credit = Column("max_credit", NUMERIC(20,2), default=0.00)
    current_credit = Column("current_credit", NUMERIC(20,2), default=0.00)
    #Relationship
    status_rel_cmp = relationship(Status, backref=backref("Client"))

    def __repr__(self):
        return "<Client(id='%s',code='%s', contact='%s', status='%s', " \
               "rnc='%s', cl_name='%s', telephone='%s', _address='%s', " \
               "price='%s',credit='%s',max_credit='%s', current_credit='%s',ncf_type='%s', discount='%s')>"\
               %(self.id, self.code, self.contact,
                 self.status, self.rnc, self.cl_name, self.telephone, self._address,
                 self.price, self.credit,self.max_credit,self.current_credit,self.ncf_type,
                 self.discount)

    metadata = MetaData()

    clients_tbl = Table(__tablename__, metadata, id, code,
                        contact, status, cl_name, rnc, telephone, _address,discount,
                        price, credit, max_credit,current_credit,ncf_type)

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
        s = db.session.query(Client)

        return s.__dict__

    def exist(self):
        exists = db.session.query(
            db.session.query(Client).filter_by(id=self.id).exists()
        ).scalar()

        return exists

    @staticmethod
    def insert(data):
        db.session.add(Client(**data))
        db.session.commit()

    @staticmethod
    def bulk_insert(data):
        db.session.bulk_save_objects(data)
        db.session.commit()
if __name__ == '__main__':
    Client()
