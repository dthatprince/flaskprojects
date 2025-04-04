from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase


# Define the Base class
class Base(DeclarativeBase):
    pass

# create an instance of the SQLAlchemy class
db = SQLAlchemy(model_class=Base)