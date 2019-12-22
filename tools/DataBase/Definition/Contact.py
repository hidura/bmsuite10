from sqlalchemy import Column, BIGINT, ForeignKey, Text, MetaData, Table
from sqlalchemy.orm import relationship, backref
from sqlalchemy.sql.sqltypes import VARCHAR

from tools.DataBase.Definition.Base import db
from tools.DataBase.Definition.Status import Status
import sqlalchemy as sa

class Contact(db.Model):
    """This table store the information
    of the contact, these contacts will
    be associated with the user of client
    that information. This is important
    to make the research."""

    __tablename__ ="contact_reg"

    __table_args__ = {"useexisting": True}

    id = Column("id",BIGINT, primary_key=True)
    code = Column("code", BIGINT, unique=True, default=sa.text("setcode('"+__tablename__+"'::text, 'code'::text,0)"))
    status = Column("status", BIGINT, ForeignKey(Status.code), nullable=False, default=11)
    contact_name = Column("contact_name", Text)
    lastname = Column("lastname",Text)
    cellphone = Column("cellphone",VARCHAR(18))
    telephone = Column("telephone",VARCHAR(18))
    _address = Column("_address",Text)
    country = Column("country", BIGINT)
    email = Column("email",Text)
    birthdate = Column("birthdate",BIGINT, default=2415021)
    document_id=Column('document_id', Text)
    doc_type=Column("doc_type", BIGINT)


    metadata = MetaData()

    Contact_tbl = Table(__tablename__, metadata,id,contact_name,lastname,cellphone, code,
                        telephone,_address,email, status,birthdate, document_id, doc_type, country)

    #Relationship
    sta_user_rel = relationship(Status,  backref=backref("Contact"))

    def __repr__(self):
        return "<Contact (id='%s', contact_name='%s', lastname='%s', cellphone='%s', " \
               "telephone='%s', _address='%s', email='%s',code='%s',birthdate='%s', " \
               "document_id='%s',doc_type='%s', country='%s'" \
               ")>"%(self.id, self.contact_name, self.lastname, self.cellphone,
                     self.telephone, self._address, self.email, self.code,
                     self.birthdate, self.document_id, self.doc_type, self.country)


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
        s = db.session.query(Contact)
        return s

    @staticmethod
    def insert(data):
        results = Contact(**data)
        db.session.add(results)
        db.session.commit()
        return results

    @staticmethod
    def bulk_insert(data):
        results = db.session.bulk_save_objects(data)
        db.session.commit()
        return results
if __name__ == '__main__':
    Contact()

__author__ = 'hidura'
