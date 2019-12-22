__maintainer__ = 'Diego Hidalgo'
__email__ = 'dhidalgo@codeservicecorp.com'
__date__ = '11/3/2018'

from sqlalchemy import Column, BIGINT, Text, MetaData, Table
from sqlalchemy.dialects.mysql.base import NUMERIC
from tools.DataBase.Definition.Base import db
import datetime
from sqlalchemy.sql.sqltypes import DateTime
import sqlalchemy as sa



class BuyOrderTbl(db.Model):
    metadata = MetaData()

    __tablename__ = "buyorder_reg"

    __table_args__ = {"useexisting": True}

    id = Column('id', BIGINT, primary_key=True)
    code = Column('code', BIGINT, nullable=False, unique=True, default=sa.text("setcode('supplierorder_reg'::text, 'code'::text, (0)::bigint)"))
    warehouse = Column('warehouse', BIGINT, nullable=False)
    buy_name = Column('buy_name', Text, nullable=False)
    registred = Column('registred', NUMERIC, nullable=False)
    _time = Column("_time", DateTime(timezone=True), nullable=True, onupdate=datetime.datetime.now)
    receive_date = Column('receive_date', NUMERIC, nullable=False)
    recive_time = Column("recive_time", Text, nullable=True)
    status = Column("status", BIGINT, nullable=True, default=11)

    BuyOrderTbl_tbl = Table(__tablename__, metadata, id, code, buy_name,registred,_time,
                            receive_date,recive_time,warehouse, status)

    def __repr__(self):
        return "<BuyOrderTbl(id='%s',code='%s',buy_name='%s',registred='%s'," \
               "_time='%s',receive_date='%s',recive_time='%s',warehouse='%s', " \
               "status='%s')>" % \
               (self.id, self.code,self.buy_name,self.registred,self._time,
                self.receive_date,self.recive_time,self.warehouse,
                self.status)

    def __Publish__(self):
        data = {}
        for column in self.__table__.columns.keys():
            value = self.__dict__[self.__table__.columns[column].name]
            if self.__table__.columns[column].type == "BIGINT":
                data[self.__table__.columns[column].name] = int(value)
            elif self.__table__.columns[column].type == "Integer":
                data[self.__table__.columns[column].name] = int(value)
            elif self.__table__.columns[column].type == "NUMERIC":
                data[self.__table__.columns[column].name] = float(value)
            elif self.__table__.columns[column].type == "Decimal":
                data[self.__table__.columns[column].name] = float(value)
            elif self.__table__.columns[column].type == "time":
                data[self.__table__.columns[column].name] = str(value.strftime('%H:%M:%S'))
            elif self.__table__.columns[column].type == "datetime":
                data[self.__table__.columns[column].name] = str(value.strftime('%H:%M:%S'))
            else:
                data[self.__table__.columns[column].name] = str(value)
        return data

    @staticmethod
    def get_all():
        s = db.session.query(BuyOrderTbl)

        return s.__dict__

    def exist(self):
        exists = db.session.query(
            db.session.query(BuyOrderTbl).filter_by(id=self.id).exists()
        ).scalar()

        return exists

    @staticmethod
    def insert(data):
        db.session.add(BuyOrderTbl(**data))
        db.session.commit()

    @staticmethod
    def bulk_insert(data):
        db.session.bulk_save_objects(data)
        db.session.commit()
if __name__ == '__main__':
    BuyOrderTbl()


