__maintainer__ = 'Diego Hidalgo'
__email__ = 'dhidalgo@codeservicecorp.com'
__date__ = '6/12/2018'

from sqlalchemy import Column, BIGINT, Text, MetaData, Table
from sqlalchemy.dialects.mysql.base import NUMERIC
from tools.DataBase.Definition.Base import db
import sqlalchemy as sa


class productSale(db.Model):
    metadata = MetaData()

    __tablename__ = "productsale_reg"

    __table_args__ = {"useexisting": True}

    id = Column('id', BIGINT, primary_key=True, autoincrement=True)
    prod_name = Column("prod_name", Text, nullable=False)
    amount = Column("amount", NUMERIC(20,2), nullable=False)
    product = Column("product", BIGINT, nullable=False)
    bill = Column("bill", BIGINT, nullable=False)# Product ordered
    category = Column("category", BIGINT, nullable=False)# The amount of product ordered

    productSale_Tbl = Table(__tablename__, metadata, id, prod_name, amount,
                              product, category, bill)

    def __repr__(self):
        return "<decreaseItems(id='%s', prod_name='%s',amount='%s'," \
               "product='%s',bill='%s',category='%s')>" % \
               (self.id, self.prod_name, self.amount,
                self.product,self.bill,self.category)

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
        s = db.session.query(productSale)

        return s.__dict__

    def exist(self):
        exists = db.session.query(
            db.session.query(productSale).filter_by(id=self.id).exists()
        ).scalar()

        return exists

    @staticmethod
    def insert(data):
        db.session.add(productSale(**data))
        db.session.commit()

    @staticmethod
    def bulk_insert(data):
        db.session.bulk_save_objects(data)
        db.session.commit()

if __name__ == '__main__':
    productSale()


