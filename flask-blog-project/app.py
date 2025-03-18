from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from sqlalchemy.orm import DeclarativeBase
from flask_migrate import Migrate

# Define the Base class
class Base(DeclarativeBase):
    pass


# create an instance of the Flask class
app = Flask(__name__)

# secret key
app.config['SECRET_KEY'] = 'e5b6c9d4f2c7a91c8b2f5a1e8c6d3f7u9a0b4c2d5e6f7a8b1c2d3e4f5g6h7i8j'

# create an instance of the SQLAlchemy class
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog_db.db'

# disable modification tracking to improve performance
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.config['SESSION_COOKIE_SECURE'] = True  # Use Secure Cookies in production
app.config['SESSION_COOKIE_HTTPONLY'] = True  # Prevent JavaScript access to cookies
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'  # Prevent CSRF attacks


# create an instance of the SQLAlchemy class
db = SQLAlchemy(model_class=Base)
db.init_app(app)  # <-- Bind the database instance to the Flask app

# Initialize Flask-Migrate 
migrate = Migrate(app, db)

# login manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message_category = "info"  # Flash message category

from routes import *
from forms import *
from flask import redirect, url_for, request

# redirect user from login/signup page to dashboard if user is already logged in
@app.before_request
def redirect_logged_in_users():
    if current_user.is_authenticated and request.endpoint in ['login', 'signup']:
        return redirect(url_for('dashboard'))
    
    
if __name__ == "__main__":
    with app.app_context():
        db.create_all() # create the table (it shall create a db when its not there)

    app.run(debug=True)


