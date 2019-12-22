from sqlalchemy import Column, BIGINT, Text, MetaData, Table
from sqlalchemy.orm import relationship, backref
from sqlalchemy.sql.schema import ForeignKey
from tools.DataBase.Definition.Base import db
from tools.DataBase.Definition.Type import Type

import sqlalchemy as sa

class Rules(db.Model):

    '''
    The rules registred on the system.
    '''
    metadata = MetaData(db.engine)

    __tablename__ = "rules_reg"

    __table_args__ = {"useexisting": True}

    id = Column('id', BIGINT, primary_key=True)
    description = Column('description', Text, nullable=False)
    code = Column('code', BIGINT, nullable=False, unique=True, default=sa.text("setcode('"+__tablename__+"'::text, 'code'::text,0)"))
    _name = Column('_name', Text, nullable=False)
    rule_type=Column("rule_type", BIGINT,ForeignKey(Type.code), nullable=True)
    Rules_tbl = Table(__tablename__, metadata, id, description, _name, code, rule_type)
    metadata.create_all()



    def __repr__(self):
        return "<Rules (id='%s', description='%s', _name='%s', code='%s', rule_type='%s')>" % \
               (self.id, self.description, self._name, self.code, self.rule_type)

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

    metadata.create_all(db.engine)
    @staticmethod
    def get_all():
        s = db.session.query(Rules)

        return s.__dict__

    def exist(self):
        exists = db.session.query(
            db.session.query(Rules).filter_by(id=self.id).exists()
        ).scalar()

        return exists

    @staticmethod
    def insert(data):
        rule_info=Rules(**data)
        db.session.add(rule_info)
        db.session.commit()
        return rule_info
    @staticmethod
    def bulk_insert(data):
        db.session.bulk_save_objects(data)
        db.session.commit()
if __name__ == '__main__':
    Rules()


__author__ = 'hidura'
