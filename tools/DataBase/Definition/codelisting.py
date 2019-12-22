
__author__ = 'Created bydhidalgo.'
__copyright__ = "Copyright 8/3/2015, PlateaMobile."

from sqlalchemy import Column, BIGINT, Text, MetaData, Table
from tools.DataBase.Definition.Base import db

class CodeListing(db.Model):

    __tablename__="codelisting_reg"
    __table_args__ = {"useexisting": True}

    id = Column("id", BIGINT, primary_key=True)
    curCode = Column("curCode", BIGINT, nullable=False)
    name_tbl = Column("name_tbl", Text, nullable=False)
    name_col = Column("name_col", Text, nullable=False)
    description = Column("description", Text, nullable=False)
    headCode = Column("headCode", BIGINT, nullable=False)
    code = Column("code", BIGINT, nullable=True)


    metadata = MetaData()

    codeListin_tbl = Table(__tablename__, metadata, id, curCode,
                           name_col, name_tbl, description,
                           headCode, code)

    def __repr__(self):
        return "<CodeListing(id='%s', curCode='%s', name_table='%s', " \
               "name_column='%s',description='%s', " \
               "headCode='%s' code='%s')>" %(self.id, self.curCode,
                                            self.name_tbl, self.name_col,
                                            self.description, self.headCode,
                                            self.code)


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

if __name__ == '__main__':
    CodeListing()