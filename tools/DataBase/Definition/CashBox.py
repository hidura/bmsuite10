
__maintainer__ = 'Diego Hidalgo'
__email__ = 'diego@sugelico.com'
__date__ = '1/23/2019'
from sqlalchemy.orm import relationship, backref

from tools.DataBase.Definition.Status import Status
from tools.DataBase.Definition.branch import Branch


from sqlalchemy import Column, BIGINT, MetaData, Table, Text, ForeignKey
from tools.DataBase.Definition.Base import db
import sqlalchemy as sa

class CashBox(db.Model):
    metadata = MetaData()

    __tablename__ = "cashbox_reg"

    __table_args__ = {"useexisting": True}

    id = Column('id', BIGINT, primary_key=True)
    code = Column("code", BIGINT, nullable=True, default=sa.text("setcode('supplierorder_reg'::text, 'code'::text, (0)::bigint)"))
    _name = Column("_name", Text, nullable=True)
    description = Column("description", Text, nullable=True)
    usercode = Column("usercode", BIGINT, nullable=True)
    warehouse = Column("warehouse", BIGINT, nullable=True)
    branch = Column("branch", BIGINT,ForeignKey(Branch.code), nullable=True)
    status = Column("status", BIGINT,ForeignKey(Status.code), nullable=True)


    status_rel_cmp = relationship(Status, backref=backref("CashBox"))
    branch_rel_cmp = relationship(Branch, backref=backref("CashBox"))


    CashBoxOpen_tbl = Table(__tablename__, metadata, id,code, _name,usercode,description,usercode,
                               warehouse, branch,status)

    def __repr__(self):
        return "<BillProdAmount(id='%s',code='%s',_name='%s',description='%s', usercode='%s'," \
               "warehouse='%s',branch='%s',status='%s')>" % \
               (self.id,self.code, self._name,self.description, self.usercode,
                self.warehouse,self.branch,self.status)

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
        s = db.session.query(CashBox)
        return s.__dict__

    def exist(self):
        exists = db.session.query(
            db.session.query(CashBox).filter_by(id=self.id).exists()
        ).scalar()

        return exists

    @staticmethod
    def insert(data):
        db.session.add(CashBox(**data))
        db.session.commit()

    @staticmethod
    def bulk_insert(data):
        db.session.bulk_save_objects(data)
        db.session.commit()

if __name__ == '__main__':
    CashBox()


