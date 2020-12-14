# from models import user
# from models.user import db



import re
from flask.templating import render_template_string
from re import U
from flask import Flask, session
from flask import request
from werkzeug.utils import redirect
from flask_sqlalchemy import SQLAlchemy
from flask import render_template
from flask import request
import os

app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])
# app.config.from_object(os.environ['config'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
from models import user
from models.user import User

def init_db():
    db.init_app()
    db.app = app
    db.create_all()


# Ham xac minh email va password
def valid_login(user_email, password):
    print("Trong valid login")
    print("username password", user_email, password)
    user_record = db.session.query(User).filter(
        User.user_email == user_email).first()
    if user_record is None:
        return False
    else:
        valid_email = user_record.user_email
        valid_password = user_record.user_password
        if user_email == valid_email and password == valid_password:
            return True
        else:
            return False


@app.route('/', methods=['GET'])
def home():
    if request.method == "GET":
        return render_template('login.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "GET":
        return render_template('login.html')
    if request.method == 'POST':
        print("POST login")
        # Xac minh user email va password
        if valid_login(request.form['user_email'], request.form['user_password']):
            user_info = db.session.query(User).filter(User.user_email == request.form['user_email']).first()
            userName = user_info.user_name
            session['user_id'] = user_info.id
            return render_template('logedIn.html', userName=userName)
        else:
            return render_template('error.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == "GET":
        return render_template('register.html')
    if request.method == "POST":
        # Nhan data tu form
        user_name = request.form['user_name']
        user_email = request.form['user_email']
        user_password = request.form['user_password']
        user_phone = request.form['user_phone']
        user_address = request.form['user_address']

        if user_name is None or user_email is None or user_password is None:
            return render_template('error.html')
        else:
        # try:
            # Lay so luong user co trong database
            user_quantity = db.session.query(User).count()
            # Kiem tra input nhap vao (Khong duoc trung email voi tai khoan khac)
            duplicate_email_exists = db.session.query(
                User).filter(User.user_email == user_email).first()
            if duplicate_email_exists is not None:
                return render_template("error.html")
            # Neu khong trung email thi tao tai khoan
            else:
                new_user = User()
                # new_user.id = str(user_quantity + 1)
                new_user.user_address = user_address if user_address else None
                new_user.user_email = user_email
                new_user.user_name = user_name if user_name else "User" + \
                    str(user_quantity + 1)
                new_user.user_password = user_password
                new_user.user_phone = user_phone if user_phone else None
                # Luu vao db
                db.session.add(new_user)
                db.session.commit()
                user_info = db.session.query(User).filter(User.user_email == user_email).first()
                userName = user_info.user_name
                # Tao session 
                session['user_id'] = user_info.id
                return render_template('logedIn.html', userName=userName)

        # except Exception as e:
        #     return render_template('error.html')

@app.route('/admin', methods=['GET', 'POST','PUT' ,'DELETE'])
def admin():
    current_user_info = db.session.query(User).filter(User.id == session['user_id']).first()
    if current_user_info.is_admin == True:
        if request.method == "GET":
            # Lay ra tat ca user
            result = []
            user_list = db.session.query(User).all()
            for user in user_list:
                result.append(user.__dict__)
            return render_template('admin.html', user_list=result)
        if request.method == "PUT":
            # Chinh sua thong tin user
            user_id = request.args.get("user_id")
            new_name = request.form['user_name'] 
            new_email = request.form['user_email']
            new_phone = request.form['user_phone']
            new_address = request.form['user_address']

            user_info = db.session.query(User).filter(User.id == user_id).first()
            user_info.user_name = new_name
            user_info.user_email = new_email
            user_info.user_phone = new_phone
            user_info.user_address = new_address
            db.session.commit()
            
            return redirect("/admin")
    else:
        return render_template('restricted.html')

@app.route('/logout', methods=['GET', 'POST', 'DELETE'])
def logout():
    session.pop('user_id',None)
    return render_template('login.html')

if __name__ == '__main__':
    app.init_db()
    app.run(debug=True)
