__maintainer__ = 'Diego Hidalgo'
__email__ = 'diego@sugelico.com'
__date__ = '1/14/2019'

from sqlalchemy import Column, BIGINT, Text, MetaData, Table
from sqlalchemy.dialects.mysql.base import NUMERIC

from tools.DataBase.Connect import conection
from tools.DataBase.Definition.Base import db
import sqlalchemy as sa


class Messages(db.Model):
    metadata = MetaData()
    __tablename__ = "messages_reg"

    __table_args__ = {"useexisting": True}

    id = Column('id', BIGINT, primary_key=True)
    code = Column('code', BIGINT, nullable=False, default=sa.text("setcode('"+__tablename__+"'::text, 'code'::text,0)"))
    sender = Column('sender', BIGINT, nullable=False)
    recipient = Column('recipient', BIGINT, nullable=False)
    sender_name = Column('sender_name', Text, nullable=False)
    recipient_name = Column('recipient_name', Text, nullable=False)
    message = Column('message', Text, nullable=False)
    subject = Column('subject', Text, nullable=False)
    send_date = Column('send_date', NUMERIC, nullable=False)
    read_date = Column('read_date', NUMERIC, nullable=True, default=0)
    status = Column('status', BIGINT, nullable=False, default=9)

    Messages_tbl = Table(__tablename__, metadata, id,code,sender, sender_name, recipient,recipient_name,
                         message,send_date,read_date,status,subject)

    def __repr__(self):
        return "<Messages(id='%s',code='%s', sender='%s',sender_name='%s',recipient='%s',recipient_name='%s'," \
               "message='%s',send_date='%s',read_date='%s',status='%s',subject='%s')>" % \
               (self.id,self.code,self.sender,self.sender_name, self.recipient,self.recipient_name,
                self.message,self.send_date, self.read_date,self.status,self.subject)

    def __Publish__(self):
        data = {}
        for column in self.__table__.columns.keys():
            value = self.__dict__[self.__table__.columns[column].name]
            if self.__table__.columns[column].type == "BIGINT":
                data[self.__table__.columns[column].name] = int(value)
            elif self.__table__.columns[column].type == "Integer":
                data[self.__table__.columns[column].name] = int(value)
            elif self.__table__.columns[column].type == "NUMERIC":
                data[self.__table__.columns[column].name] = float(value)
            elif self.__table__.columns[column].type == "Decimal":
                data[self.__table__.columns[column].name] = float(value)
            elif self.__table__.columns[column].type == "time":
                data[self.__table__.columns[column].name] = str(value.strftime('%H:%M:%S'))
            elif self.__table__.columns[column].type == "datetime":
                data[self.__table__.columns[column].name] = str(value.strftime('%H:%M:%S'))
            else:
                data[self.__table__.columns[column].name] = str(value)
        return data

    @staticmethod
    def get_all():
        s = db.session.query(Messages)

        return s.__dict__

    def exist(self):
        exists = db.session.query(
            db.session.query(Messages).filter_by(code=self.code).exists()
        ).scalar()

        return exists

    @staticmethod
    def insert(data):
        db.session.add(Messages(**data))
        db.session.commit()

    @staticmethod
    def bulk_insert(data):
        db.session.bulk_save_objects(data)
        db.session.commit()