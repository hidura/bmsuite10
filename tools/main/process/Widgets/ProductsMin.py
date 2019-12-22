from tools.DataBase.Definition import db
from tools.DataBase.Definition.Views.ItemMins import ItemMins
from tools.DataBase.Definition.WareHouse import WareHouse


class ProductsMin:
    def __init__(self):
        self.msg={"min_products":[]}

    def getLowest(self, maxitems=10):
        data = db.session.query(ItemMins). \
            filter(WareHouse.mainwarehouse == True).\
            order_by(ItemMins.amount.desc())
        for piece in data:
            del piece.__dict__['_sa_instance_state']
            self.msg["min_products"].append(piece.__Publish__())
        return self.msg


