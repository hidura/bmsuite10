from mongoengine import Document,LongField,StringField,DateTimeField
from mongoengine.base.fields import ObjectIdField

from tools.DataBase.CodeGenerator import CodeGen
from tools.DataBase.Connect import conection



###This is the internal database,that is used to create a lot of thins like:
#Labels, and define their values on the site depending on the system.
#Buttons and webpages too.

class Label(Document):
    id = ObjectIdField()
    name = StringField(required=True)#The id on the webpage
    value = StringField(required=True)#Default value of the label

class Language(Document):
    id = ObjectIdField()
    name = StringField(required=True)#The language name
    code = StringField(required=True)#The language code

class LabelValue(Document):
    id = ObjectIdField()
    value = StringField(required=True)
    language = StringField(required=True)#ID of the language
    label = StringField(required=True)


if __name__ == '__main__':
    None

__author__ = 'hidura'
