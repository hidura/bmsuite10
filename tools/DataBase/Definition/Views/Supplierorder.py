__maintainer__ = 'Diego Hidalgo'
__email__ = 'dhidalgo@codeservicecorp.com'
__date__ = '3/3/2019'

from sqlalchemy import Column, BIGINT, MetaData, Table, Text, FLOAT
from tools.DataBase.Definition.Base import db

class Supplierorder(db.Model):
    metadata = MetaData()

    __tablename__ = "supplierorder_vw"

    __table_args__ = {"useexisting": True}

    orderid = Column('orderid', BIGINT)
    ordercode =Column('ordercode', BIGINT)
    commercerid =Column('commercerid', BIGINT)
    status=Column("status",BIGINT)
    sup_user=Column("sup_user",BIGINT)
    email =Column('email', Text)
    cl_name =Column('cl_name', Text)
    cl_logo=Column('cl_logo', Text)
    contact_name =Column('contact_name', Text)
    ordergendate =Column('ordergendate', Text)
    order_receive =Column('order_receive', Text)
    reference =Column('reference', Text)
    _address =Column('_address', Text)
    telephone =Column('telephone', Text)
    key_uuid = Column('key_uuid', Text)
    status_name = Column('status_name', Text)
    sup_prod_id = Column('sup_prod_id', BIGINT, primary_key=True)
    sup_prod_productprecode =Column('sup_prod_productprecode', BIGINT)
    sup_prod_product_name =Column('sup_prod_product_name', Text)
    sup_prod_unit =Column('sup_prod_unit', Text)
    sup_prod_notes=Column('sup_prod_notes', Text)
    sup_prod_amount = Column('sup_prod_amount', FLOAT)
    order_total = Column('order_total', FLOAT)
    discount = Column("discount", FLOAT)
    order_tax = Column('order_tax', FLOAT)
    order_price_uni = Column('order_price_uni', FLOAT)
    total = Column('total', FLOAT)
    subtotal = Column('subtotal', FLOAT)
    tax = Column('tax', FLOAT)


    Supplierorder_tbl = Table(__tablename__, metadata, orderid, ordercode,commercerid,email,
                              ordergendate,contact_name,reference,_address,telephone,key_uuid,
                              status_name,sup_prod_id,sup_prod_productprecode,sup_prod_product_name,
                              sup_prod_unit,sup_prod_notes,status, cl_logo,cl_name,sup_user,order_receive,
                              order_total,order_tax,order_price_uni,total,subtotal,tax,discount)


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


if __name__ == '__main__':
    Supplierorder()


