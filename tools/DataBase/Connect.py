'''
Created on Jun 23, 2013

@author: hidura
'''


from sqlalchemy import create_engine
from mongoengine import connect
from sqlalchemy.pool import NullPool


class conection:


    def conODM(self, config):
        return connect(db=config["mongo"]["db"], alias='default', username=config["mongo"]["user"],
                       password=config["mongo"]["password"], port=int(config["mongo"]["port"]),
                       host=config["mongo"]["host"])
        
        
if __name__ == '__main__':
    conection().conODM()

