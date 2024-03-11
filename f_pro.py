from werkzeug.utils import secure_filename
from flask import Flask, session,render_template, redirect, url_for, request, make_response, flash, abort
import uuid, os
import sqlite3 as lit
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import mimetypes
import random

app = Flask(__name__)
app.secret_key = 'kvpg_YbdT2d45'
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

class Customers(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True)
    name = db.Column(db.String(50), nullable=False)
    surname = db.Column(db.String(25), nullable=False)
    telephone = db.Column(db.Integer, unique=True, nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    password = db.Column(db.String(50), nullable=False, default='0')

    def __repr__(self):
        return f"('{self.id}', '{self.name}', '{self.surname}', '{self.email}' , '{self.telephone}', '{self.date_created}')"

class Employees(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True)
    name = db.Column(db.String(50), nullable=False)
    surname = db.Column(db.String(25), nullable=False)
    mail = db.Column(db.String(50), unique=True, nullable=False)
    address = db.Column(db.String(25), nullable=False)
    saloon = db.Column(db.String(25), nullable=False)
    telephone = db.Column(db.Integer, unique=True, nullable=False)
    table_number = db.Column(db.Integer, unique=True, nullable=False)
    password = db.Column(db.String(50), nullable=False, default='0')

    def __repr__(self):
        return f"('{self.id}', '{self.name}', '{self.surname}', '{self.mail}', '{self.address}',, '{self.saloon}' '{self.telephone}', '{self.table_number}')"

class Appointments(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True)
    employee_id = db.Column(db.Integer, nullable=False)
    cemail = db.Column(db.String(50), nullable=False)
    date_booked = db.Column(db.String(50), default='No Booking Yet')
    image = db.Column(db.Text, unique=True)
    mimetype = db.Column(db.Text)
    picode = db.Column(db.String(50))
    style= db.Column(db.String(50))
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f"('{self.id}', '{self.employee_id}', '{self.cemail}', '{self.date_booked}', '{self.image}', '{self.mimetype}', '{self.style}', '{self.date_posted}', '{self.picode}')"

class Hairstyles(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True)
    name = db.Column(db.String(50), nullable=False)
    code_name= db.Column(db.String(25), nullable=False)
    price=db.Column(db.String(25), nullable=False)
    date_added=db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f"('{self.name}', '{self.code_name}', '{self.price}')"

db.create_all()
db.session.commit()

@app.route('/')
def home():
    if 'email' in session:
        email = session['email']
        return render_template(
            'u_loggedin.html',
            username=email)
    return "You are not logged in <br><a href = '/u_login'>" + "click here to log in to Gallery</a><br>"+"<br>Visit the Saloon <br><a href = '/index'>" + "click here to log in to Appointey</a>"

@app.route('/u_signin', methods = ['GET', 'POST'])
def u_signin():
    sign = 2
    return render_template('home.html', sign = sign) 

@app.route('/welcome', methods = ['GET', 'POST'])
def welcome():
    return redirect(url_for('home'))

@app.route('/u_signup', methods = ['GET', 'POST'])
def u_signup():
    if request.method == "POST":
        flash("Lets get started")
        return redirect(url_for('u_info')) 
    return render_template('u_info.html')  

@app.route('/u_login', methods = ['GET', 'POST'])
def u_login():
   if request.method == 'POST':
      email = request.form['email']
      password = request.form['pwd']
      data=User.query.filter_by(email=email, password=password).first()
      
      if email == "sa@hotmail.com" and password == "marek":
        acc=User.query.filter_by().all()
        return render_template("admain.html", accounts = acc)
      elif data is None:
        ms = "wrong login details or user does not exist!"
        return render_template('home.html', ms = ms)
      else:
        session['email'] = request.form['email']
        if session['email'] is not None:
            frequent()
        return render_template('u_loggedin.html')
   return render_template('home.html')

def frequent():
    data=User.query.filter_by(email=session["email"]).first()
    y=data.frequency
    x = 1+int(y)
    data.frequency = x
    db.session.commit()
    db.session.close() 

@app.route('/u_info', methods = ['GET', 'POST'])
def u_info():
    if request.method == 'POST':
        u_create()
    masg = "Sign In with your new account :)"
    sim = 4
    sign = 2
    return render_template('home.html', sign = sign, masg=masg, sim = sim) 

@app.route('/ubuttons', methods = ['GET', 'POST'])
def ubuttons():
    if request.form['submit'] == 'create':
      show = 2
      accounts=User.query.filter_by().all()
      return render_template('admain.html', show = show, accounts = accounts) 
    if request.form['submit'] == 'update':
      show = 4
      accounts=User.query.filter_by().all()
      return render_template('admain.html', show = show, accounts = accounts) 
    if request.form['submit'] == 'review':
      accounts=User.query.filter_by().order_by(User.frequency.desc()).all()
      return render_template('admain.html', accounts = accounts) 
    if request.form['submit'] == 'delete':
      show = 8
      accounts=User.query.filter_by().all()
      return render_template('admain.html', show = show, accounts = accounts) 

@app.route('/crudma', methods=['GET', 'POST'])
def crudma():
    if request.form['submit'] == 'create':
        u_create()
        return u_read()
    if request.form['submit'] == 'execute':
        u_excute()
        return u_read()
    if request.form['submit'] == 'update':
        u_update()
        return u_profile()
    if request.form['submit'] == 'delete':
        u_delete()
        return u_read()
    if request.form['submit'] == 'change':
        return uc_password()
    if request.form['submit'] == 'erase':
        return u_erase_acc()

def u_create():
        name = request.form['name']
        surname = request.form['surname']
        email = request.form['email']
        country = request.form['country']
        city = request.form['city']
        address = request.form['address']
        telephone = request.form['telephone']
        password = request.form['password']
       
        new_user = User(name=name, surname=surname, email=email, country=country, city=city, address=address, telephone=telephone, password=password)
        new = Frequency(email=email)
        db.session.add(new_user)
        db.session.add(new)
        db.session.commit()
        db.session.close()
        data=User.query.filter_by(email=email, password=password).first()
        return data

def u_read():
    accounts=User.query.filter_by().all()
    return render_template("admain.html", accounts = accounts)

def uc_password():
    email=session['email']
    query=User.query.filter_by(email = email).first() 
    
    #password = request.form['psw']
    #pwd = request.form['pwd']
    #if password == pwd:
    query.password = request.form['pwd']
    db.session.commit()
    db.session.close()
    flash("Password changed successfully")
    return render_template("u_loggedin.html")

def u_erase_acc():
    email=session['email']
    query=User.query.filter_by(email = email).first() 
    old = Frequency.query.filter_by(email=email).first()
    db.session.delete(old)
    db.session.delete(query)
    db.session.commit()
    db.session.close()
    return u_logout()

def u_update():
    if request.method == "POST":
        password = request.form['pwd']
        email = session['email'] 
        query=User.query.filter_by(email=email, password=password).first()  
        if query is None:
            flash("Wrong password or email!")
        else:
           query.name = request.form['name']
           query.surname = request.form['surname']
           query.country = request.form['country']
           query.city = request.form['city']
           query.address = request.form['address']
           query.telephone = request.form['telephone']
           db.session.commit()
           db.session.close()
           flash("Update successful")
        
    return render_template("u_loggedin.html")

def u_excute():
    if request.method == "POST":
        id = request.form['id']
        query=User.query.filter_by(id=id).first()  
        query.name = request.form['name']
        query.surname = request.form['surname']
        query.email = request.form['email']
        query.country = request.form['country']
        query.city = request.form['city']
        query.address = request.form['address']
        query.telephone = request.form['telephone']
        db.session.commit()
        db.session.close()
    flash("Update successful")

@app.route("/u_delete", methods = ["POST", "GET"])
def u_delete():
    if request.method == "POST":
        id = request.form['id'] 
        query=User.query.filter_by(id = id).first()
        db.session.delete(query)
        db.session.commit()
        db.session.close()
        return "Deleted successfully"

@app.route('/u_upload', methods=['GET', 'POST'])
def u_upload():
    title  = request.form['title']
    f = request.files['file']
    club  = request.form['club']
    place  = request.form['place']
    new_filename = uuid.uuid1()
    _, ext = os.path.splitext(f.filename)
    
    if request.form['submit'] == 'add':
        if f is None:
            return 'No pic uploaded!', 400
        if id not in session: 
            f.save('Final Modification/static/ugallery/%s%s' % (new_filename, ext))
            session[title] =  str(new_filename)+ext
           
            filename = secure_filename(f.filename)
            mimetype = f.mimetype
            msg = "file uploaded successfully : )"

            if not filename or not mimetype:
                return 'Bad upload!', 400
            pic = Gallery( title=title, picode=session[title], image=filename, mimetype=mimetype, club=club, place=place, email=session['email'])
            db.session.add(pic)
            db.session.commit()
            db.session.close()
            reply = 2
        return render_template("u_loggedin.html", msg = msg, reply=reply)

    if request.form['submit'] == 'display':
        return u_display()

@app.route('/u_display')
def u_display():
    email = session['email']
    pic = Gallery.query.filter_by(email=email).all()
    if pic is None:
        return 'Images Not Found!', 404
    view = 7 
    return render_template("u_final.html", view = view, pic=pic)
   
@app.route('/u_layout', methods = ['GET', 'POST'])
def u_layout():
    email = session['email']
    pic = Gallery.query.filter_by(email=email).all()
    if request.form['submit'] == 'xtra-large':
      view = 1
      return render_template('u_final.html', view=view, pic=pic) 
    if request.form['submit'] == 'large':
      view = 2
      return render_template('u_final.html', view=view, pic=pic)
    if request.form['submit'] == 'medium':
      view = 3
      return render_template('u_final.html', view=view, pic=pic) 
    if request.form['submit'] == 'small':
      view = 4
      return render_template('u_final.html', view=view, pic=pic) 
    if request.form['submit'] == 'list':
      view = 5
      return render_template('u_final.html', view=view, pic=pic)
    if request.form['submit'] == 'details':
      view = 6
      return render_template('u_final.html', view=view, pic=pic)
    if request.form['submit'] == 'default':
      view = 7
      return render_template('u_final.html', view=view, pic=pic)

@app.route('/u_remove',  methods=['GET', 'POST'])
def u_remove():
        dl = request.form['remove']
        img = Gallery.query.filter_by(email=session['email'], title=dl).first()
        if img is None:
            return 'No such memo, does nto exist!', 400
        session.pop(dl, None)
        print(session)
        db.session.delete(img)
        db.session.commit()
        db.session.close()
        msg= " "+dl+"memory, successfully deletd"
        reply = 4
        return render_template("u_loggedin.html", reply = reply, msg = msg)
    
@app.route('/u_edit')
def u_edit():
   return render_template('u_loggedin.html')

@app.route('/u_profile', methods = ['GET', 'POST'])
def u_profile():
    sign = 4
    email=session['email']
    profile=User.query.filter_by(email=email).first()
    return render_template('u_loggedin.html', sign = sign, profile=profile)  

@app.route('/cyba_tech')
def u_tech():
    return render_template('tech.html') 

@app.route('/services')
def u_services():
   return render_template('services.html')

@app.route('/about')
def u_about():
   return render_template('about.html')

@app.route('/u_logout')
def u_logout():
   session.pop('email', None)
   session.clear()
   return redirect(url_for('home'))


@app.route('/index')
def index():
    if 'email' in session:
        email = session['email']
        return render_template(
            'loggedin.html',
            username=email)
    return login()

@app.route('/signin', methods = ['GET', 'POST'])
def signin():
    sign = 2
    return render_template('index.html', sign = sign) 
  
@app.route('/signup', methods = ['GET', 'POST'])
def signup():
    if request.method == "POST":
        flash("Lets get started")
        return redirect(url_for('register')) 
    return render_template('register.html')  

@app.route('/login', methods = ['GET', 'POST'])
def login():
   if request.method == 'POST':
      email = request.form['email']
      password = request.form['pwd']
      data=Customers.query.filter_by(email=email, password=password).first()
      
      if email == "sa@hotmail.com" and password == "marek":
        return render_template("admin.html")
      elif data is None:
        ms = "wrong login details or user does not exist!"
        return render_template('index.html', ms = ms)
      else:
        session['email'] = request.form['email']
        if session['email'] is not None:
            front=Hairstyles.query.filter_by().all()
        return render_template('loggedin.html', front=front)
   front=Hairstyles.query.filter_by().all()
   return render_template('index.html', front=front)

@app.route('/register', methods = ['GET', 'POST'])
def register():
    data = ""
    if request.method == 'POST':
        create() 
    masg = "Sign In with your new account :)"
    sim = 4
    sign = 2
    return render_template('index.html', sign = sign, masg=masg, sim = sim) 

@app.route('/option', methods = ['GET', 'POST'])
def option():
    if request.form['submit'] == 'CUSTOMERS':
      return customers()
    if request.form['submit'] == 'EMPLOYEES':
      view = 2
      accounts = employees()
      return render_template('admin.html', view=view, accounts = accounts) 
    if request.form['submit'] == 'HISTORY':
      view = 3
      accounts = transactions()
      return render_template('admin.html', view=view, accounts = accounts) 
    if request.form['submit'] == 'HAIRSTYLES':
      styles=hairstyles()
      view=4
      return render_template("admin.html", styles=styles, view=view)
    if request.form['submit'] == 'LOG OUT':
      return logout()

@app.route('/c_buttons', methods = ['GET', 'POST'])
def c_buttons():
    if request.form['submit'] == 'create':
      show = 2
      return render_template('admin.html', show = show) 
    if request.form['submit'] == 'update':
      show = 4
      view = 1
      accounts = clients()
      return render_template('admin.html', show = show, view=view, accounts = accounts)  
    if request.form['submit'] == 'delete':
      show=8
      view=1
      accounts = clients()
      return render_template('admin.html', show = show, view=view, accounts = accounts) 

@app.route('/e_buttons', methods = ['GET', 'POST'])
def e_buttons():
    if request.form['submit'] == 'create':
      send=5
      return render_template('admin.html', send=send) 
    if request.form['submit'] == 'update':
      send=7
      view=2
      accounts = employees()
      return render_template('admin.html', send=send, view=view, accounts = accounts)  
    if request.form['submit'] == 'delete':
      send=9
      view=2
      accounts = employees()
      return render_template('admin.html', send=send,view=view,accounts = accounts) 

@app.route('/h_buttons', methods = ['GET', 'POST'])
def h_buttons():
    if request.form['submit'] == 'add':
      peek=1
      return render_template('admin.html', peek=peek) 
    if request.form['submit'] == 'append':
      peek=2
      view=4
      styles = hairstyles()
      return render_template('admin.html', peek=peek, view=view, styles=styles)  
    if request.form['submit'] == 'delete':
      peek=3
      view=4
      styles = hairstyles()
      return render_template('admin.html', peek=peek, view=view, styles = styles) 

@app.route('/crud', methods=['GET', 'POST'])
def crud():
    if request.form['submit'] == 'create':
        create()
        return customers() 
    if request.form['submit'] == 'execute':
        excute()
        return customers()
    if request.form['submit'] == 'update':
        update()
        accounts=employees()
        view=2
        return render_template("admin.html", view=view, accounts=accounts)
    if request.form['submit'] == 'insert':
        insert()
        accounts=employees()
        view=2
        return render_template("admin.html", view=view, accounts=accounts)
    if request.form['submit'] == 'eradicate':
        eradicate()
        accounts=employees()
        view=2
        return render_template("admin.html", view=view, accounts=accounts)    
    if request.form['submit'] == 'delete':
        delete()
        return customers()
    if request.form['submit'] == 'erase':
        erase()
        return logout()
    if request.form['submit'] == 'modify':
        modify()
        sign = 4
        ms="personal details successfully modified"
        profile=Customers.query.filter_by(email=session['email']).first()
        return render_template('final.html', sign = sign, profile=profile, ms=ms) 
    if request.form['submit'] == 'change':
        c_password()
        ms="password changed!"
        sign = 4
        profile=Customers.query.filter_by(email=session['email']).first()
        return render_template('final.html', sign = sign, profile=profile, ms=ms) 

@app.route('/load', methods=['GET', 'POST'])
def load():
    if request.form['submit'] == 'add':
        add()
        styles=hairstyles() 
        view=4
        return render_template("admin.html", view=view, styles=styles)
    if request.form['submit'] == 'append':
        append()
        styles=hairstyles() 
        view=4
        return render_template("admin.html", view=view, styles=styles)
    if request.form['submit'] == 'delete':
        clear()
        styles=hairstyles() 
        view=4
        return render_template("admin.html", view=view, styles=styles)

def customers():  
    db = lit.connect('Final Modification/Users.db')
    with db:
      cur = db.cursor()
      selectquery = "SELECT * FROM Customers"
      cur.execute(selectquery)
      accounts = cur.fetchall()
      view=1
    return render_template('admin.html', view=view, accounts = accounts)

def clients():  
    db = lit.connect('Final Modification/Users.db')
    with db:
      cur = db.cursor()
      selectquery = "SELECT * FROM Customers"
      cur.execute(selectquery)
      accounts = cur.fetchall()
    return accounts

def employees():  
    db = lit.connect('Final Modification/Users.db')
    with db:
      cur = db.cursor()
      selectquery = "SELECT * FROM Employees"
      cur.execute(selectquery)
      accounts = cur.fetchall()
    return accounts

def transactions():  
    db = lit.connect('Final Modification/Users.db')
    with db:
      cur = db.cursor()
      selectquery = "SELECT * FROM Appointments"
      cur.execute(selectquery)
      accounts = cur.fetchall()
    return accounts

def hairstyles():  
    db = lit.connect('Final Modification/Users.db')
    with db:
      cur = db.cursor()
      selectquery = "SELECT * FROM Hairstyles"
      cur.execute(selectquery)
      styles = cur.fetchall()
    return styles

def create():
        name = request.form['name']
        surname = request.form['surname']
        email = request.form['email']
        telephone = request.form['telephone']
        password = request.form['password']
        new_user = Customers(name=name, surname=surname, email=email, telephone=telephone, password=password)
        db.session.add(new_user)
        db.session.commit()
        db.session.close()
        print("new row inserted!")

def insert():
        name = request.form['name']
        surname = request.form['surname']
        mail = request.form['mail']
        address = request.form['address']
        saloon = request.form['saloon']
        num = request.form['num']
        telephone = request.form['telephone']
        new_user = Employees(name=name, surname=surname, mail=mail, address=address, saloon=saloon, table_number=num, telephone=telephone)
        db.session.add(new_user)
        db.session.commit()
        db.session.close()
        return "done!"

def add():
    f = request.files['file']
    new_filename = uuid.uuid1()
    _, ext = os.path.splitext(f.filename)
    if f is None:
        return 'No pic uploaded!', 400
    if id not in session: 
        f.save('Final Modification/static/gallery/%s%s' % (new_filename, ext))
        code =  str(new_filename)+ext
        filename = secure_filename(f.filename)
        mimetype = f.mimetype
        if not filename or not mimetype:
            return 'Bad upload!', 400
        name = request.form['name']
        price= request.form['price']
        ran=Hairstyles(name=name, code_name=code, price=price)
        db.session.add(ran)
        db.session.commit()
        db.session.close()
        return "done!"

def append():
    f = request.files['file']
    id = request.form['id']
    new_filename = uuid.uuid1()
    _, ext = os.path.splitext(f.filename)
    if f is None:
        return 'No pic uploaded!', 400
    if id not in session: 
        f.save('Final Modification/static/gallery/%s%s' % (new_filename, ext))
        code =  str(new_filename)+ext
        filename = secure_filename(f.filename)
        mimetype = f.mimetype
        if not filename or not mimetype:
            return 'Bad upload!', 400
        query=Hairstyles.query.filter_by(id=id).first()  
        query.name = request.form['name']
        query.code_name = code
        query.price = request.form['price']
        db.session.commit()
        db.session.close()
        return "done!"

def clear():
        id= request.form['id']
        old=Hairstyles.query.filter_by(id=id).first() 
        db.session.delete(old)
        db.session.commit()
        db.session.close()
        print("row deleted!")

def c_password():
    email=session['email']
    query=Customers.query.filter_by(email = email).first() 
    password = request.form['psw']
    pwd = request.form['pwd']
    if password == pwd:
       query.password = pwd
       db.session.commit()
       db.session.close()
       sn="Password changed successfully"
       return render_template("loggedin.html", sn=sn)
    else:
       return "Failed to change password"

def modify():
    if request.method == "POST":
        new_email=request.form['email']
        query=Customers.query.filter_by(email=session['email']).first()  
        query.name = request.form['name']
        query.surname = request.form['surname']
        query.telephone = request.form['telephone']
        query.email = new_email
        db.session.commit()
        db.session.close()
        session.pop('email', None)
        session['email']=new_email
    flash("Update successful")

def update():
    if request.method == "POST":
        id=request.form['id']
        query=Employees.query.filter_by(id=id).first()  
        if query is None:
            flash("Account doesn't exist!")
        else:
           query.name = request.form['name']
           query.surname = request.form['surname']
           query.mail = request.form['mail'] 
           query.address = request.form['address']
           query.saloon = request.form['saloon']
           query.num = request.form['num']
           query.telephone = request.form['telephone']
           db.session.commit()
           db.session.close()
           flash("Update successful")
    print("done!")

def excute():
    if request.method == "POST":
        id = request.form['id']
        query=Customers.query.filter_by(id=id).first()  
        query.name = request.form['name']
        query.surname = request.form['surname']
        query.telephone = request.form['telephone']
        query.email = request.form['email']
        db.session.commit()
        db.session.close()
    flash("Update successful")

@app.route("/delete", methods = ["POST", "GET"])
def delete():
    if request.method == "POST":
        id = request.form['id'] 
        query=Customers.query.filter_by(id = id).first()
        db.session.delete(query)
        db.session.commit()
        db.session.close()
        return "Deleted successfully" 

def eradicate():
    if request.method == "POST":
        id = request.form['id'] 
        query=Employees.query.filter_by(id = id).first()
        db.session.delete(query)
        db.session.commit()
        db.session.close()
        return "Deleted successfully" 

def range():
    x=db.session.query(Employees).count()
    x+=1
    n = random.randint(1,x)
    return n

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    f = request.files['file']
    new_filename = uuid.uuid1()
    _, ext = os.path.splitext(f.filename)
    
    if request.form['submit'] == 'book':
        if f is None:
            return 'No pic uploaded!', 400
        if id not in session: 
            f.save('Final Modification/static/gallery/%s%s' % (new_filename, ext))
            session['img'] =  str(new_filename)+ext
            filename = secure_filename(f.filename)
            mimetype = f.mimetype
            msg = "successfully booked : )"
            if not filename or not mimetype:
                return 'Bad upload!', 400
            n=range()
            trans=Appointments(employee_id=n, cemail=session['email'], date_booked=request.form['date'], image=filename, mimetype=mimetype, picode=session['img'], style=request.form['style'])
            db.session.add(trans)
            db.session.commit()
            db.session.close()
            reply = 2
        return render_template("loggedin.html", msg = msg, reply=reply)

    if request.form['submit'] == 'history':
        emp = Appointments.query.filter_by(cemail=session['email']).all()
        view=3
        if emp == []:
            return 'No History of Bookings Yet!'+"<br><a href = '/back'>" + "back</a>", 404     
        else:
          print(emp)
          return render_template("final.html", emp=emp, view=view)
    
    if request.form['submit'] == 'check':
        return check_order()

def check_order():
    email = session['email']
    apt = Appointments.query.filter_by(cemail=email).first()
    if apt is not None:
        try:
            num=apt.employee_id 
            emp = Employees.query.filter_by(id=num).first()
            view=2      
            return render_template("final.html", emp=emp, apt=apt.date_booked, view=view)
        except:
            return 'No Bookings Yet!'+"<br><a href = '/back'>" + "back</a>", 404
   
    if apt is None:
        return 'No Bookings Yet!'+"<br><a href = '/back'>" + "back</a>", 404
    
@app.route('/cancel',  methods=['GET', 'POST'])
def cancel():
        apt = Appointments.query.filter_by(cemail=session['email']).first()
        if apt is None:
            return 'No booking, does not exist!', 400
        db.session.delete(apt)
        db.session.commit()
        db.session.close()
        msg="booking successfully canceled"
        return render_template("final.html", msg = msg)
    
@app.route('/back')
def back():
    front=Hairstyles.query.filter_by().all()
    return render_template('loggedin.html', front=front)

@app.route('/profile', methods = ['GET', 'POST'])
def profile():
    sign = 4
    profile=Customers.query.filter_by(email=session['email']).first()
    return render_template('final.html', sign = sign, profile=profile) 

def erase():
    if request.method == "POST":
        email = session['email'] 
        query=Customers.query.filter_by(email=email).first()
        db.session.delete(query)
        db.session.commit()
        db.session.close()
        return "Deleted successfully" 

@app.route('/logout')
def logout():
   session.pop('email', None)
   print(session)
   return redirect(url_for('index'))

if __name__ == '__main__':
   app.run(debug = True)

   