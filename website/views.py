from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user

views = Blueprint('views', __name__)

@views.route('/', endpoint='index')
def base():
    return render_template('index.html')


@views.route('/user')
# @login_required
def user():
    return render_template('user_dashboard.html', user=current_user)


@views.route('/edit_project', methods=['GET', 'POST'])
def edit_project():
    if request.method == 'POST':
        error = True
        print("Edit project...")
        if error:
            print("Error editing project...")
        else:
            flash('Editing project successful')
            return redirect(url_for('views.user'))
    return render_template('edit_project.html')


@views.route('/delete_project', methods=["POST"])
def delete_project():
    if request.method == 'POST':
        error = True
        print("Edit project...")
        if error:
            print("Error deleting project...")
        else:
            flash('Deleting project successful')
            return redirect(url_for('views.user'))


@views.route('/new_project', methods=['GET', 'POST'])
def new_project():
    if request.method == 'POST':
        error = True
        if error:
            print("Error making new project...")
        else:
            flash('New project made successfully')
            return redirect(url_for('views.user'))
    return render_template('new_project.html')


@views.route('/edit_task', methods=['GET', 'POST'])
def edit_task():
    if request.method == 'POST':
        print("Edit task...")
    return render_template('edit_task.html')


@views.route('/new_task', methods=['GET', 'POST'])
def new_task():
    if request.method == 'POST':
        error = True
        if error:
            print("Error editing task...")
        else:
            flash('Editing task successful')
            return redirect(url_for('views.user'))
    return render_template('new_task.html')


@views.route('/user_details', methods=['GET'])
def user_details():
    return render_template('user_details.html')


@views.route("/update_user_details", methods=["POST"])
def update_user_details():
    # Get the form data
    email = request.form.get("email")
    password = request.form.get("password")
    error = True
    if error:
        print("Error updating user details...")
    else:
        flash('Updated user details successfully')
        return redirect(url_for('views.user_details'))


@views.route('/project_details', methods=['GET', 'POST'])
def project_details():
    if request.method == 'POST':
        error = True
        if error:
            print("Error updating project details...")
        else:
            flash('Updated project details successfully')
            return redirect(url_for('views.project_details'))
    return render_template('project_details.html')
