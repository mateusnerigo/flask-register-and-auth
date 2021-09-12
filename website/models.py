from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

# Creating Notes table
class Notes(db.Model) :

  # Creating columns
  id = db.Column(
    db.Integer,
    primary_key=True
  )

  date = db.Column(
    db.DateTime(timezone=True),
    default=func.now()
  )

  data = db.Column(db.String(10000))

  # creating a foreign key column
  user_id = db.Column(
    db.Integer,
    db.ForeignKey('users.id')
  )


# Creating Users table
class Users(db.Model, UserMixin) :

  # Creating columns
  id = db.Column(
    db.Integer,
    primary_key=True
  )

  email = db.Column(
    db.String(150),
    unique=True
  )

  password = db.Column(db.String(150))
  first_name = db.column(db.String(150))
  notes = db.relationship('Notes')
