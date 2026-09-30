from  flask import  render_template,redirect,url_for,flash,request
from  flask_login import  login_user ,logout_user,login_required
from  auth import  bp
from  models import  db, User


@bp.route("/register",methods = ["GET","POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username","").strip()
        password = request.form.get("password","").strip()

        if not username or not password:
            flash("用户名和密码不能为空")
            return  redirect(url_for("auth.register"))

        if User.query.filter_by(username = username).first():
            flash("用户名已存在")
            return redirect(url_for("auth.register"))

        user = User(username = username)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()

        flash("注册成功，请登录")
        return  redirect(url_for("auth.login"))

    return  render_template("auth/register.html")

@bp.route("/login",methods = ["GET","POST"])
def login():
    if  request.method == "POST":
        username = request.form.get("username","").strip()
        password = request.form.get("password","").strip()

        if not username or not  password :
            flash("用户名和密码不能为空")
            return  redirect(url_for("auth.login"))

        user = User.query.filter_by(username = username).first()

        if user is None or not user.check_password(password):
            flash("用户名或密码错误")
            return  redirect(url_for("auth.login"))

        login_user(user)
        flash("登录成功")

        return redirect(url_for("shop.index"))

    return render_template("auth/login.html")

@bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("已退出登录")
    return redirect(url_for("auth.login"))

