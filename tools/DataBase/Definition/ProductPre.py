__maintainer__ = 'Diego Hidalgo'
__email__ = 'dhidalgo@codeservicecorp.com'
__date__ = '8/3/2018'

from sqlalchemy import Column, BIGINT, Text, MetaData, Table
from sqlalchemy.dialects.mysql.base import NUMERIC
from tools.DataBase.Definition.Base import db
import sqlalchemy as sa

class ProductPre(db.Model):
    metadata = MetaData()

    __tablename__ = "productpre_reg"

    __table_args__ = {"useexisting": True}



    id = Column('id', BIGINT, primary_key=True)
    code=Column("code", BIGINT, nullable=False, default=sa.text("setcode('"+__tablename__+"'::text, 'code'::text,0)"))
    product=Column("products", BIGINT, nullable=False)
    preorder=Column("preorder", BIGINT, nullable=False)
    product_name=Column("product_name", Text, nullable=False)
    amount = Column("amount", NUMERIC(20,2), default=0.00, nullable=False)
    notes = Column("notes", Text, nullable=True, default="")
    companion = Column("companion", Text, nullable=True, default="")
    term =Column("term", Text, nullable=True, default="")
    portion = Column("portion", Text, nullable=True, default="")
    subtotal=Column("subtotal", NUMERIC(20,2), default=0.00, nullable=False)
    tax=Column("tax", NUMERIC(20,2), default=0.00, nullable=False)
    total=Column("total", NUMERIC(20,2), default=0.00, nullable=False)
    discount=Column("discount", NUMERIC(20,2), default=0.00, nullable=False)
    status=Column("status", BIGINT, default=11, nullable=False)
    created_by = Column("created_by", BIGINT, nullable=False)
    cashbox = Column("cashbox", BIGINT, nullable=False, default=1)
    server_code = Column("server_code", BIGINT, nullable=False, default=0, comment="The server code, if is 0 is not syncronized")
    created_date = Column("created_date", NUMERIC, nullable=False)
    client = Column("client", Text, nullable=False, default="GENERICO")
    saveit=Column("saveit", BIGINT, default=0)
    ProductPre_tbl = Table(__tablename__, metadata, id, code,product, preorder,product_name,
                           amount,notes,companion,term,portion,subtotal,tax,total,discount,
                           status,created_by, cashbox,created_date,client,server_code, saveit)


    metadata.create_all(db.engine)
    def __repr__(self):
        return "<ProductPre(id='%s',code='%s',product='%s',preorder='%s',product_name='%s'," \
               "amount='%s',notes='%s',companion='%s',term='%s',portion='%s',subtotal='%s'," \
               "tax='%s',total='%s',discount='%s',status='%s',created_by='%s',cashbox='%s'," \
               "created_date='%s',client='%s',server_code='%s',saveit='%s')>" % \
               (self.id, self.code, self.product,self.preorder, self.product_name,self.amount,
                self.notes,self.companion,self.term, self.portion,self.subtotal,self.tax,self.total,
                self.discount,self.status,self.created_by,self.cashbox,self.created_date,self.client,
                self.server_code,self.saveit)

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
        s = db.session.query(ProductPre)

        return s.__dict__

    def exist(self):
        exists = db.session.query(
            db.session.query(ProductPre).filter_by(id=self.id).exists()
        ).scalar()

        return exists

    @staticmethod
    def insert(data):
        db.session.add(ProductPre(**data))
        db.session.commit()

    @staticmethod
    def bulk_insert(data):
        db.session.bulk_save_objects(data)
        db.session.commit()


if __name__ == '__main__':
    ProductPre()


