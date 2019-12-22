__maintainer__ = 'Diego Hidalgo'
__email__ = 'diego@sugelico.com'
__date__ = '1/28/2018'

from sqlalchemy import Column, BIGINT, Text, MetaData, Table
from tools.DataBase.Definition.Base import db


class GetProducts(db.Model):
    def __init__(self, name):
        self.name = name
    metadata = MetaData()

    __tablename__ = "getproducts"

    __table_args__ = {"useexisting": True}

    item_reg_item_id= Column('item_reg_item_id', BIGINT, primary_key=True)
    item_reg_item_name = Column('item_reg_item_name', Text)
    item_reg_code= Column('item_reg_code', BIGINT)
    item_reg_price = Column('item_reg_price', Text)
    item_reg_status = Column('item_reg_status', BIGINT)
    item_reg_category=Column('item_reg_category', BIGINT)
    status_reg_description = Column('status_reg_description', Text)
    type_reg_tpname = Column('type_reg_tpname', Text)
    item_reg_item_type= Column('item_reg_item_type', BIGINT)
    item_reg_subtotal = Column('item_reg_subtotal', Text)
    item_reg_tax = Column('item_reg_tax', Text)
    category_reg_cat_name= Column('category_reg_cat_name', Text)

    category_reg_printer= Column('category_reg_printer', Text)
    category_reg_avatar= Column('category_reg_avatar', Text)
    category_reg_cat_type= Column('category_reg_cat_type', BIGINT)

    category_reg_type_product= Column('category_reg_type_product', BIGINT)
    item_reg_avatar= Column('item_reg_avatar', Text)
    category_reg_tp_avatar= Column('category_reg_tp_avatar', Text)


    GetProducts_tbl = Table(__tablename__, metadata, item_reg_item_id,item_reg_item_name, item_reg_code,item_reg_price,
                            item_reg_status,item_reg_category,status_reg_description,type_reg_tpname,item_reg_item_type,
                            item_reg_subtotal,item_reg_tax,category_reg_cat_name,category_reg_printer,category_reg_avatar,
                            category_reg_cat_type,category_reg_type_product,item_reg_avatar,category_reg_tp_avatar)



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
    None


