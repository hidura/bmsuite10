from sqlalchemy import Column, BIGINT, Text, MetaData, Table
from tools.DataBase.Definition.Base import db
import sqlalchemy as sa

class NCF(db.Model):
    metadata = MetaData()

    __tablename__ = "ncf_reg"

    __table_args__ = {"useexisting": True}

    id = Column('id', BIGINT, primary_key=True)
    header = Column('header', Text, nullable=False)
    ncf_type = Column('ncf_type', BIGINT, nullable=False)
    cur_number = Column('cur_number', BIGINT, nullable=False)
    ncf_limit = Column('ncf_limit', BIGINT, nullable=False)
    code = Column('code', BIGINT, nullable=False, unique=True, default=sa.text("setcode('"+__tablename__+"'::text, 'code'::text,0)"))

    Status_tbl = Table(__tablename__, metadata, id, header, ncf_limit, code,ncf_type,cur_number)


    def __repr__(self):
        return "<NCF (id='%s', header='%s', ncf_limit='%s', code='%s', ncf_type='%s',cur_number='%s')>" % \
               (self.id, self.header, self.ncf_limit, self.code, self.ncf_type,self.cur_number)

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
        s = db.session.query(NCF)

        return s.__dict__

    def exist(self):
        exists = db.session.query(
            db.session.query(NCF).filter_by(id=self.id).exists()
        ).scalar()

        return exists

    @staticmethod
    def insert(data):
        db.session.add(NCF(**data))
        db.session.commit()

    @staticmethod
    def bulk_insert(data):
        db.session.bulk_save_objects(data)
        db.session.commit()


if __name__ == '__main__':
    NCF()
__author__ = 'hidura'
