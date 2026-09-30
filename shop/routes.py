from flask import redirect, url_for, flash,request
from flask_login import login_required, current_user
from models import db, CartItem, Order, OrderItem,Product
from flask import render_template
from shop import bp

from shop_app.utils import admin_required


@bp.route("/")
def index():
    # 从 URL 取参数
    page = request.args.get("page",1,type = int)
    keyword = request.args.get("q","").strip()

    # 基础查询
    query = Product.query

    # 有关键词就过滤
    if keyword:
        query = query.filter(Product.name.contains(keyword))

    # 分页，每页 6 个
    pagination = query.order_by(Product.id.desc()).paginate(page = page ,per_page = 6)

    return  render_template(
        "shop/index.html",
        pagination = pagination,
        products = pagination.items,
        keyword  = keyword
    )








@bp.route("/cart/add/<int:product_id>",methods = ["POST"])
@login_required
def add_to_cart(product_id):
    # 查商品，找不到 404
    product = Product.query.get_or_404(product_id)

    # 查购物车里有没有这个商品
    item = CartItem.query.filter_by(
        user_id = current_user.id ,
        product_id = product_id
    ).first()

    if item:
        # 已有，数量 +1
        item.quantity +=1
    else:
        # 没有，新建
        item = CartItem(
            user_id = current_user.id,
            product_id = product_id,
            quantity = 1
        )
        db.session.add(item)
    db.session.commit()
    flash(f"已加入购物车：{product.name}")
    return  redirect(url_for("shop.index"))

@bp.route("/cart")
@login_required
def cart():
    # 查当前用户的购物车项
    items = CartItem.query.filter_by(user_id = current_user.id).all()

    # 算总价
    total = sum(item.product.price * item.quantity for item in items)

    return  render_template("shop/cart.html",items = items,total = total)



@bp.route("/checkout", methods=["POST"])
@login_required
def checkout():
    # 查购物车
    items = CartItem.query.filter_by(user_id = current_user.id).all()

    if not items:
        flash("购物车是空的")
        return  redirect(url_for("shop.cart"))

    try:
       # 1. 检查库存，扣库存
       for item in items:
           product = item.product

           if product.stock < item.quantity:
               raise Exception(f"{product.name} 库存不足")

           product.stock -= item.quantity

        # 2. 算总价
       total = sum(item.product.price * item.quantity for item in items)

        # 3. 创建订单
       order = Order(user_id = current_user.id,total = total)
       db.session.add(order)
       db.session.flush()   # 先写入，拿到 order.id

        # 4. 创建订单项，清空购物车
       for item in items:
           order_item = OrderItem(
           order_id = order.id,
           product_id = item.product_id,
           quantity = item.quantity,
           price = item.product.price
           )

           db.session.add(order_item)
           db.session.delete(item)

        # 5. 全部成功，提交
       db.session.commit()

       flash(f"下单成功！订单号：{order.id}")
       return redirect(url_for("shop.orders"))

    except Exception as e :
        # 任何一步失败，全部回滚
        db.session.rollback()
        flash(str(e))
        return redirect(url_for("shop.cart"))




@bp.route("/cart/remove/<int:item_id>",methods= ["POST"])
@login_required
def remove_from_cart(item_id):
    item = CartItem.query.get_or_404(item_id)

    # 只能删自己的
    if item.user_id != current_user.id:
        flash("无权操作")

        return  redirect(url_for("shop.cart"))

    db.session.delete(item)
    db.session.commit()

    flash("已从购物车移除")
    return  redirect(url_for("shop.cart"))


@bp.route("/orders")
@login_required
def orders():
    # 查当前用户的所有订单，按时间倒序
    orders = Order.query.filter_by(user_id = current_user.id).order_by(Order.created_at.desc()).all()

    return render_template("shop/orders.html", orders=orders) # ✅ orders

@bp.route("/cart/update/<int:item_id>",methods = ["POST"])
@login_required
def update_cart(item_id):
    item = CartItem.query.get_or_404(item_id)

    # 只能改自己的
    if item.user_id != current_user.id:
        flash("无权操作")
        return  redirect(url_for("shop.cart"))

    # 取动作：加还是减
    action = request.form.get("action","")

    if action =="inc":
        # 数量加 1，但不能超过库存
        if item.quantity < item.product.stock:
            item.quantity += 1

        else:
            flash("已达库存上限")

    elif action == "dec":
        # 数量减 1，最小是 1
        if item.quantity > 1 :
            item.quantity -= 1

    db.session.commit()
    return  redirect(url_for("shop.cart"))
