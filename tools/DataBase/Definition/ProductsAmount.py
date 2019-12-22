__maintainer__ = 'Diego Hidalgo'
__email__ = 'dhidalgo@codeservicecorp.com'
__date__ = '4/22/2018'

from sqlalchemy import Column, BIGINT, MetaData, Table
from sqlalchemy.dialects.mysql.base import NUMERIC
from tools.DataBase.Definition.Base import db
import sqlalchemy as sa


class ProductsAmount(db.Model):
    metadata = MetaData()

    __tablename__ = "products_amount_asc"

    __table_args__ = {"useexisting": True}

    id = Column('id', BIGINT, primary_key=True)
    warehouse =Column("warehouse", BIGINT, nullable=True)
    product = Column("product", BIGINT, nullable=True)
    amount = Column("amount", NUMERIC(20,2), nullable=True)

    ProductsAmount_tbl = Table(__tablename__, metadata, id, warehouse, product, amount)

    def __repr__(self):
        return "<ProductsAmount(id='%s', product='%s', amount='%s', warehouse='%s')>" % \
               (self.id, self.product, self.amount, self.warehouse)

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
        s = db.session.query(ProductsAmount)

        return s.__dict__

    def exist(self):
        exists = db.session.query(
            db.session.query(ProductsAmount).filter_by(id=self.id).exists()
        ).scalar()

        return exists

    @staticmethod
    def insert(data):
        db.session.add(ProductsAmount(**data))
        db.session.commit()

    @staticmethod
    def bulk_insert(data):
        db.session.bulk_save_objects(data)
        db.session.commit()

if __name__ == '__main__':
    ProductsAmount()


