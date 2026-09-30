from  flask import  Flask
from  flask_login import  LoginManager
from  config import  Config

from  models import  db,User

login_manager = LoginManager()

@login_manager.user_loader
def load_user(user_id):
    return  db.session.get(User,int(user_id))


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)


    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view ="auth.login"

    from auth import  bp as auth_bp
    app.register_blueprint(auth_bp,url_prefix ="/auth")

    from shop import  bp as shop_bp
    app.register_blueprint(shop_bp)

    from  admin import  bp as  admin_bp
    app.register_blueprint(admin_bp, url_prefix="/admin")

    with app.app_context():
        db.create_all()

    return  app

if __name__ == "__main__":
    app = create_app()
    app.run(debug = True)