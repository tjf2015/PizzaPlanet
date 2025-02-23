from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint('auth',__name__)
req = request



@auth.route('/login', methods=['GET', 'POST'])
def login():
    if req.method == 'POST':
        email = req.form.get('email')
        password = req.form.get('password')
        
        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                # flash('Loggend in Successfully',category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.manage_pizza'))
            else:
                flash('Incorrect Password, please try again', category='error')
                return render_template('login.html')
        else:
            flash('Email does not exist.', category='error')
            return render_template('signup.html')        
    else:
        return render_template('login.html')

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('views.home'))

@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = req.form.get('name')
        email = req.form.get('email')
        password1 = req.form.get('password1')
        password2 = req.form.get('password2')
        is_owner_str = req.form.get('is_owner')  # Expect "true" or "false"
        is_owner = True if is_owner_str == "true" else False

        if len(email) < 4:
            flash('Email must be greater than 4 characters.', category='error')
        elif len(name) < 2:
            flash('Name must be greater than 1 character.', category='error')
        elif password1 != password2:
            flash("Passwords don't match.", category='error')
        elif len(password1) < 7:
            flash('Password must be longer than 7 characters.', category='error')
        else:
            new_user = User(
                name=name,
                email=email,
                password=generate_password_hash(password1, method='pbkdf2:sha256'),
                is_owner=is_owner
            )
            print('*************before add user to db************')
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            # Redirect based on user role:
            if new_user.is_owner:
                return redirect(url_for('views.manage_pizza'))
            else:
                return redirect(url_for('views.create_pizza'))
        return redirect(url_for('auth.signup'))
    return render_template('signup.html')
   