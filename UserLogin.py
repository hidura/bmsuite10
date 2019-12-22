import hashlib

import flask_login

from tools.DataBase.Definition.Base import db
from tools.DataBase.Definition.Contact import Contact
from tools.DataBase.Definition.User import User
from passlib.hash import sha256_crypt as crypt

class UserInfo(flask_login.UserMixin):
    # proxy for a database of users
    def __init__(self, id):
        self.authenticated = False
        self.username = None
        self.name = None
        self.avatar = None
        # This means that login with the system.
        getUserInfo = db.session.query(Contact.contact_name,
                                       Contact.lastname,User.username, User.avatar). \
            filter(User.code == int(id)).\
            filter(Contact.code ==User.contact).first()
        if getUserInfo!=None:
            self.authenticated=True
            self.name = getUserInfo[0]+" "+getUserInfo[1]
            self.username = getUserInfo[2]
            self.avatar = getUserInfo[3]

        self.id = id

    @classmethod
    def get(cls, id):
        return cls

    def getUsername(self):
        return self.username

    def getName(self):
        return self.name

    def is_authenticated(self):
        return self.authenticated

    def is_active(self):
        return self.authenticated

    def get_id(self):
        return self.id

class UserLogin(flask_login.UserMixin):

    def __init__(self, inputs):

        # This means that login with the system.
        getUserInfo = db.session.query(User). \
            filter(User.username == inputs["username"]).first()
        if getUserInfo != None:
            if crypt.verify(inputs["passwd"], getUserInfo.passwd):
                self.user_info = UserInfo(getUserInfo.code)
                self.user_info.id = getUserInfo.code
            else:
                self.user_info = None
        else:
            self.user_info = None
