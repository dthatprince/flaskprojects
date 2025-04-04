from flask import Flask
from flask_login import LoginManager
from db import db
from flask_migrate import Migrate

from sites.sites_blueprint import sites_blueprint
from auth.auth_blueprint import auth_blueprint, User
from posts.posts_blueprint import posts_blueprint



# create an instance of the Flask class
app = Flask(__name__)

# blueprints
app.register_blueprint(sites_blueprint, url_prefix='/')
app.register_blueprint(auth_blueprint, url_prefix='/auth')
app.register_blueprint(posts_blueprint, url_prefix='/blog')
#app.register_blueprint(posts_blueprint, url_prefix='/blog')

# secret key
app.config['SECRET_KEY'] = 'e5b6c9d4f2c7a91c8b2f5a1e8c6d3f7u9a0b4c2d5e6f7a8b1c2d3e4f5g6h7i8j'

# create an instance of the SQLAlchemy class
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog_db.db'

# disable modification tracking to improve performance
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.config['SESSION_COOKIE_SECURE'] = True  # Use Secure Cookies in production
app.config['SESSION_COOKIE_HTTPONLY'] = True  # Prevent JavaScript access to cookies
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'  # Prevent CSRF attacks

db.init_app(app)  # <-- Bind the database instance to the Flask app

# Initialize Flask-Migrate 
migrate = Migrate(app, db)

# login manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'auth.login'
login_manager.login_message_category = "info"  # Flash message category

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


if __name__ == "__main__":
    with app.app_context():
        db.create_all() # create the table (it shall create a db when its not there)

    app.run(debug=True)


