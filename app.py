import sys
import os


sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import json
from collections import OrderedDict
from datetime import timedelta
import flask_login
import requests
from flask import Flask, request, render_template, session, url_for, redirect, flash
from flask_login import LoginManager, login_required
from markupsafe import Markup

from passlib.hash import sha256_crypt as crypt


ALLOWED_EXTENSIONS = set(['pdf', 'png', 'jpg', 'jpeg'])


from tools.DataBase.Definition.Base import db

from tools.DataBase.CodeGenerator import CodeGen
from tools.DataBase.ODM.DataModelODM import waiterKey, account_movement, Module, ModulesFields

from tools.DataBase.Connect import conection
from tools.DataBase.Definition.SupplierOrder import SupplierOrder
from tools.DataBase.Definition.Views.getaccounts import getaccounts
from tools.DataBase.Definition.Type import Type
from tools.DataBase.Definition.BuyOrderTbl import BuyOrderTbl
from tools.DataBase.Definition.WareHouse import WareHouse
from tools.DataBase.Definition.Contact import Contact
from tools.DataBase.Definition.category import category
from tools.DataBase.Definition.ncf import NCF
from tools.DataBase.Definition.Supplier import Supplier
from tools.DataBase.Definition.Level import Level
from tools.DataBase.Definition.Views.ItemMins import ItemMins
from tools.DataBase.Definition.company import company
from tools.DataBase.bmsobjects.Modules import Modules
from tools.DataBase.Definition.User import User

app = Flask(__name__)
login_manager = LoginManager()

login_manager.init_app(app)

UPLOAD_FOLDER = os.path.dirname(os.path.abspath(__file__))+'/static/'

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
with open(os.path.dirname(os.path.abspath(__file__))+"/config.json") as f:
    config = json.loads(f.read())
    app.secret_key = config["secret_key"]
    app.config["SQLALCHEMY_DATABASE_URI"] = config["postgres"]
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # This is by default don't touch it.
    app.config["MAIL_SERVER"] = config["mail"]["host"]
    app.config["MAIL_PORT"] = int(config["mail"]["port"])
    app.config["MAIL_USE_SSL"] = True
    app.config["MAIL_USERNAME"] = config["mail"]["username"]
    app.config["mail"] = config["mail"]["mail"]
    app.config["MAIL_PASSWORD"] = config["mail"]["password"]
    conection().conODM(config)

with app.app_context():
    db.init_app(app)

    from tools.main import general
    from tools.main.general import RequestProc
    from tools.main.process.BuyOrder import BuyOrder
    from tools.main.process.Items import Items
    from tools.main.process.Widgets.ProductsMin import ProductsMin
    from tools.main.process.Widgets.TotalSales import TotalSales
    from tools.main.process.supplier import supplier
    from main import main
    from Header import header, userDetails
    from UserLogin import UserLogin, UserInfo
    from werkzeug.utils import secure_filename


static_file_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'static')
db.init_app(app)
bmsnet='http://bmsuite.io:3588/'
application = app




@app.route("/", methods=['GET', 'POST'])
def process():
    # The processor that receive the classnmae
    # and execute the process
    arguments = RequestProc(request).dataPckg

    if 'key' not in arguments and 'usercode' not in arguments:
        if "user_id" not in session:
            return render_template('login.html', basic={"title": "Login"})
        arguments["__usercode__"] = session["user_id"]
    elif 'key' in arguments and 'usercode' in arguments:
        #Prioritize the usercode over the key
        del arguments['key']
        
    if "classname" in arguments:
        clasname_full = arguments["classname"]

        if len(clasname_full.split("."))>1:
            classname = clasname_full.split(".")[0]
            method = clasname_full.split(".")[1]
            try:
                value = main().exec_code(classname, method, arguments)

                return json.dumps(value["value"])
            except ValueError as e:
                return e
    else:

        if 'user_id' in session:
            return redirect(url_for('index'))
        return render_template('login.html',basic={"title" : ""})

##Open New Orders page
@app.route('/new_orders', methods=['GET'])
@login_required
@header

def new_orders():
    return render_template('new_order.html',basic={"title":"Nueva orden de compra"}, user_details=userDetails,
                           data=BuyOrder().loadInitial())


##Open New Request to BMSUITE Order
@app.route('/request_orders', methods=['GET'])
@login_required
@header
def request_orders():
    return render_template('request_orders.html',basic={"title":"Nueva cotizacion"},
                           user_details=userDetails,
                           data=BuyOrder().loadInitial())


##Open New supplier Order
@app.route('/buyorder', methods=['GET'])
@login_required
@header
def buyorder():

    data = BuyOrder().loadInitial()

    return render_template('supplier_order.html',basic={"title":"Nueva orden de compra"},
                           user_details=userDetails,
                           data=data)


##Account program
@app.route('/account_program', methods=['GET'])
@login_required
@header
def account_program():
    msg={"accounts":[],"title":"Programación de cuentas"}
    for piece in db.session.query(getaccounts):
        msg['accounts'].append(piece.__Publish__())

    msg['modules']=Module.objects()
    return render_template('account_program.html',basic=msg,
                           user_details=userDetails)




##Open New Request to BMSUITE Order
@app.route('/gen607', methods=['GET'])
@login_required
@header
def gen607():
    return render_template('gen607.html', basic={"title": "607 Report"},
                           user_details=userDetails,
                           data=BuyOrder().loadInitial())



## Add new products to BMSUITE
@app.route('/product_add', methods=['GET'])
@login_required
@header
def products_add():
    return render_template('product_add.html',basic={"title":"Nuevo productos"},
                           user_details=userDetails,
                           data=BuyOrder().loadInitial())

## Add new products to BMSUITE
@app.route('/category_add', methods=['GET'])
@login_required
@header
def category_add():
    return render_template('category_add.html',basic={"title":"Nueva categoria"},
                           user_details=userDetails)


## Add new products to BMSUITE
@app.route('/categories', methods=['GET'])
@login_required
@header
def categories():
    return render_template('category.html', basic={"title": "Categorías"},
                           user_details=userDetails)



## Add new products to BMSUITE
@app.route('/sales_rep', methods=['GET'])
@login_required
@header
def sales_rep():
    data = {"product_type": db.session.query(Type).filter_by(level=4).all(),
            "categories": db.session.query(category).all(),
            "cat_type":db.session.query(Type).filter_by(level=13).all()}

    return render_template('sales_rep.html',basic={"title":"Reporte de ventas"},
                           user_details=userDetails,
                           data=data)


## Add new products to BMSUITE
@app.route('/accounts', methods=['GET'])
@login_required
@header
def accounts():
    accounts_lst=db.session.query(getaccounts).order_by(getaccounts.account_type)
    msg={}
    account_type=""
    for account in accounts_lst:
        piece = account.__Publish__()

        if account_type!=piece[getaccounts.acc_type.name]:
            target = []
            msg[piece[getaccounts.acc_type.name]]={piece[getaccounts.level_name.name]:target}
            account_type=piece[getaccounts.acc_type.name]
        else:
            target=msg[piece[getaccounts.acc_type.name]][piece[getaccounts.level_name.name]]
        balance=piece[getaccounts.cur_balance.name]
        piece[getaccounts.cur_balance.name]='{0:,.2f}'.format(float(balance))
        target.append(piece)

    return render_template('accounts.html',basic={"title":"Libro de cuentas"},
                           user_details=userDetails,
                           data={"accounts":msg})



## Add new products to BMSUITE
@app.route('/cashflow', methods=['GET'])
@login_required
@header
def cashflow():
    return render_template('cashflow.html',basic={"title":"Flujo de efectivo"},
                           user_details=userDetails,
                           data=BuyOrder().loadInitial())


## Modify products to BMSUITE
@app.route('/products', methods=['GET'])
@login_required
@header
def products():
    return render_template('products.html',basic={"title":"Modificación de productos"},
                           user_details=userDetails,
                           data=BuyOrder().loadInitial())



## Add Groups
@app.route('/groups', methods=['GET'])
@login_required
@header
def groups():
    modulesInfo=Modules(static_file_dir)
    modulesInfo.loadInfo()
    return render_template('groups.html', basic={"title":"Nuevo grupo"},
                           user_details=userDetails, modules_info=modulesInfo)


## Add Orders Rep
@app.route('/orders_rep', methods=['GET'])
@login_required
@header
def orders_rep():
    modulesInfo=Modules(static_file_dir)
    modulesInfo.loadInfo()
    return render_template('orders_rep.html', basic={"title":"Reporte de ordenes"},
                           user_details=userDetails, modules_info=modulesInfo)

## Add Accounts Financially
@app.route('/add_account', methods=['GET'])
@login_required
@header
def add_account():
    accounts_level=db.session.query(Level).\
        filter(Level.code>=18).\
        filter(Level.code<=24)
    accounts=[]
    for piece in accounts_level:
        accounts.append(piece.__Publish__())
    return render_template('add_accounts.html', basic={"title":"Nueva cuenta", "accounts_level":accounts},

                           user_details=userDetails)




## Get products By
@app.route('/getProductsBy', methods=['GET', 'POST'])
def getProductsBy():
    inputs = request.get_json()
    return json.dumps(Items().Get(inputs)["value"])


## Get Suppliers By
@app.route('/getSuppliersBy', methods=['GET', 'POST'])
def getSuppliersBy():
    inputs = request.get_json()
    return json.dumps(supplier().Get(inputs)["value"])

##Create the Order
@app.route('/add_order', methods=['GET', 'POST'])
def add_order():
    return json.dumps(BuyOrder().create(request.get_json()))


##Create the Order
@app.route('/req_order', methods=['GET', 'POST'])
@login_required
@header
def req_order():

    inputs=request.get_json()
    request_data = BuyOrder().create(inputs)# The request save it on the System.

    inputs["contact_email"] = userDetails.username
    inputs["commerce_client"] =db.session.query(company.maincode).first()[0]
    inputs["supplier_name"] = inputs["products"][0]["supplier_name"]
    inputs["supplier"] = inputs["products"][0]["supplier"]

    inputs["supplier_email"] = db.session.query(Contact.email).\
        filter(Contact.code==Supplier.contact).\
        filter(Supplier.code==inputs["products"][0]["supplier"]).first()[0]
    inputs["contact_name"] = userDetails.name+" "+userDetails.lastname
    inputs["created_by"]= userDetails.id
    inputs["code"]=request_data["code"]
    warehose_info=db.session.query(WareHouse).filter(WareHouse.code==int(inputs["warehouse"])).first()

    if warehose_info!=None:
        inputs["_address"]=warehose_info.warehouse_name+", dirección:"+warehose_info._address

    fulldate=inputs["receive_date"]+" "+inputs["recive_time"]
    inputs["_date"]=fulldate
    inputs["bmsnet"]=bmsnet
    bmsuite_req = BuyOrder().requestProducts(inputs)# The request to bmsuite.
    key_uuid=bmsuite_req["key"]
    supplier_order={SupplierOrder.status.name:11,
                          SupplierOrder.supplier_name.name: str(inputs["products"][0]["supplier_name"]),
                          SupplierOrder._date.name:general().date2julian(),
                          SupplierOrder.key_uuid.name:key_uuid,
                          SupplierOrder.bill_id_int.name:int(request_data[BuyOrderTbl.code.name]),
                          SupplierOrder.created_by.name:int(userDetails.id),
                          SupplierOrder.supplier_id.name:int(inputs["products"][0]["supplier"])}

    SupplierOrder.insert(supplier_order)

    return json.dumps(bmsuite_req)


##View the order.
@app.route('/view_order', methods=['GET'])
@login_required
@header
def view_order():
    order_id = request.args.get("id")
    headers = {'Content-Type': 'application/json'}
    response = requests.post(bmsnet+'view_bms_order',data=json.dumps({"id":order_id}),headers=headers)
    if response.status_code!=200:
        return "Bad order"
    else:

        return render_template('bill_model.html', basic={"title": "Ver Ordenes"},
                        user_details=userDetails, data=json.loads(response.content.decode()))


##Create the Order
@app.route('/take_order', methods=['POST'])
def take_order():
    #Send the order to the main site and make it save it there.
    inputs = request.form.to_dict()
    inputs["status"]=102 if "status" not in inputs else int(inputs["status"])
    headers = {'Content-Type': 'application/json'}
    response = requests.post(bmsnet+'take_order',
                             data=json.dumps(inputs), headers=headers)

    return response.content

##View the order.
@app.route('/mark_receive', methods=['POST'])
def mark_receive():
    if (len(request.form.to_dict().items()))>0:
        #That means that is from the webpage localy
        inputs=request.form.to_dict()
    else:
        inputs=json.loads(request.data.decode())

    orderDetails = {}
    # Updating the products.
    for piece in OrderedDict(sorted(inputs.items())):
        if len(piece.split("|")) > 1:
            if piece.split("|")[0] not in orderDetails:
                orderDetails[piece.split("|")[0]] = {}

            orderDetails[piece.split("|")[0]][piece.split("|")[1]] = str(inputs[piece]).replace(",", "")
            del inputs[piece]
    inputs["products"]=orderDetails
    connection = db.engine.raw_connection()
    cursor = connection.cursor()

    cursor.callproc('addorders', [json.dumps(inputs)])
    data = list(cursor.fetchall())
    cursor.close()

    headers = {'Content-Type': 'application/json'}
    response = requests.post(bmsnet+'/set_received',
                             data=json.dumps({"id": inputs["orderid"]}), headers=headers)
    if response.status_code != 200:
        return "Bad order"
    else:
        return "Salvado"


##Open New Orders page
@app.route('/dashboard', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
@login_required
@header
def index():
    return render_template('index.html', basic={"title":"Dashboard"}, user_details=userDetails)

##Open New Orders page
@app.route('/getfields_module', methods=['GET', 'POST'])
@login_required
@header
def getfields_module():
    arguments = RequestProc(request).dataPckg
    return ModulesFields.objects(module=arguments['module']).to_json()


# Login
@app.route("/login")
def login():
    return render_template('login.html', basic={"title": "Login"})


# Permissions
@app.route("/permissions", methods=['GET'])
@login_required
@header
def permissions():
    return render_template('permissions.html', basic={"title": "Manejador de permisos"}, user_details=userDetails)


# Products Minimum
@app.route("/products_min", methods=['GET'])
@login_required
@header
def products_min():
    minprods=ProductsMin().getLowest()["min_products"]

    return render_template('products_min.html', basic={"title": "Reporte de products minimos"},
                           user_details=userDetails,data=minprods)


# Modules
@app.route("/modules", methods=['GET', 'POST'])
@login_required
@header
def modules():
    modulesInfo=Modules(static_file_dir)
    modulesInfo.loadInfo()
    return render_template('modules.html', basic={"title": "Manejador de modulos"},
                           user_details=userDetails, modules_info=modulesInfo)

@login_manager.user_loader
def load_user(user_id):
    return UserInfo.get(user_id)

@app.errorhandler(401)
def unauthorized(e):
    return render_template('unathorized.html',basic={'title':'Acceso no autorizado'}), 401

@app.route("/loginweb", methods=['POST'])
def loginweb():
    # Here we use a class of some kind to represent and validate our
    # client-side form data. For example, WTForms is a library that will
    # handle this for us, and we use a custom LoginForm to validate.

    userlogin = UserLogin(request.form).user_info

    remember = False
    duration = timedelta(days=0.0)
    if 'rememberme' in request.form:
        if request.form['rememberme'] == 'on':
            remember = True
            duration = timedelta(days=6.0)
    if userlogin != None:
        flask_login.login_user(userlogin, remember=remember)

        return redirect(url_for('index'))

    return render_template('login.html', basic={"title": "Nombre de usuario y contraseña no valido"})




# New Suppliers
@login_required
@header
@app.route("/new_supplier", methods=['GET', 'POST'])
def new_supplier():
    return render_template('addsupplier.html',
                           user_details=userDetails, basic={"title": "Registro de suplidores"})


# Add Entry
@login_required
@header
@app.route("/addentry", methods=['GET', 'POST'])
def addentry():
    return render_template('addentry.html',
                           user_details=userDetails, basic={"title": "Registro de movimientos"})



# New Supplier
@app.route("/addnewsupplier", methods=['POST'])
@login_required
@header
def addnewsupplier():
    msg = None
    if request.method == 'POST':
        file_dst = None
        # validations
        contact_data={
            Contact.contact_name.name:request.form['first_name'],
            Contact.lastname.name: request.form['last_name'],
            Contact.email.name: request.form['email'],
            Contact.telephone.name: request.form['telephone'],
            Contact.cellphone.name: request.form['cellphone'],
            Contact.status.name:11
        }
        contact_info=Contact.insert(contact_data)
        file_dst="/static/images/avatar/Ym1zdWl0ZSB1c2VyKGJveSkgd2l0aG91dCBhdmF0YXI=.svg"
        if "avatar" in request.files:
            file = request.files['avatar']
            if file.filename == '':
                mgs = "No file has been selected"
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                file_dst = app.config['UPLOAD_FOLDER'] + "/" + filename

        data = {User.username.name: request.form['email'],
                User.status.name:11,
                User.contact.name: contact_info.code,
                'passwd': request.form['passwd'],
                'usrtype': int(request.form['usertype']),
                User.avatar.name:file_dst}

        data['passwd'] = general().gen_hash(data['passwd'])
        #data['uuid'] = uuid.uuid4().__str__()
        user_inf=User.insert(data)

        Supplier.insert({Supplier.status.name: 11,
                         Supplier.sup_name.name: request.form['sup_name'],
                         Supplier.rnc.name: request.form['rnc'],
                         Supplier.user_code.name: user_inf.code,
                         Supplier.telephone.name: request.form['telephone'],
                         Supplier.contact.name: contact_info.code,
                         Supplier._address.name: request.form['_address']
                         })

        # raw_conn = db.engine.raw_connection()
        # cursor = raw_conn.cursor()
        #
        # cursor.callproc('routnot_messages', [request.form['username'], user_inf.code])
        # raw_conn.commit()
        # data = cursor.fetchall()[0]
        flash('Your Account has been created successfully')
        return redirect(url_for('new_supplier'))





# New Users
@app.route("/addnewuser", methods=['GET', 'POST'])
@login_required
@header
def addnewuser():
    msg = None
    if request.method == 'GET':
        data={"usertype":db.session.query(Type).filter_by(level=7).all()}

        return render_template('new_user.html',
                               basic={"title": "Registro de usuarios"},
                           user_details=userDetails, data=data)
    if request.method == 'POST':
        file_dst = None
        # validations
        contact_data={
            Contact.contact_name.name:request.form['first_name'],
            Contact.lastname.name: request.form['last_name'],
            Contact.email.name: request.form['username'],
            Contact.telephone.name: request.form['telephone'],
            Contact.cellphone.name: request.form['cellphone'],
            Contact.status.name:11
        }
        contact_info=Contact.insert(contact_data)
        file_dst="/static/images/avatar/Ym1zdWl0ZSB1c2VyKGJveSkgd2l0aG91dCBhdmF0YXI=.svg"
        if "avatar" in request.files:
            file = request.files['avatar']
            if file.filename == '':
                mgs = "No file has been selected"
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                file_dst = app.config['UPLOAD_FOLDER'] + "/" + filename

        data = {User.username.name: request.form['username'],
                User.status.name:11,
                User.contact.name: contact_info.code,
                'passwd': request.form['passwd'],
                'usrtype': int(request.form['usertype']),
                User.avatar.name:file_dst}

        data['passwd'] = general().gen_hash(data['passwd'])
        #data['uuid'] = uuid.uuid4().__str__()
        user_inf=User.insert(data)

        if len(request.form["waiter_key"])>0:
            code = CodeGen().GenCode({"table": "waiterKey", "column": "code"})

            waiterKey(code=code, user_code=user_inf.code, key=request.form["waiter_key"],
                      created_by=user_inf.code,
                      created_date=general().date2julian()).save()
        flash('Your Account has been created successfully')
        return redirect(url_for('login'))



def totalsales():

    return TotalSales().getGeneralSales()

def minproducts():
    minprods=ProductsMin().getLowest()
    htmlstr = "<div class='row'>"
    cont = 1
    for piece in minprods["min_products"][:11]:
        id_name=str(piece[ItemMins.item_name.name]).replace(" ","")

        if cont % 3==0:
            htmlstr+="</div><div class='row'>"
        htmlstr += "<div class='col-md-4'><div id='%s' mindata='%s' maxdata='%s'></div>" \
                   "<script>" \
                        "var chart = c3.generate(" \
                            "{" \
                   "            bindto: '#%s',data: {columns: [['%s', %s]],type: 'gauge'},gauge: " \
                   "{label:'%s',min: 0,max: %s,    units: '' },size: {height: 180}});chart.load()</script></div>"%(
                                id_name.lower()+str(piece[ItemMins.item_code.name]),
                                str(piece[ItemMins.amount.name]),
                                str(piece[ItemMins.buyamount.name]),
                                id_name.lower()+ str(piece[ItemMins.item_code.name]),
                                     piece[ItemMins.item_name.name],
                                    str(piece[ItemMins.amount.name]),
                                     piece[ItemMins.item_name.name],
                                    str(piece[ItemMins.buyamount.name]))

    htmlstr += "</div>"

    return Markup(htmlstr)

def gen_hash(data):
    """ generate the hashes for the passwords """
    password_gen = crypt.encrypt(data)
    return password_gen


## Helpers

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def validate_data(data):
    """
    validates the data given and check for inaccuracies
    then removes the redundant data
    :param data: dict
    :return: tuple: bool, errors
    """
    error = None
    result = False
    empty = [True for x in data.values() if not x or x.isspace() or x == '0']
    app.logger.info(empty)
    if empty != []:
        error = "Please fill the empty fields in order to create an account"

    elif data['username'] != data['email2']:
        error = "The email addresses don't match"

    elif check_email_existance(data['username']):
        error = 'The email you\'re trying to use is already taken'

    elif data['passwd'] != data['password2']:
        error = "The passwords don't match"

    else:
        result = True
        data.pop('email2'); data.pop('password2')

    return result, error



def check_email_existance(email):
    """
    checks if the email already exists in the database.
    :param email: string
    :return: bool
    """
    result = True
    user = User.query.filter_by(username=email).first()
    if user is not None:
        flash(str(user))
    else:
        result = False
    return result

app.jinja_env.globals.update(totalsales=totalsales)
app.jinja_env.globals.update(minproducts=minproducts)


