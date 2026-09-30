from  flask_sqlalchemy import  SQLAlchemy
from  flask_login import  UserMixin
from  datetime import  datetime,timezone

from pygments.lexer import default
from sqlalchemy.orm import backref

db = SQLAlchemy()

class User(UserMixin,db.Model):
    id = db.Column(db.Integer,primary_key  = True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    is_admin = db.Column(db.Boolean,default = False)   # 是不是管理员

    orders = db.relationship("Order",backref = "user")

    def set_password(self,password):
        from werkzeug.security import  generate_password_hash
        self.password_hash = generate_password_hash(password)

    def check_password(self,password):
        from  werkzeug.security import  check_password_hash
        return  check_password_hash(self.password_hash,password)

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float,nullable =  False)
    stock = db.Column(db.Integer,default = 0)  ## 库存

## 购物车项
class CartItem(db.Model):
    id = db.Column(db.Integer,primary_key = True)
    user_id = db.Column(db.Integer,db.ForeignKey("user.id"))
    product_id = db.Column(db.Integer,db.ForeignKey("product.id"))
    quantity = db.Column(db.Integer,default = 1)

    product = db.relationship("Product")

class Order(db.Model):
    id = db.Column(db.Integer,primary_key = True)
    user_id = db.Column(db.Integer,db.ForeignKey("user.id"))
    total = db.Column(db.Float)   ##订单总价
    status = db.Column(db.String(20),default = "待发货")
    created_at = db.Column(db.DateTime,default = lambda :datetime.now(timezone.utc))
    items = db.relationship("OrderItem",backref = "order",cascade = "all,delete-orphan")


class OrderItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey("order.id"))
    product_id = db.Column(db.Integer, db.ForeignKey("product.id"))
    quantity = db.Column(db.Integer)
    price = db.Column(db.Float)  # 下单时的价格

    product = db.relationship("Product")

