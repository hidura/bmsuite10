from sqlalchemy import Column, BIGINT, Text, MetaData, Table
from sqlalchemy.dialects.mysql.base import NUMERIC
from sqlalchemy.dialects.postgresql.base import TIME
from tools.DataBase.Definition.Base import db
import sqlalchemy as sa

class Discount(db.Model):
    metadata = MetaData()

    __tablename__ = "discount_reg"

    __table_args__ = {"useexisting": True}

    id = Column('id', BIGINT, primary_key=True)
    code=Column("code", BIGINT, nullable=False, default=sa.text("setcode('"+__tablename__+"'::text, 'code'::text,0)"))
    product = Column('product', BIGINT, nullable=False)
    discount = Column('discount', NUMERIC(20,2), nullable=False, default=0.00)
    start_hour=Column("start_hour", TIME, nullable=False)
    end_hour=Column("start_hour", TIME, nullable=False)
    status=Column("status", BIGINT, nullable=False)
    days=Column("days", Text, nullable=False)
    Discount_tbl = Table(__tablename__, metadata, id, product, discount, start_hour,
                         end_hour, status, days, code)

    def __repr__(self):
        return "<Discount (id='%s', product='%s', discount='%s', " \
               "start_hour='%s', end_hour='%s', days='%s', code='%s')>" % \
               (self.id, self.product, self.discount,
                self.start_hour, self.end_hour, self.days,self.code)

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
        s = db.session.query(Discount)

        return s.__dict__

    def exist(self):
        exists = db.session.query(
            db.session.query(Discount).filter_by(id=self.id).exists()
        ).scalar()

        return exists

    @staticmethod
    def insert(data):
        db.session.add(Discount(**data))
        db.session.commit()

    @staticmethod
    def bulk_insert(data):
        db.session.bulk_save_objects(data)
        db.session.commit()

if __name__ == '__main__':
    HappyHour()

__author__ = 'hidura'
