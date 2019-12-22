__maintainer__ = 'Diego Hidalgo'
__email__ = 'diego@sugelico.com'
__date__ = '1/23/2019'

from sqlalchemy import Column, BIGINT, MetaData, Table
from sqlalchemy.dialects.mysql.base import NUMERIC

from tools.DataBase.Definition.Base import db
import sqlalchemy as sa

class cashboxOpen(db.Model):
    metadata = MetaData()

    __tablename__ = "cashboxopen_reg"

    __table_args__ = {"useexisting": True}

    id = Column('id', BIGINT, primary_key=True)
    code = Column("code", BIGINT, nullable=True, default=sa.text("setcode('supplierorder_reg'::text, 'code'::text, (0)::bigint)"))
    cashbox = Column("cashbox", BIGINT, nullable=True)
    open_amount = Column("open_amount", NUMERIC(20, 2), nullable=True)
    open_date = Column("open_date", NUMERIC(20, 2), nullable=True)
    close_date = Column("close_date", NUMERIC(20, 2), nullable=False, default=0.00)
    close_amount = Column("close_amount", NUMERIC(20, 2), nullable=True, default=0.00)
    status = Column("status", BIGINT, nullable=True)

    CashBoxOpen_tbl = Table(__tablename__, metadata, id,code, cashbox,open_amount,open_date,
                               close_amount,close_date,status)

    def __repr__(self):
        return "<CashboxOpen(id='%s', cashbox='%s', " \
               "open_amount='%s', open_date='%s', close_amount='%s', close_date='%s', status='%s',code='%s')>" % \
               (self.id, self.cashbox, self.open_amount,self.open_date,self.close_amount,
                self.close_date, self.status,self.code)

    metadata.create_all(db.engine)


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
        s = db.session.query(cashboxOpen)

        return s.__dict__

    def exist(self):
        exists = db.session.query(
            db.session.query(cashboxOpen).filter_by(id=self.id).exists()
        ).scalar()

        return exists

    @staticmethod
    def insert(data):
        db.session.add(cashboxOpen(**data))
        db.session.commit()

    @staticmethod
    def bulk_insert(data):
        db.session.bulk_save_objects(data)
        db.session.commit()
if __name__ == '__main__':
    cashboxOpen()


