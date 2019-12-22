from sqlalchemy import Column, BIGINT, Text, MetaData, Table
from sqlalchemy.orm import relationship, backref
from sqlalchemy.sql.schema import ForeignKey
from tools.DataBase.Definition.Base import db
from tools.DataBase.Definition.Status import Status
from tools.DataBase.Definition.company import company
import sqlalchemy as sa


class Branch(db.Model):
    metadata = MetaData()

    __tablename__ = "branch_reg"

    __table_args__ = {"useexisting": True}

    id = Column('id', BIGINT, primary_key=True)
    _name = Column('_name', Text, nullable=True)
    _address = Column('_address', Text, nullable=False)
    telephone = Column('telephone', Text, nullable=True)
    code = Column('code', BIGINT, nullable=True, unique=True, default=sa.text("setcode('supplierorder_reg'::text, 'code'::text, (0)::bigint)"))
    status = Column('status', BIGINT,ForeignKey(Status.code), default=11, nullable=False)
    company = Column('company', BIGINT, ForeignKey(company.code), nullable=True)
    image = Column("image", Text)
    altpath = Column("altpath", Text)



    def __repr__(self):
        return "<Branch (id='%s', _name='%s', code='%s', status='%s', " \
               "_address='%s', telephone='%s', type='%s', image='%s',company='%s',altpath='%s')>" \
               % (self.id, self._name, self.code, self.status,
                  self._address, self.telephone, self.type, self.image,self.company,self.altpath)


    branch_tbl = Table(__tablename__, metadata, id, _name, code, status,
                       _address, telephone, image,company, altpath)



    metadata.create_all(db.engine)


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
        s = db.session.query(Branch)

        return s.__dict__

    def exist(self):
        exists = db.session.query(
            db.session.query(Branch).filter_by(_name=self._name).exists()
        ).scalar()

        return exists

    @staticmethod
    def insert(data):
        branch_data=Branch(**data)
        db.session.add(branch_data)
        db.session.commit()
        return branch_data

    @staticmethod
    def bulk_insert(data):
        db.session.bulk_save_objects(data)
        db.session.commit()

if __name__ == '__main__':
    Branch()

__author__ = 'hidura'
