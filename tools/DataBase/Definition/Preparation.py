from sqlalchemy import Column, BIGINT, Text, MetaData, Table
from tools.DataBase.Definition.Base import db
from sqlalchemy.orm import relationship, backref
from sqlalchemy.sql.schema import ForeignKey
from tools.DataBase.Definition.Status import Status
import sqlalchemy as sa


class Preparation(db.Model):
    metadata = MetaData()

    __tablename__ = "preparation_reg"

    __table_args__ = {"useexisting": True}

    id = Column('id', BIGINT, primary_key=True)
    code=Column("code", BIGINT, nullable=True, default=sa.text("setcode('"+__tablename__+"'::text, 'code'::text,0)"))
    status = Column("status", BIGINT, nullable=False)
    prepare_by = Column("prepare_by", Text, nullable=True)
    prep_date = Column("prep_date", BIGINT, nullable=True)
    # product = Column("product", BIGINT, nullable=False)
    # amount = Column("amount", BIGINT, nullable=False)
    # services = Column("services", BIGINT, nullable=False)
    description = Column("description", Text, nullable=True)
    created = Column("created", BIGINT, nullable=True)
    created_by=Column("created_by", BIGINT)
    Preparation_tbl = Table(__tablename__, metadata, id, code, status, prepare_by,
                            prep_date, description,created, created_by)

    def __repr__(self):
        return "<Preparation (id='%s',code='%s',status='%s',prepare_by='%s',prep_date='%s', " \
               "description='%s',created='%s',created_by='%s')>" % \
               (self.id, self.code, self.status, self.prepare_by,
                self.services, self.description,self.created,self.created_by)

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
    Preparation()

__author__ = 'hidura'
