from sqlalchemy.sql.expression import select, update, insert
from tools.DataBase.Definition.Base import db
from tools.DataBase.Definition.codelisting import CodeListing

__author__ = 'hidura'




class CodeGen:
    #This class work with the generation of the code
    #On every table.
    conn = db.session

    def getCodeLstingCode(self, code=None):
        if code == None:
            result = self.conn.execute(select([CodeListing]))

            valCurrentCode = self.conn.execute(select([CodeListing]).where(CodeListing.code == len(result.fetchall())+1))

            if valCurrentCode == None:
                return len(valCurrentCode.fetchall())+1
            else:
                _futureCode = self.getCodeLstingCode(len(valCurrentCode.fetchall())+2)
                return _futureCode
        else:

            valCurrentCode = self.conn.execute(select([CodeListing]).where(CodeListing.code == code))

            if len(valCurrentCode.fetchall())==0:
                return code
            else:
                _futureCode = self.getCodeLstingCode(code+1)
                return _futureCode

    def GenCode(self, kwargs):
        connection = db.engine.raw_connection()
        cursor = connection.cursor()

        cursor.callproc('setcode', [kwargs["table"],kwargs["column"] if 'column' in kwargs else 'code',0])
        data = cursor.fetchall()
        cursor.close()
        connection.commit()
        return data[0][0]
        #this method will generate and save a new code,
        #And will find if that code is in use, if not in use will returned.


    def RollBackCode(self, kwargs):


        getCurrCode = select([CodeListing]).where(CodeListing.name_tbl == kwargs["table"])

        codeTbl = 0

        result = self.conn.execute(getCurrCode).fetchone()
        currentCode = 1
        if result != None:
            currentCode = (int(result.curCode)-1)
            self.conn.execute(update(CodeListing).where(CodeListing.code == int(result.code)).values(curCode=currentCode))
        else:
            currentCode=0

        return currentCode
        #this method will generate and save a new code,
        #And will find if that code is in use, if not in use will returned.



if __name__ == '__main__':
    None