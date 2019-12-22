from sqlalchemy import Column, BIGINT, Text, MetaData, Table

from sqlalchemy.dialects.postgresql.base import NUMERIC

from tools.DataBase.Definition.Base import db
from sqlalchemy.orm import relationship, backref
from sqlalchemy.sql.schema import ForeignKey
from tools.DataBase.Definition.Status import Status
import sqlalchemy as sa


class Item(db.Model):
    metadata = MetaData()

    __tablename__ = "item_reg"

    __table_args__ = {"useexisting": True}

    id = Column('id', BIGINT, primary_key=True)
    item_name = Column("item_name", Text, nullable=True)
    description = Column("description", Text)
    avatar = Column("avatar", Text)
    code = Column("code", BIGINT, nullable=False, default=sa.text("setcode('"+__tablename__+"'::text, 'code'::text,0)"))
    supplier = Column("supplier", BIGINT, nullable=False)
    barcode = Column("barcode", Text, nullable=False)
    amount = Column("amount", NUMERIC(20, 2), nullable=True, default=0.00)
    category = Column("category", BIGINT, nullable=True)
    item_type = Column("item_type", BIGINT, nullable=True)
    #initial_cost=Column("initial_cost", NUMERIC(20, 2), nullable=True)  # The total amount(Sum of subtotal+Taxes)
    unit = Column("unit", BIGINT, nullable=True)
    status = Column('status', BIGINT, ForeignKey(Status.code), nullable=True, default=12)
    price = Column("price", NUMERIC(20, 2), nullable=True)  # The total amount(Sum of subtotal+Taxes)
    #price1 = Column("price1", NUMERIC(20, 2), nullable=True)  # The total amount(Sum of subtotal+Taxes)
    #price2 = Column("price2", NUMERIC(20, 2), nullable=True)  # The total amount(Sum of subtotal+Taxes)
    #price3 = Column("price3", NUMERIC(20, 2), nullable=True)  # The total amount(Sum of subtotal+Taxes)
    #price4 = Column("price4", NUMERIC(20, 2), nullable=True)  # The total amount(Sum of subtotal+Taxes)

    subtotal = Column("subtotal", NUMERIC(20, 2), nullable=True)  # The subtotal(price, without taxes)
    tax = Column("tax", NUMERIC(20, 2), nullable=True)  # The taxes

    Item_tbl = Table(__tablename__, metadata, id, item_name, description, code,
                     item_type, status, amount, subtotal, price, tax, category, avatar, unit, supplier
                     ,barcode
                     #,price1,price2,price3,price4,initial_cost
                    )

    # Relationship
    status_rel_cmp = relationship(Status, backref=backref("Item"))

    def __repr__(self):
        return "<Item (id='%s', code='%s', item_name='%s', " \
               "description='%s', item_type='%s', status='%s', amount='%s'," \
               "subtotal='%s', price='%s', tax='%s', category='%s',avatar='%s'," \
               "unit='%s'supplier='%s',barcode='%s')>" % \
               (self.id, self.code, self.item_name, self.description, self.item_type,
                self.status, self.amount, self.subtotal, self.price, self.tax, self.category,
                self.avatar, self.unit, self.supplier,
                self.barcode)

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
        s = db.session.query(Item)

        return s.__dict__

    def exist(self):
        exists = db.session.query(
            db.session.query(Item).filter_by(code=self.code).exists()
        ).scalar()

        return exists

    @staticmethod
    def insert(data):
        db.session.add(Item(**data))
        db.session.commit()

    @staticmethod
    def bulk_insert(data):
        db.session.bulk_save_objects(data)
        db.session.commit()
if __name__ == '__main__':
    Item()

__author__ = 'hidura'
