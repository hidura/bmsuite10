__maintainer__ = 'Diego Hidalgo'
__email__ = 'diego@sugelico.com'
__date__ = '9/4/2018'


from sqlalchemy import Column, BIGINT, Text, MetaData, Table, BOOLEAN
from sqlalchemy.dialects.mysql.base import NUMERIC

from tools.DataBase.Definition.Base import db

class LoteProduct(db.Model):
    metadata = MetaData()

    __tablename__ = "loteproduct_reg"

    __table_args__ = {"useexisting": True}

    id = Column('id', BIGINT, primary_key=True)
    product = Column("product", BIGINT, nullable=True)
    product_name = Column("product_name", Text, nullable=True, default="")
    lote=Column("lote", Text, nullable=False, default="")
    buybill=Column("buybill", BIGINT, nullable=False, default=0)
    salebill=Column("salebill", BIGINT, nullable=False, default=0)
    buyprice=Column("buyprice", NUMERIC(20,2), nullable=False, default=0.00)# Buy price per unit.
    saleprice=Column("saleprice", NUMERIC(20,2), nullable=False, default=0.00)# Sale price per unit.
    used=Column("used", BOOLEAN, nullable=False, default=False)

    LoteProduct_tbl = Table(__tablename__, metadata, id, product, product_name,lote,buybill,salebill,
                            buyprice,saleprice,used)

    def __repr__(self):
        return "<LoteProduct(id='%s',product='%s',product_name='%s',lote='%s',buybill='%s',salebill='%s'," \
               "buyprice='%s',saleprice='%s',used='%s')>" % \
               (self.id, self.product, self.product_name, self.lote, self.buybill, self.salebill, self.buyprice,
                self.saleprice, self.used)

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
        s = db.session.query(LoteProduct)

        return s.__dict__

    def exist(self):
        exists = db.session.query(
            db.session.query(LoteProduct).filter_by(id=self.id).exists()
        ).scalar()

        return exists

    @staticmethod
    def insert(data):
        db.session.add(LoteProduct(**data))
        db.session.commit()

    @staticmethod
    def bulk_insert(data):
        db.session.bulk_save_objects(data)
        db.session.commit()

if __name__ == '__main__':
    LoteProduct()


