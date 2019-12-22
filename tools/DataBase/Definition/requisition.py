from sqlalchemy import Column, BIGINT, Text, MetaData, Table
from tools.DataBase.Definition.Base import db
import sqlalchemy as sa


class requisition(db.Model):
    metadata = MetaData()

    __tablename__ = "requisition_reg"

    __table_args__ = {"useexisting": True}

    id = Column('id', BIGINT, primary_key=True)
    code = Column("code", BIGINT, unique=True, nullable=False, default=sa.text("setcode('"+__tablename__+"'::text, 'code'::text,0)"))
    created_by = Column("created_by", BIGINT, nullable=True)
    created = Column("created", BIGINT, nullable=True)
    description = Column("description", Text, nullable=True)
    status = Column("status", BIGINT, nullable=True)
    Requisition_tbl = Table(__tablename__, metadata, id, code, description, created_by, created, status)

    def __repr__(self):
        return "<Requisition (id='%s', code='%s', " \
               "created_by='%s',created='%s', status='%s',descriptio='%s')>" % \
               (self.id, self.code, self.created_by,
                self.created, self.status, self.description)

    @staticmethod
    def get_all():
        s = db.session.query(requisition)

        return s.__dict__

    def exist(self):
        exists = db.session.query(
            db.session.query(requisition).filter_by(id=self.id).exists()
        ).scalar()

        return exists

    @staticmethod
    def insert(data):
        db.session.add(requisition(**data))
        db.session.commit()

    @staticmethod
    def bulk_insert(data):
        db.session.bulk_save_objects(data)
        db.session.commit()
if __name__ == '__main__':
    requisition()

__author__ = 'hidura'
