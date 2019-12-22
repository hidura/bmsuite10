__email__ = 'dhidalgo@codeservicecorp.com'
__maintainer__ = 'Diego Hidalgo'
__date__ = '11/3/2018'
from tools.DataBase.Definition.BuyOrderTbl import BuyOrderTbl
from tools.DataBase.Definition.Item import Item
from tools.DataBase.Definition.Supplier import Supplier


from sqlalchemy import Column, BIGINT, Text, MetaData, Table, ForeignKey
from sqlalchemy.dialects.mysql.base import NUMERIC

from tools.DataBase.Definition.Base import db
from sqlalchemy.orm import relationship, backref
from sqlalchemy.sql.schema import ForeignKey
import sqlalchemy as sa


class BuyOrderProds(db.Model):
    metadata = MetaData()

    __tablename__ = "buyorderprods_reg"

    __table_args__ = {"useexisting": True}

    id = Column('id', BIGINT, primary_key=True)
    buyorder = Column("buyorder", BIGINT,ForeignKey(BuyOrderTbl.code), nullable=False)
    product  = Column("product", BIGINT,ForeignKey(Item.code), nullable=False)
    product_name  = Column("product_name", Text,nullable=False)
    amount = Column("amount", NUMERIC(20,2), nullable=False)
    price_uni = Column("price_uni", NUMERIC(20,2),default=0.00, nullable=False)
    tax = Column("tax", NUMERIC(20, 2), default=0.00, nullable=False)
    discount = Column("discount", NUMERIC(20, 2), default=0.00, nullable=False)
    total = Column("total", NUMERIC(20, 2), default=0.00, nullable=False)
    supplier = Column("supplier", BIGINT, ForeignKey(Supplier.code), nullable=True)
    notes = Column("notes", Text, nullable=False, default="")


    BuyOrderProds_tbl = Table(__tablename__, metadata, id,buyorder,product,amount,
                              supplier,notes,product_name, price_uni,tax,discount,total)

    # Relations
    buyorder_rel_typ = relationship(BuyOrderTbl, backref=backref("BuyOrderProds"))
    product_rel_typ = relationship(Item, backref=backref("BuyOrderProds"))

    def __repr__(self):
        return "<BuyOrderProds(id='%s',buyorder='%s',product='%s',amount='%s'," \
               "supplier='%s',notes='%s',product_name='%s',price_uni='%s'," \
               "tax='%s',total='%s',discount='%s')>" % \
               (self.id,self.buyorder,self.product,
                self.amount,self.supplier,self.notes,
                self.product_name,self.price_uni,
                self.tax,self.discount,self.total)


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
        s = db.session.query(BuyOrderProds)

        return s.__dict__

    def exist(self):
        exists = db.session.query(
            db.session.query(BuyOrderProds).filter_by(id=self.id).exists()
        ).scalar()

        return exists

    @staticmethod
    def insert(data):
        db.session.add(BuyOrderProds(**data))
        db.session.commit()

    @staticmethod
    def bulk_insert(data):
        db.session.bulk_save_objects(data)
        db.session.commit()
if __name__ == '__main__':
    BuyOrderProds()


