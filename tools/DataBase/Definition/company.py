from sqlalchemy import Column, BIGINT, Text, MetaData, Table
from sqlalchemy.orm import relationship, backref
from sqlalchemy.sql.schema import ForeignKey
from tools.DataBase.Definition.Base import db
from tools.DataBase.Definition.Status import Status
from tools.DataBase.Definition.Type import Type
import sqlalchemy as sa


class company(db.Model):
    metadata = MetaData()

    __tablename__ = "company_reg"

    __table_args__ = {"useexisting": True}

    id = Column('id', BIGINT, primary_key=True)
    _name = Column('_name', Text, nullable=True)
    _address = Column('_address', Text, nullable=False)
    telephone = Column('telephone', Text, nullable=True)
    rnc = Column("rnc", Text)
    owner = Column('_owner', Text, nullable=True)
    code = Column('code', BIGINT, nullable=True, unique=True, default=sa.text("setcode('supplierorder_reg'::text, 'code'::text, (0)::bigint)"))
    maincode=Column("maincode", BIGINT)# This is the code that's in the register system on the matrix.
    status = Column('status', BIGINT,ForeignKey(Status.code), default=12, nullable=False)
    cmp_type = Column('cmp_type', BIGINT, ForeignKey(Type.code), default=81, nullable=True)
    image = Column("image", Text)

    # Relations
    status_rel_cmp = relationship(Status, backref=backref("company"))
    type_rel_cmp = relationship(Type, backref=backref("company"))

    def __repr__(self):
        return "<company (id='%s', _name='%s', code='%s', status='%s', " \
               "_address='%s', telephone='%s', owner='%s', type='%s', image='%s',rnc='%s', maincode='%s')>" \
               % (self.id, self._name, self.code, self.status,
                  self._address, self.telephone, self.owner, self.type, self.image, self.rnc, self.maincode)


    company_tbl = Table(__tablename__, metadata, id, _name, code, status, _address, telephone, owner, image, rnc, maincode)


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
        s = db.session.query(company)

        return s.__dict__

    def exist(self):
        exists = db.session.query(
            db.session.query(company).filter_by(id=self.id).exists()
        ).scalar()

        return exists

    @staticmethod
    def insert(data):
        db.session.add(company(**data))
        db.session.commit()

    @staticmethod
    def bulk_insert(data):
        db.session.bulk_save_objects(data)
        db.session.commit()
if __name__ == '__main__':
    company()

__author__ = 'hidura'
