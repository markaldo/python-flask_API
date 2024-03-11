from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///Users.db"
app.config["SQLALCHEMY_ECHO"] = True
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    surname = db.Column(db.String(25), nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    country = db.Column(db.String(40), nullable=False)
    city = db.Column(db.String(50), nullable=False)
    address = db.Column(db.String(100), nullable=False)
    telephone = db.Column(db.Integer, unique=True, nullable=False)
    frequency = db.Column(db.Integer,nullable=False, default='0')
    password = db.Column(db.String(50), nullable=False, default='0')

    def __repr__(self):
        return f"('{self.id}', '{self.name}', '{self.surname}','{self.email}', '{self.country}', '{self.city}', '{self.address}', '{self.telephone}', '{self.frequency}')"

class Gallery(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=False)
    image = db.Column(db.Text, unique=True, nullable=False)
    mimetype = db.Column(db.Text, nullable=False)
    picode = db.Column(db.String(50), nullable=False)
    club = db.Column(db.String(50), nullable=False)
    place = db.Column(db.String(50), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    email = db.Column(db.String(50), unique=True, nullable=False)

    def __repr__(self):
        return f"('{self.title}', '{self.mimetype}', '{self.picode}', '{self.club}', '{self.place}' , '{self.date_posted}')"

class Frequency(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50), unique=True, nullable=False)
    frequency = db.Column(db.Integer,nullable=False, default='0')

    def __repr__(self):
        return f"{self.frequency}"

db.create_all()
db.session.commit()

def test():
  db.session.add(User(name="Jose",surname="Preec", email="nail@hotmail.com", country="Script", city="Voola", address="Flat 9", telephone="5504", password="rest"))
  db.session.commit()
  db.session.close()
print("User Table successfully Made!")

db.engine.table_names()