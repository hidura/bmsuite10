from sqlalchemy import Column, BIGINT, Text, MetaData, Table
from tools.DataBase.Definition.Base import db
import sqlalchemy as sa


class Level(db.Model):
    """The level of the type,
    means the classification of any
     type in the system."""

    metadata = MetaData()

    __tablename__="level_reg"

    __table_args__ = {"useexisting": True}

    id = Column('id',BIGINT, primary_key=True)
    lvl_name = Column('lvl_name',Text, nullable=False)
    code = Column('code',BIGINT, nullable=False, unique=True, default=sa.text("setcode('"+__tablename__+"'::text, 'code'::text,0)"))

    level_tbl = Table(__tablename__, metadata, id, lvl_name,code)




    def __repr__(self):
        return "<level_reg(id='%s', lvl_name='%s', " \
               "code='%s')>"%(self.id, self.lvl_name,
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

    @staticmethod
    def get_all():
        s = db.session.query(Level)

        return s.__dict__

    def exist(self):
        exists = db.session.query(
            db.session.query(Level).filter_by(id=self.id).exists()
        ).scalar()

        return exists

    @staticmethod
    def insert(data):
        db.session.add(Level(**data))
        db.session.commit()

    @staticmethod
    def bulk_insert(data):
        db.session.bulk_save_objects(data)
        db.session.commit()

if __name__ == '__main__':
    Level()


__author__ = 'hidura'
