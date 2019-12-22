from sqlalchemy import Column, BIGINT, Text, MetaData, Table
from sqlalchemy.dialects.mysql.base import NUMERIC
from tools.DataBase.Definition.Base import db
import sqlalchemy as sa

class AccountsTbl(db.Model):
    metadata = MetaData()

    __tablename__ = "accounts_reg"

    __table_args__ = {"useexisting": True}

    id = Column('id', BIGINT, primary_key=True)
    code = Column("code", BIGINT, nullable=False, default=sa.text("setcode('supplierorder_reg'::text, 'code'::text, (0)::bigint)"))
    account_name = Column("account_name", Text, nullable=False)
    current_amount = Column("current_amount", NUMERIC(20, 2),
                            default=0.00, nullable=False)
    classification = Column("classification", Text, nullable=False)
    account_type = Column("account_type", Text, nullable=False)
    position =Column("position", Text)

    status = Column("status", BIGINT, nullable=False, default=11)

    Accounts_tbl = Table(__tablename__, metadata, id, code,
                         account_name, current_amount,
                         classification, account_type,position,status)

    def __repr__(self):
        return "<Accounts (id='%s', code='%s', " \
               "account_name='%s', current_amount='%s'," \
               "classification='%s',account_type='%s'," \
               "position='%s',status='%s')>" % \
               (self.id, self.code,
                self.account_name, self.current_amount,
                self.classification, self.account_type,self.position,self.status)

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
        s = db.session.query(AccountsTbl)

        return s.__dict__

    def exist(self):
        exists = db.session.query(
            db.session.query(AccountsTbl).filter_by(cat_name=self._name).exists()
        ).scalar()

        return exists

    @staticmethod
    def insert(data):
        db.session.add(AccountsTbl(**data))
        db.session.commit()

    @staticmethod
    def bulk_insert(data):
        db.session.bulk_save_objects(data)
        db.session.commit()

__author__ = 'hidura'
