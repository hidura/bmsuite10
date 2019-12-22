import json

from tools.DataBase.Definition.Rules import Rules
from tools.DataBase.Definition.RulesBranch import RulesBranch
from tools.DataBase.Definition.RulesCompany import RulesCompany
from tools.DataBase.Definition.RulesUser import RulesUser

__author__ = 'Created by: dhidalgo.'
__copyright__ = "Copyright 8/3/2015,"
from tools.DataBase.Definition import db

import os
from tools.DataBase.Definition.branch import Branch
from sqlalchemy.sql.expression import select, and_
from tools.DataBase.CodeGenerator import CodeGen
from tools.DataBase.Definition.Status import Status
from tools.DataBase.Definition.Type import Type
from tools.DataBase.Definition.company import company
from tools.DataBase.Process import DBProcess



class RulesProc:
    def __init__(self):
        self.status = 200
        self.msg = None
        self.type = "text/plain"

        self.session = db.session
        self.engine = db.engine



    def create(self, inputs):
        storeDict = {}
        for column in DBProcess(Rules.Rules_tbl).getColumnDefinition:
            if column["name"] in inputs:
                storeDict[column["name"]] = DBProcess(Rules.Rules_tbl).parse(column, inputs[column["name"]])
        rule_info = Rules.insert(storeDict)

        return {"status": 200, "value": {"code": rule_info.code}, "type": "application/json"}

    def Handle(self,inputs):
        storeDict = {}
        for column in DBProcess(Rules.Rules_tbl).getColumnDefinition:
            if column["name"] in inputs:
                storeDict[column["name"]] = DBProcess(Rules.Rules_tbl).parse(column, inputs[column["name"]])

        self.session.query(Rules).filter_by(code=int(inputs['code'])).update(storeDict)

        self.session.commit()
        return {"status": 200, "value": {"code": inputs['code']}, "type": "application/json"}

    def Get(self, inputs):
        self.msg = []

        data = self.session.query(Rules)
        if Rules._name.name in inputs:
            data = data.filter(Rules._name.ilike('%' + inputs['_name'] + '%'))

        if Rules.description.name in inputs:
            data = data.filter(Rules.description.ilike('%' + inputs['description'] + '%'))

        for piece in data:
            self.msg.append(piece.__Publish__())
        return {"status": 200, "value": self.msg, "type": "application/json"}


    def addRule2(self, inputs):
        '''
        Add rules to user, companies or branches
        :param inputs:
            List of rules
            User Bigint
            Or a company bigint.
            Or a branch bigint.
        :return:
            List with the result string.
        '''
        connection = self.engine.raw_connection()
        cursor = connection.cursor()

        cursor.callproc('addruleto', [json.dumps(inputs)])
        data = cursor.fetchall()
        cursor.close()
        connection.commit()
        return {"status": 200, "value": data[0], "type": "application/json"}

    def delRule2(self, inputs):
        '''
        Delete rules to user, companies or branches
        :param inputs:
            List of rules
            User Bigint
            Or a company bigint.
            Or a branch bigint.
        :return:
            List with the result string.
        '''
        connection = self.engine.raw_connection()
        cursor = connection.cursor()

        cursor.callproc('delruleto', [json.dumps(inputs)])
        data = cursor.fetchall()
        cursor.close()
        connection.commit()
        return {"status": 200, "value": data[0], "type": "application/json"}

    def getRuleBy(self, inputs):
        self.msg = []


        #If the company is present on the inputs then take the company.
        if "company" in inputs:
            data = self.session.query(RulesCompany).filter(RulesCompany.company_code==int(inputs['company']))
            if RulesCompany._name.name in inputs:
                data = data.filter(RulesCompany._name.ilike('%' + inputs['_name'] + '%'))

            if RulesCompany.description.name in inputs:
                data = data.filter(RulesCompany.description.ilike('%' + inputs['description'] + '%'))
            for piece in data:
                self.msg.append(piece.__Publish__())

        #If the branch is present on the inputs then take the branch.
        if "branch" in inputs:
            data = self.session.query(RulesBranch).filter(RulesBranch.branch_code==int(inputs['branch']))
            if RulesBranch._name.name in inputs:
                data = data.filter(RulesBranch._name.ilike('%' + inputs['_name'] + '%'))

            if RulesBranch.description.name in inputs:
                data = data.filter(RulesBranch.description.ilike('%' + inputs['description'] + '%'))
            for piece in data:
                self.msg.append(piece.__Publish__())

        #If the user is present on the inputs then take the user.
        if "user" in inputs:
            data = self.session.query(RulesUser).filter(RulesUser.user_code==int(inputs['user']))
            if RulesUser._name.name in inputs:
                data = data.filter(RulesUser._name.ilike('%' + inputs['_name'] + '%'))

            if RulesUser.description.name in inputs:
                data = data.filter(RulesUser.description.ilike('%' + inputs['description'] + '%'))
            for piece in data:
                self.msg.append(piece.__Publish__())

        return {"status": 200, "value": self.msg, "type": "application/json"}
