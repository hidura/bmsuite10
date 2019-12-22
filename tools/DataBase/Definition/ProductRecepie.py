
__maintainer__ = 'Diego Hidalgo'
__email__ = 'diego@sugelico.com'
__date__ = '9/4/2018'

from tools.DataBase.Definition.Item import Item
from sqlalchemy import Column, BIGINT, Text, MetaData, Table
from sqlalchemy.dialects.mysql.base import NUMERIC
from tools.DataBase.Definition.Base import db
from sqlalchemy.orm import relationship, backref
import sqlalchemy as sa


class ProductRecepie(db.Model):
    metadata = MetaData()

    __tablename__ = "productrecepie_reg"

    __table_args__ = {"useexisting": True}

    id = Column('id', BIGINT, primary_key=True)
    code=Column("code", BIGINT, nullable=False, default=sa.text("setcode('"+__tablename__+"'::text, 'code'::text,0)"))
    product=Column("product", BIGINT,nullable=False)
    item_recipe = Column("item_recipe", BIGINT, nullable=False)
    item_recipe_name=Column("item_recipe_name", Text,nullable=False)
    unit =Column("unit", BIGINT, nullable=False)
    unit_name=Column("unit_name", Text, nullable=False,default="")
    amount=Column("amount", NUMERIC(20,2), nullable=False, default=0.00)
    status=Column("status", BIGINT, nullable=False, default=11)



    product_rec_rel = relationship(Item, backref=backref("product"))
    item_recipe_rec_rel = relationship(Item, backref=backref("item_recipe"))

    ProductRecepie_tbl = Table(__tablename__, metadata, id, code,item_recipe,item_recipe_name,
                               unit_name,unit,amount,status,product)

    def __repr__(self):
        return "<ProductRecepie(id='%s',code='%s',item_recipe='%s',item_recipe_name='%s'," \
               "unit='%s',unit_name='%s',amount='%s',status='%s',product='%s')>" % \
               (self.id,self.code,self.item_recipe,self.item_recipe_name,self.unit,
                self.unit_name,self.amount, self.status,self.product)

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
        s = db.session.query(ProductRecepie)

        return s.__dict__

    def exist(self):
        exists = db.session.query(
            db.session.query(ProductRecepie).filter_by(id=self.id).exists()
        ).scalar()

        return exists

    @staticmethod
    def insert(data):
        db.session.add(ProductRecepie(**data))
        db.session.commit()

    @staticmethod
    def bulk_insert(data):
        db.session.bulk_save_objects(data)
        db.session.commit()
if __name__ == '__main__':
    ProductRecepie()


