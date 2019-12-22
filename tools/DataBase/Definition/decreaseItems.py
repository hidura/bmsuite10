__maintainer__ = 'Diego Hidalgo'
__email__ = 'dhidalgo@codeservicecorp.com'
__date__ = '6/12/2018'

from sqlalchemy import Column, BIGINT, Text, MetaData, Table
from sqlalchemy.dialects.mysql.base import NUMERIC
from tools.DataBase.Definition.Base import db
import sqlalchemy as sa


class decreaseItems(db.Model):
    metadata = MetaData()

    __tablename__ = "decreaseItems_reg"

    __table_args__ = {"useexisting": True}

    id = Column('id', BIGINT, primary_key=True, autoincrement=True)
    prod_name = Column("prod_name", Text, nullable=False)
    amount_input = Column("amount_input", NUMERIC(20,2), nullable=False)
    product = Column("product", BIGINT, nullable=False)
    recipe = Column("recipe", BIGINT, nullable=False)# Product ordered
    recipe_amount = Column("recipe_amount", BIGINT, nullable=False)# The amount of product ordered
    amount_product = Column("amount_product", NUMERIC(20,2), nullable=False)
    unit = Column("unit", BIGINT, nullable=False)
    ordercode = Column("ordercode", BIGINT, nullable=False)
    unit_name = Column("unit_name", Text, nullable=False)

    decreaseItems_tbl = Table(__tablename__, metadata, id, prod_name, amount_input,
                              product, amount_product,recipe,recipe_amount, unit, unit_name,ordercode)

    def __repr__(self):
        return "<decreaseItems(id='%s', prod_name='%s',amount_input='%s'," \
               "product='%s',amount_product='%s',recipe='%s'," \
               "recipe_amount='%s',unit='%s',unit_name='%s',ordercode='%s')>" % \
               (self.id, self.prod_name, self.amount_input,
                self.product, self.amount_product,self.recipe,
                self.recipe_amount, self.unit, self.unit_name,self.ordercode)

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
        s = db.session.query(decreaseItems)

        return s.__dict__

    def exist(self):
        exists = db.session.query(
            db.session.query(decreaseItems).filter_by(id=self.id).exists()
        ).scalar()

        return exists

    @staticmethod
    def insert(data):
        db.session.add(decreaseItems(**data))
        db.session.commit()

    @staticmethod
    def bulk_insert(data):
        db.session.bulk_save_objects(data)
        db.session.commit()

if __name__ == '__main__':
    decreaseItems()


