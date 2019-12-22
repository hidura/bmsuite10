import datetime

from sqlalchemy import Column, BIGINT, Text, MetaData, Table
from tools.DataBase.Definition.Base import db
from sqlalchemy.sql.sqltypes import DateTime
import sqlalchemy as sa

class ProductReverse(db.Model):
    metadata = MetaData()
    __tablename__ = "productreverse_reg"

    __table_args__ = {"useexisting": True}

    id = Column('id', BIGINT, primary_key=True)
    code = Column("code", BIGINT, nullable=False, default=sa.text("setcode('"+__tablename__+"'::text, 'code'::text,0)"))
    created_by = Column('created_by', BIGINT, nullable=False)
    created_date = Column('created_date', BIGINT, nullable=False)
    _time = Column("_time", DateTime(timezone=True), nullable=True, onupdate=datetime.datetime.now)
    preorder = Column("preorder", BIGINT, nullable=False)
    product = Column("product", BIGINT, nullable=False)
    reason = Column("reason", Text, nullable=False)
    status = Column("status", BIGINT, nullable=False, default=16)

    ProductReverse_tbl = Table(__tablename__, metadata,
                               id, code, created_by,
                               created_date, _time,
                               preorder, reason, status)

    def __repr__(self):
        return "<ProductReverse (id='%s', code='%s', created_by='%s', " \
               "created_date='%s', _time='%s', preorder='%s', reason='%s', status='%s')>" % \
               (self.id, self.code, self.created_by,
                self.created_date, self._time, self.preorder, self.reason, self.status)

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
        s = db.session.query(ProductReverse)

        return s.__dict__

    def exist(self):
        exists = db.session.query(
            db.session.query(ProductReverse).filter_by(id=self.id).exists()
        ).scalar()

        return exists

    @staticmethod
    def insert(data):
        db.session.add(ProductReverse(**data))
        db.session.commit()

    @staticmethod
    def bulk_insert(data):
        db.session.bulk_save_objects(data)
        db.session.commit()

if __name__ == '__main__':
    ProductReverse()

__author__ = 'hidura'
