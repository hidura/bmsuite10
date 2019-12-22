from tools.main import general

__maintainer__ = 'Diego Hidalgo'
__email__ = 'diego@sugelico.com'
__date__ = '2/13/2019'

from sqlalchemy import Column, BIGINT, Text, MetaData, Table
from sqlalchemy.dialects.mysql.base import NUMERIC
import sqlalchemy as sa
from tools.DataBase.Definition.Base import db


class SupplierOrderProducts(db.Model):
    metadata = MetaData()

    __tablename__ = "supplierorderproducts_reg"

    __table_args__ = {"useexisting": True}

    id = Column('id', BIGINT, primary_key=True, autoincrement=True)
    productprecode = Column("productprecode", BIGINT, nullable=False,
                            default=sa.text("setcode('supplierorderaproducts_reg'::text, 'code'::text, (0)::bigint)"))
    product_name = Column("product_name", Text, nullable=False)
    bill = Column("bill", BIGINT, nullable=False)
    amount = Column("amount", NUMERIC, nullable=False)
    price_uni = Column("price_uni", NUMERIC, nullable=False, default=0.00)
    tax = Column("tax", NUMERIC, nullable=False, default=0.00)
    total = Column("total", NUMERIC, nullable=False, default=0.00)

    unit = Column("unit", Text, nullable=False, default="")
    notes = Column("notes", Text, nullable=False, default="")
    created_date = Column("created_date", NUMERIC, nullable=False, default=general().date2julian())

    SupplierOrderProducts_tbl = Table(__tablename__, metadata, id, productprecode, product_name, bill,
                                     amount, unit, notes, created_date, price_uni,tax,total)

    def __repr__(self):
        return "<SupplierOrderProducts(id='%s',productprecode='%s',product_name='%s'," \
               "bill='%s', amount='%s', notes='%s', unit='%s'," \
               "created_date='%s',price_uni='%s', tax='%s', total='%s')>" % \
               (self.id, self.productprecode, self.product_name, self.bill,
                self.amount, self.notes, self.unit, self.created_date,
                self.price_uni,self.tax, self.total)




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
    def insert(data):
        db.session.add(SupplierOrderProducts(**data))
        db.session.commit()

    @staticmethod
    def bulk_insert(data):
        db.session.bulk_save_objects(data)
        db.session.commit()

    @staticmethod
    def handle(data, code):
        db.session.query(SupplierOrderProducts).\
            filter_by(productprecode=code).update(data)
        db.session.commit()

    @staticmethod
    def delete(code):
        db.session.query(SupplierOrderProducts).filter(SupplierOrderProducts.productprecode==code).delete()
        db.session.commit()


if __name__ == '__main__':
    SupplierOrderProducts()


