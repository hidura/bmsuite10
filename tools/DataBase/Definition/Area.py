from sqlalchemy import Column, BIGINT, Text, MetaData, Table
from tools.DataBase.Definition.Base import db
import sqlalchemy as sa


class Area(db.Model):
    metadata = MetaData()

    __tablename__ = "area_reg"

    __table_args__ = {"useexisting": True}

    id = Column('id', BIGINT, primary_key=True, autoincrement=True)
    code = Column("code", BIGINT, nullable=False, unique=True, default=sa.text("setcode('supplierorder_reg'::text, 'code'::text, (0)::bigint)"))
    area_name = Column("area_name", Text, nullable=True)
    status = Column("status", BIGINT, nullable=False, default=12)
    description = Column("description", Text, nullable=True)
    company = Column("company", Text, nullable=True)

    Area_tbl = Table(__tablename__, metadata, id, code, area_name, status, description,company)

    def __repr__(self):
        return "<Area (id='%s', area_name='%s', code='%s'," \
               "status='%s', description='%s',company='%s')>" \
               % (self.id, self.area_name, self.code, self.status, self.description,self.company)

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
        s = db.session.query(Area)

        return s.__dict__

    def exist(self):
        exists = db.session.query(
            db.session.query(Area).filter_by(cat_name=self._name).exists()
        ).scalar()

        return exists

    @staticmethod
    def insert(data):
        db.session.add(Area(**data))
        db.session.commit()

    @staticmethod
    def bulk_insert(data):
        db.session.bulk_save_objects(data)
        db.session.commit()


if __name__ == '__main__':
    Area()

__author__ = 'hidura'
