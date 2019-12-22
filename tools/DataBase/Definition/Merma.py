from sqlalchemy import Column, BIGINT, Text, MetaData, Table
from tools.DataBase.Definition.Base import db

import sqlalchemy as sa

class Merma(db.Model):
    metadata = MetaData()

    __tablename__ = "Merma_reg"

    __table_args__ = {"useexisting": True}

    id = Column('id', BIGINT, primary_key=True)
    code = Column("code", BIGINT, unique=True, nullable=False, default=sa.text("setcode('"+__tablename__+"'::text, 'code'::text,0)"))
    merma_made = Column("merma_made", Text, nullable=True)
    created_by = Column("created_by", BIGINT, nullable=True)
    bill = Column("bill", BIGINT, nullable=True)
    created = Column("created", BIGINT, nullable=True)
    description = Column("description", Text, nullable=True)
    status = Column("status", BIGINT, nullable=True)
    Merma_tbl = Table(__tablename__, metadata, id, code, merma_made, created_by, created, status,bill)

    def __repr__(self):
        return "<Merma (id='%s', code='%s', merma_made='%s', " \
               "created_by='%s',created='%s', status='%s',bill='%s')>" % \
               (self.id, self.code, self.merma_made, self.created_by,
                self.created, self.status, self.bill)

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
        s = db.session.query(Merma)

        return s.__dict__

    def exist(self):
        exists = db.session.query(
            db.session.query(Merma.filter_by(code=self.code)).exists()
        ).scalar()

        return exists

    @staticmethod
    def insert(data):
        db.session.add(Merma(**data))
        db.session.commit()

    @staticmethod
    def bulk_insert(data):
        db.session.bulk_save_objects(data)
        db.session.commit()

if __name__ == '__main__':
    Merma()

__author__ = 'hidura'
