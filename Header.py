# This class loads the header of the page and the decorator inside
# Also loads the main information as the groups of modules the user
# Have access.
import json
from functools import wraps

from flask import (request, session)
from markupsafe import Markup

from tools.DataBase.Connect import conection
from tools.DataBase.Definition import db
from tools.DataBase.Definition.Contact import Contact
from tools.DataBase.Definition.User import User
from tools.DataBase.Definition.Views.getNotifications import GetNotification
from tools.DataBase.Definition.Views.getmessages import GetMessages
from tools.DataBase.ODM.DataModelODM import UserModule, Module, Group_module
from tools.DataBase.bmsobjects import Profile

userDetails = Profile


def header(func):
    @wraps(func)
    def func_wrapper():
        if not db.session.is_active:
            db.session.bind.dispose()

        id = session["user_id"]
        userDetails.id = id

        getUserInfo = db.session.query(Contact.contact_name, Contact.lastname,
                                       User.username, User.avatar).\
            filter(User.code == int(id)).\
            filter(Contact.code==User.contact).first()
        if getUserInfo != None:
            userDetails.name=getUserInfo[0]
            userDetails.lastname=getUserInfo[1]
            userDetails.username = getUserInfo[2]
            userDetails.avatar = getUserInfo[3]

            ###Module Extractor
            modules_str = None
            curr_module=""
            module_group=None
            for piece in UserModule.objects(user=int(id), status=11).order_by('+group_name'):
                if module_group != piece.group_name:
                    module_group = piece.group_name
                    if modules_str !=None:
                        modules_str += "</ul></div></li>"
                    elif modules_str == None:
                        modules_str =""
                    modules_str += "<li class='nav-item'>" \
                                        "<a data-toggle='collapse' href='#%s' class='collapsed' aria-expanded='false'>" \
                                            "<i class='%s'></i>" \
                                            "<p>%s</p>" \
                                            "<span class='caret'></span>" \
                                        "</a>" \
                                        "<div class='collapse' id='%s' style=''><ul class='nav nav-collapse'>"%\
                                   (
                                    str(piece.group_name).lower().replace(" ",""),
                                    Group_module.objects(code=piece.group).first().icon,
                                    module_group,
                                    str(piece.group_name).lower().replace(" ",""))

                module_info = Module.objects(code=piece.module).first()

                if str(module_info.path).lower()!=str(request.path).lower():
                    if module_info.path!=None:
                        # This is because the transitioning system and may can encounter with problem
                        modules_str+="<li>" \
                                    "<a href='%s'>" \
                                        "<i class='%s'></i>" \
                                        "<span class='sub-item'>%s</span>" \
                                    "</a>" \
                            "</li>"%(module_info.path, module_info.icon, module_info.name)
                else:

                    if module_info.path!=None:
                        # This is because the transitioning system and may can encounter with problem
                        curr_module = "<li class='nav-item active'>" \
                                    "<a href='%s'>" \
                                        "<i class='%s'></i>" \
                                        "<p>%s</p>" \
                                    "</a>" \
                                "</li>"%(module_info.path, module_info.icon, module_info.name)
                        modules_str += "<li>" \
                                   "<a href='%s'>" \
                                   "<i class='%s'></i>" \
                                   "<span class='sub-item'>%s</span>" \
                                   "</a>" \
                                   "</li>" % (module_info.path, module_info.icon, module_info.name)

            modules_str = modules_str + "</ul></div></li>" if modules_str!=None else ""
            userDetails.modules_group = Markup(curr_module+modules_str)


            ##Message extractor
            messages_query = db.session.query(GetMessages).\
                filter(GetMessages.status == 9).\
                filter(GetMessages.recipient == int(id))
            span_notifications =""
            if messages_query.count()>0:
                span_notifications="<span class='notification'>%s</span>"%(messages_query.count())

            message_str=""
            for piece in messages_query:
                data_message = piece.__Publish__()
                message_str +=data_message[GetMessages.message_content.name]


            messages = """<li class='nav-item dropdown hidden-caret'>
                                <a class='nav-link dropdown-toggle' href='#' id='messageDropdown' role='button' data-toggle='dropdown'
                                aria-haspopup='true' aria-expanded='false'>
                                    <i class='fa fa-envelope'></i>
                                    %s
                                </a>
                                <ul class='dropdown-menu messages-notif-box animated fadeIn' aria-labelledby='messageDropdown'>
                                    <li>
                                        <div class='dropdown-title d-flex justify-content-between align-items-center'>
                                            Mensajes
                                            <a href='#' class='small'>Marcar como leidos</a>
                                        </div>
                                    </li>
                                    <div class='scroll-wrapper message-notif-scroll scrollbar-outer' style='position: relative;'><div class='message-notif-scroll scrollbar-outer scroll-content' style='height: auto; margin-bottom: 0px; margin-right: 0px; max-height: 0px;'>
                                        <div class='notif-center'>
                                            <!--Mensjaes-->%s
                                        </div>
                                        </div><div class='scroll-element scroll-x'><div class='scroll-element_outer'><div class='scroll-element_size'></div><div class='scroll-element_track'></div><div class='scroll-bar ui-draggable ui-draggable-handle'></div></div></div><div class='scroll-element scroll-y'><div class='scroll-element_outer'><div class='scroll-element_size'></div><div class='scroll-element_track'></div><div class='scroll-bar ui-draggable ui-draggable-handle'></div></div></div></div>
                                    </li>
                                    <li>
                                        <a class='see-all' href='javascript:void(0);'>Ver mensajes<i class='fa fa-angle-right'></i> </a>
                                    </li>
                                </ul>
                            </li>"""%(span_notifications,message_str)
            userDetails.messages = Markup(messages)



            ##Notification extractor

            notifications_query = db.session.query(GetNotification). \
                filter(GetNotification.status == 9). \
                filter(GetNotification.recipient == int(id))
            notifications_str=""
            for piece in notifications_query:
                notifications_str+=piece.__Publish__()[GetNotification.notification_content.name]
            span_notifications =""
            if notifications_query.count()>0:
                span_notifications="<span class='notification'>%s</span>"%(notifications_query.count())
            notfications = """<li class='nav-item dropdown hidden-caret submenu'><a class='nav-link dropdown-toggle' href='#' id='notifDropdown' role='button' data-toggle='dropdown' aria-haspopup='true' aria-expanded='false'><i class='fa fa-bell'></i>%s</a><ul class='dropdown-menu notif-box animated fadeIn' aria-labelledby='notifDropdown'><li><div class='dropdown-title'>Tiene %s notificaciones pendientes</div></li><li><div class='scroll-wrapper notif-scroll scrollbar-outer' style='position: relative;'><div class='notif-scroll scrollbar-outer scroll-content' style='height: auto; margin-bottom: 0px; margin-right: 0px; max-height: 256px;'><div class='notif-center'><!--Notifications-->%s</div></div><div class='scroll-element scroll-x' style=''><div class='scroll-element_outer'><div class='scroll-element_size'></div><div class='scroll-element_track'></div><div class='scroll-bar ui-draggable ui-draggable-handle' style='width: 100px;'></div></div></div><div class='scroll-element scroll-y' style=''><div class='scroll-element_outer'><div class='scroll-element_size'></div><div class='scroll-element_track'></div><div class='scroll-bar ui-draggable ui-draggable-handle' style='height: 100px;'></div></div></div></div></li><li class='submenu'><a class='see-all' href='javascript:void(0);'>Ver todas las notificaciones<i class='fa fa-angle-right'></i> </a></li></ul></li>""" % \
                           (span_notifications,notifications_query.count(),notifications_str)
            userDetails.notifications = Markup(notfications)
        return func()
    return func_wrapper

