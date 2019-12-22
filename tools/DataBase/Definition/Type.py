from sqlalchemy import Column, BIGINT, Text, MetaData, Table
from tools.DataBase.Definition.Base import db
import sqlalchemy as sa


class Type(db.Model):
    metadata = MetaData()

    __tablename__ = "type_reg"

    __table_args__ = {"useexisting": True}

    id = Column('id', BIGINT, primary_key=True, autoincrement=True)
    tpname = Column('tpname', Text, nullable=True)
    code = Column('code', BIGINT, nullable=False, unique=True, default=sa.text("setcode('supplierorder_reg'::text, 'code'::text, (0)::bigint)"))
    level = Column('level', BIGINT, nullable=True)
    Type_tbl = Table(__tablename__, metadata, id, tpname, code, level)

    def __repr__(self):
        return "<Type (id='%s', tpname='%s', code='%s', level='%s')>" % \
               (self.id, self.tpname, self.code, self.level)

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
        s = db.session.query(Type)

        return s.__dict__

    def exist(self):
        exists = db.session.query(
            db.session.query(Type).filter_by(id=self.id).exists()
        ).scalar()

        return exists

    @staticmethod
    def insert(data):
        db.session.add(Type(**data))
        db.session.commit()

    @staticmethod
    def bulk_insert(data):
        db.session.bulk_save_objects(data)
        db.session.commit()
if __name__ == '__main__':
    Type()

__author__ = 'hidura'
