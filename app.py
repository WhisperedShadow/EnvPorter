from flask import Flask, render_template, request, redirect, url_for, flash, Response
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from database import db, User, KeyBase, Keys
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

app.config['SECRET_KEY'] = "Arandomsecretkey"
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("SQL_LINK")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message = 'You need to be logged in to access this page'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('index'))
        else:
            flash('Invalid username or password')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        
        if User.query.filter_by(username=username).first():
            flash('User already exists')
        else:
            new_user = User(
                username=username, 
                email=email, 
                password=generate_password_hash(password, method='pbkdf2:sha256')
            )
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/')
@login_required
def index():
    return render_template('index.html', bases=KeyBase.query.filter_by(user_id=current_user.id).all())

@app.route('/new', methods=['GET', 'POST'])
@login_required
def new():
    if request.method == 'POST':
        category = request.form.get('category')
        
        if not category:
            flash("Category is required")
            return redirect(url_for('new'))
        
        new_base = KeyBase(base_name=category, user_id=current_user.id)
        db.session.add(new_base)
        db.session.commit()  

        for key, value in request.form.items():
            if key.startswith("key") and value:
                index = key[3:]  
                keyname = value
                keyvalue = request.form.get(f'value{index}')
                
                if keyvalue: 
                    new_key = Keys(base_id=new_base.base_id, keyname=keyname, key=keyvalue)
                    db.session.add(new_key)

        db.session.commit()  
        return redirect(url_for('index'))
        
    return render_template('new.html')

@app.route('/remove/<int:base_id>')
@login_required
def deletebase(base_id):
    base = KeyBase.query.get_or_404(base_id) 
    Keys.query.filter_by(base_id=base_id).delete()
    db.session.delete(base)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/edit/<int:base_id>', methods=['GET', 'POST'])
@login_required
def edit(base_id):
    base = KeyBase.query.get_or_404(base_id)
    keys = Keys.query.filter_by(base_id=base_id).all()

    if request.method == 'POST':
        category = request.form.get('category')
        
        if not category:
            flash("Category is required")
            return redirect(url_for('edit', base_id=base_id))
        
        base.base_name = category
        db.session.commit()

        existing_keys = {k.keyname: k for k in keys}

        new_keys = {}
        for key, value in request.form.items():
            if key.startswith("key") and value:
                index = key[3:]  
                keyname = value
                keyvalue = request.form.get(f'value{index}')
                
                if keyvalue:
                    new_keys[keyname] = keyvalue
        for existing_keyname in list(existing_keys.keys()):
            if existing_keyname not in new_keys:
                db.session.delete(existing_keys[existing_keyname])

        for keyname, keyvalue in new_keys.items():
            if keyname in existing_keys:
                existing_keys[keyname].key = keyvalue
            else:
                db.session.add(Keys(base_id=base.base_id, keyname=keyname, key=keyvalue))

        db.session.commit()
        return redirect(url_for('index'))
        
    return render_template('edit.html', base=base, keys=keys)

if __name__ == '__main__':
    app.run(debug=True)
