from Demos.win32ts_logoff_disconnected import username

from  app import  create_app
from  models import  db ,User

app = create_app()

with app.app_context():
    # 检查管理员是否存在
    admin = User.query.filter_by(username = "admin" ).first()

    if admin:
        print("管理员已存在")

    else:
        admin = User(username  = "admin",is_admin = True)
        admin.set_password("admin123")
        db.session.add(admin)
        db.session.commit()
        print("管理员创建成功：admin / admin123")