#!/usr/bin/python
# -*- coding: iso-8859-15 -*-
from sqlalchemy import Column, BIGINT, String, MetaData, Table
from sqlalchemy.sql.sqltypes import BOOLEAN

from tools.DataBase.Definition.Base import db
import sqlalchemy as sa

class WareHouse(db.Model):
    """This is the base class of the users in the system
    here the system store all the users, without discrimination,
    if is an user client or an user of a commerce, will be determine
    by the column usrtype, that is connected to the type table."""
    __tablename__="warehouse_reg"
    __table_args__ = {"useexisting": True}

    id = Column("id",BIGINT, primary_key=True)
    code = Column("code",BIGINT, nullable=False, default=sa.text("setcode('supplierorder_reg'::text, 'code'::text, (0)::bigint)"))
    warehouse_name = Column("warehouse_name", String, nullable=False, default="")
    billDisc = Column("billDisc", BOOLEAN, nullable=False, default=False)
    mainwarehouse = Column("mainwarehouse", BOOLEAN, nullable=False, default=False)
    company = Column("company",BIGINT,nullable=False,default=0)
    warehouse_charge = Column("warehouse_charge", BIGINT)
    status = Column("status", BIGINT, nullable=False)
    description = Column("description", String, nullable=False, default="")
    _address = Column("_address", String, nullable=False, default="")


    metadata = MetaData()

    WareHouse_tbl = Table(__tablename__, metadata,id, code, warehouse_name, billDisc, warehouse_charge,
                     status,description,mainwarehouse,company,_address)

    def __repr__(self):
        return "<User (id='%s', code='%s', warehouse_name='%s',billDisc='%s'," \
               "warehouse_charge='%s', status='%s', description='%s'," \
               "mainwarehouse='%s',company='%s',_address='%s')>"%\
               (self.id, self.code, self.warehouse_name, self.billDisc,
                self.warehouse_charge, self.status, self.description,
                self.mainwarehouse,self.company, self._address)


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
        s = db.session.query(WareHouse)

        return s.__dict__

    def exist(self):
        exists = db.session.query(
            db.session.query(WareHouse).filter_by(id=self.id).exists()
        ).scalar()

        return exists

    @staticmethod
    def insert(data):
        db.session.add(WareHouse(**data))
        db.session.commit()

    @staticmethod
    def bulk_insert(data):
        db.session.bulk_save_objects(data)
        db.session.commit()

if __name__ == '__main__':
    WareHouse()

__author__ = 'hidura'
