from sqlalchemy import Column, BIGINT, Text, MetaData, Table
from sqlalchemy.orm import relationship, backref
from sqlalchemy.sql.schema import ForeignKey
from tools.DataBase.Definition.Area import Area
from tools.DataBase.Definition.Status import Status
from tools.DataBase.Definition.Type import Type
from tools.DataBase.Definition.Base import db
import sqlalchemy as sa


class Tables(db.Model):
    metadata = MetaData()

    __tablename__ = "tables_reg"

    __table_args__ = {"useexisting": True}

    id = Column('id', BIGINT, primary_key=True, autoincrement=True)
    tblname = Column('tblname', Text, nullable=True)
    code = Column('code', BIGINT, nullable=True, unique=True, default=sa.text("setcode('supplierorder_reg'::text, 'code'::text, (0)::bigint)"))
    status = Column('status', BIGINT, ForeignKey(Status.code), nullable=False, default=12)
    area = Column("area", BIGINT, ForeignKey(Area.code), nullable=True)
    table_type = Column("table_type", BIGINT,ForeignKey(Type.code), nullable=True)
    _position = Column("_position", Text, nullable=True)

    Tables_tbl = Table(__tablename__, metadata, id, tblname, code, area, status, table_type, _position)

    # Relations
    table_rel_sta = relationship(Status, backref=backref("Tables"))
    table_rel_are = relationship(Area, backref=backref("Tables"))
    table_rel_typ = relationship(Type, backref=backref("Tables"))

    def __repr__(self):
        return "<Tables (id='%s', tblname='%s', code='%s', " \
               "area='%s', status='%s', type='%s', position='%s')>" \
               % (self.id,self.tblname, self.code,self.area,
                  self.status, self.table_type, self._position)

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
        s = db.session.query(Tables)

        return s.__dict__

    def exist(self):
        exists = db.session.query(
            db.session.query(Tables).filter_by(id=self.id).exists()
        ).scalar()

        return exists

    @staticmethod
    def insert(data):
        db.session.add(Tables(**data))
        db.session.commit()

    @staticmethod
    def bulk_insert(data):
        db.session.bulk_save_objects(data)
        db.session.commit()
if __name__ == '__main__':
    Tables()

__author__ = 'hidura'
