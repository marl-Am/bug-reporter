from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash

from website.models import Project, Task, User
from . import db

auth = Blueprint('auth', __name__)


@auth.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        flash('You are already registered.', 'success')
        return redirect(url_for('views.user_dashboard'))
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        retype_password = request.form.get('retype_password')
        if ( (len(email) < 7 or len(email) > 30) or (len(password) < 7 or len(password) > 30) ):
            flash('Input should be between 7 and 30 characters.', category = 'error')
            return redirect(url_for('views.user_dashboard'))

        user = User.query.filter_by(email=email).first()
        if user:
            flash('Account already exists.', category='error')
        else:
            new_user = User(email=email, password=generate_password_hash(
                password, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('Account created!', category='success')
            return redirect(url_for('views.user_dashboard'))
    return render_template('register.html')


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        flash('You are already logged in.', 'success')
        return redirect(url_for('views.user_dashboard'))
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in successfully!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.user_dashboard'))
            else:
                flash('Incorrect password.', category='error')
        else:
            flash('Account does not exist.', category='error')

    return render_template('login.html')


@auth.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    flash('Logged out.', category='success')
    return redirect(url_for('auth.login'))


@auth.route('/delete_account/<int:id>', methods=['POST'])
@login_required
def delete_account(id):
    if id == current_user.id:
        user_to_delete = User.query.filter_by(id=current_user.id).first()
        projects_to_delete = Project.query.filter_by(user_id=current_user.id)
        tasks_to_delete = Task.query.filter_by(project_id=current_user.id)

        for task_to_delete in tasks_to_delete:
            db.session.delete(task_to_delete)
        for project_to_delete in projects_to_delete:
            db.session.delete(project_to_delete)
        db.session.delete(user_to_delete)
        db.session.commit()

        logout_user()
        flash('Account deleted.', 'success')
        return redirect(url_for('auth.login'))
    else:
        flash('Sorry, you can not delete that user!', 'error')
        return redirect(url_for('views.user_details'))
