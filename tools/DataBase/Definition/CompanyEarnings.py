## This table will store the daily company earnings
## Of every branch inside the company.

__maintainer__ = 'Diego Hidalgo'
__email__ = 'diego@sugelico.com'
__date__ = '1/23/2019'

from sqlalchemy import Column, BIGINT, MetaData, Table
from sqlalchemy.dialects.mysql.base import NUMERIC

from tools.DataBase.Definition.Base import db
import sqlalchemy as sa

class ComapnyEarnings(db.Model):
    metadata = MetaData()

    __tablename__ = "companyearnings_reg"

    __table_args__ = {"useexisting": True}

    id = Column('id', BIGINT, primary_key=True)
    code = Column("code", BIGINT, nullable=True, default=sa.text("setcode('supplierorder_reg'::text, 'code'::text, (0)::bigint)"))
    company = Column("company", BIGINT, nullable=True)
    total_earnings = Column("total_earnings", NUMERIC(20, 2), nullable=True)
    _date = Column("_date", NUMERIC(20, 2), nullable=True)
    company_earnings = Column("company_earnings", NUMERIC(20, 2), nullable=True, default=0.00)
    status = Column("status", BIGINT, nullable=True)

    ComapnyEarnings_tbl = Table(__tablename__, metadata, id, code, company, total_earnings,
    _date, status)

    def __repr__(self):
        return "<ComapnyEarnings(id='%s',code='%s',total_earnings='%s',_date='%s'," \
               "comapany_earnings='%s',status='%s',company='%s')>" % \
               (self.id,self.code,self.total_earnings, self._date,
                self.company_earnings, self.status, self.company)

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
        s = db.session.query(ComapnyEarnings)

        return s.__dict__

    def exist(self):
        exists = db.session.query(
            db.session.query(ComapnyEarnings).filter_by(id=self.id).exists()
        ).scalar()

        return exists

    @staticmethod
    def insert(data):
        db.session.add(ComapnyEarnings(**data))
        db.session.commit()

    @staticmethod
    def bulk_insert(data):
        db.session.bulk_save_objects(data)
        db.session.commit()
if __name__ == '__main__':
    ComapnyEarnings()


