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


def getUserName():
    user_info = db.session.query(User).filter(
        User.user_email == request.form['user_email']).first()
    userName = user_info.user_name
    session['user_id'] = user_info.id
    return userName


def createUser(user_name, user_email, user_password, user_phone, user_address):
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
        user_info = db.session.query(User).filter(
            User.user_email == user_email).first()
        userName = user_info.user_name
        # Tao session
        session['user_id'] = user_info.id
        return userName


def get_user_info(user_id):
    user_info = db.session.query(User).filter(User.id == user_id).first()
    data = user_info.__dict__
    return user_info


def get_all_user():
    result = []
    user_list = db.session.query(User).all()
    for user in user_list:
        result.append(user.__dict__)
    return result


@app.route('/', methods=['GET'])
def home():
    if request.method == "GET":
        return render_template('login.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "GET":
        return render_template('login.html')
    if request.method == 'POST':
        # Xac minh user email va password
        if valid_login(request.form['user_email'], request.form['user_password']):
            userName = getUserName()
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
            userName = createUser(user_name, user_email,
                                  user_password, user_phone, user_address)
            return render_template('logedIn.html', userName=userName)


@app.route('/admin', methods=['GET', 'POST', 'PUT', 'DELETE'])
def admin():
    current_user_info = db.session.query(User).filter(
        User.id == session['user_id']).first()
    if current_user_info.is_admin == True:
        if request.method == "GET":
            # Hien thi thong tin chi tiet cua user theo id
            user_id = request.args.get("user_id")
            if user_id:
                user_info = get_user_info(user_id)
                if user_info:
                    return render_template('user_info.html', user=user_info)
            # Lay ra tat ca user
            all_user_info = get_all_user()
            return render_template('admin.html', user_list=all_user_info)
    else:
        return render_template('restricted.html')


@app.route('/logout', methods=['GET'])
def logout():
    # Xoa session
    session.pop('user_id', None)
    return render_template('login.html')


if __name__ == '__main__':
    app.init_db()
    app.run(debug=True)
