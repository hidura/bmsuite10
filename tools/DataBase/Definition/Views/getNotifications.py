__maintainer__ = 'Diego Hidalgo'
__email__ = 'dhidalgo@codeservicecorp.com'
__date__ = '1/7/2019'

from sqlalchemy import Column, BIGINT, Text, MetaData, Table
from sqlalchemy.dialects.mysql.base import NUMERIC
from tools.DataBase.Definition.Base import db


class GetNotification(db.Model):
    metadata = MetaData()

    __tablename__ = "getnotifications"

    __table_args__ = {"useexisting": True}

    notification_id = Column('notification_id', BIGINT, primary_key=True)
    notification_content = Column('notification_content', Text )
    status = Column('status', BIGINT)
    recipient = Column('recipient', BIGINT)
    status_name = Column('status_name', Text)


    GetNotification_tbl = Table(__tablename__, metadata,notification_id,notification_content,
                            status,recipient,status_name)



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


if __name__ == '__main__':
    GetNotification()


