from sqlalchemy import Column, BIGINT, Text, MetaData, Table
from tools.DataBase.Definition.Base import db
from sqlalchemy.orm import relationship, backref
from sqlalchemy.sql.schema import ForeignKey

from tools.DataBase.Definition.Item import Item
from tools.DataBase.Definition.Status import Status
from tools.DataBase.Definition.company import company
import sqlalchemy as sa


class Recipe(db.Model):
    metadata = MetaData()

    __tablename__ = "recepie_reg"

    __table_args__ = {"useexisting": True}

    id = Column('id', BIGINT, primary_key=True)
    code = Column("code", BIGINT, nullable=False, default=sa.text("setcode('"+__tablename__+"'::text, 'code'::text,0)"))
    item = Column("item", BIGINT, ForeignKey(Item.code), nullable=True)
    directions = Column("directions", Text, nullable=True)
    notes = Column("notes", Text, nullable=True)
    commerce = Column("company", ForeignKey(company.code), nullable=True)
    status = Column('status', BIGINT, ForeignKey(Status.code), nullable=True, default=12)

    # Relationship
    status_rel_cmp = relationship(Status, backref=backref("Recipe"))
    contact_rel_cmp = relationship(Item, backref=backref("Recipe"))
    company_rel_cmp = relationship(company, backref=backref("Recipe"))

    Recepie_tbl = Table(__tablename__, metadata, id, code, item,
                        directions, notes, status, commerce)

    def __repr__(self):
        return "<Recepie (id='%s', code='%s', item='%s', directions='%s'," \
               "notes='%s', status='%s', commerce='%s')>" % \
               (self.id, self.code, self.item,
                self.directions,self.notes, self.status, self.commerce)

    @staticmethod
    def get_all():
        s = db.session.query(Recipe)

        return s.__dict__

    def exist(self):
        exists = db.session.query(
            db.session.query(Recipe).filter_by(id=self.id).exists()
        ).scalar()

        return exists

    @staticmethod
    def insert(data):
        db.session.add(Recipe(**data))
        db.session.commit()

    @staticmethod
    def bulk_insert(data):
        db.session.bulk_save_objects(data)
        db.session.commit()
if __name__ == '__main__':
    Recipe()

__author__ = 'hidura'
