from  admin  import  bp
from flask import render_template,request,redirect,url_for,flash
from  flask_login import login_required
from  utils import  admin_required
from models import Product, db,CartItem, Order


@bp.route("/")
@login_required
@admin_required
def index():
    # 查所有商品
    products = Product.query.order_by(Product.id.desc()).all()
    return  render_template("admin/index.html",products = products)


@bp.route("/product/new", methods = ["GET","POST"])
@login_required
@admin_required
def new_product():
    if request.method == "POST":
        name = request.form.get("name","").strip()
        price = request.form.get("price","").strip()
        stock = request.form.get("stock","").strip()

        # 校验
        if not name or not price or not  stock:
            flash("所有字段都不能为空")
            return redirect(url_for("admin.new_product"))

        try:
            price = float(price)
            stock  = int(stock)

        except ValueError:
            flash("价格和库存必须是数字")
            return  redirect(url_for("admin.new_product"))


        # 创建商品
        product = Product(name = name ,price = price,stock = stock)
        db.session.add(product)
        db.session.commit()

        flash(f"商品已添加：{name}")
        return  redirect(url_for("admin.index"))

    return render_template("admin/new_product.html")

@bp.route("/product/<int:product_id>/edit",methods = ["GET","POST"])
@login_required
@admin_required
def edit_product(product_id):
    product = Product.query.get_or_404(product_id)

    if request.method == "POST":
        name = request.form.get("name","").strip()
        price = request.form.get("price","").strip()
        stock = request.form.get("stock","").strip()

        if not name or not price or not stock:
            flash("所有字段都不能为空")

            return redirect(url_for("admin/edit_product",product_id = product_id))

        try:
            price =float(price)
            stock =int(stock)

        except ValueError:
            flash("价格和库存必须是数字")
            return  redirect(url_for("admin.edit_product",product_id = product_id))

        product.name = name
        product.price = price
        product.stock = stock
        db.session.commit()

        flash("修改成功")
        return  redirect(url_for("admin.index"))

    return  render_template("admin/edit_product.html",product = product)

@bp.route("/product/<int:product_id>/delete",methods =["POST"])
@login_required
@admin_required
def delete_product(product_id):
    product = Product.query.get_or_404(product_id)

    # 检查有没有购物车引用
    if CartItem.query.filter_by(product_id = product_id).first():
        flash("该商品在用户购物车中，无法删除")
        return  redirect(url_for("admin.index"))

    db.session.delete(product)
    db.session.commit()

    flash(f"已删除：{product.name}")

    return  redirect(url_for("admin.index"))


@bp.route("/orders")
@login_required
@admin_required
def orders():
    # 查所有订单，按时间倒序
    orders = Order.query.order_by(Order.created_at.desc()).all()
    return  render_template("admin/orders.html",orders = orders)


@bp.route("/order/<int:order_id>/status",methods = ["POST"])
@login_required
@admin_required
def update_order_status(order_id):
    order  = Order.query.get_or_404(order_id)

    new_status = request.form.get("status","").strip()

    # 只允许这几个状态
    if new_status not in ["待发货","已发货","已完成"]:
        flash("无效的状态")
        return  redirect(url_for("admin.orders"))

    order.status = new_status
    db.session.commit()

    flash(f"订单 #{order.id} 状态已更新为：{new_status}")
    return redirect(url_for("admin.orders"))

