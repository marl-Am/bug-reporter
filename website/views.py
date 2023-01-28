from flask import Blueprint, flash, redirect, render_template, request, url_for, jsonify
from flask_login import current_user, login_required
from werkzeug.security import generate_password_hash

from website.models import Project, Task, User

from . import db

views = Blueprint('views', __name__)


@views.route('/', endpoint='index')
def base():
    return render_template('index.html')


@views.route('/user_dashboard/')
@login_required
def user_dashboard():
    projects = db.session.query(Project).filter_by(
        user_id=current_user.id).all()
    return render_template('user_dashboard.html', user=current_user, projects=projects)


@views.route('/edit_project', methods=['GET', 'POST'])
@login_required
def edit_project():
    if request.method == 'GET':
        project_id = request.args.get("project_id")
        project = Project.query.filter_by(id=project_id).first()
        if not project:
            flash('(GET) Project not found.', 'error')
            return redirect(url_for('views.user_dashboard'))
        return render_template('edit_project.html', project=project)

    if request.method == 'POST':
        project_id = request.form.get("project_id")
        project = Project.query.filter_by(id=project_id).first()
        if not project:
            flash('(POST) Project not found.', 'error')
            return redirect(url_for('views.user_dashboard'))

        if project.user_id != current_user.id:
            flash('You are not authorized to edit this project.', 'error')
            return redirect(url_for('views.user_dashboard'))

        # Get the form data
        title = request.form.get("title")
        content = request.form.get("content")
        status = request.form.get("status")
        # Update the fields of the project
        project.title = title
        project.content = content
        project.status = status
        # Save the changes to the database
        db.session.commit()
        flash('Project details updated successfully.', 'success')
        return redirect(url_for('views.user_dashboard'))


@views.route('/delete_project', methods=["POST"])
@login_required
def delete_project():
    project_id = request.form.get("project_id")
    project_to_delete = Project.query.filter_by(id=project_id).first()
    tasks_to_delete = Task.query.filter_by(project_id=project_id).all()
    for task in tasks_to_delete:
        db.session.delete(task)

    db.session.delete(project_to_delete)
    db.session.commit()
    flash('Project deleted.', 'success')
    return redirect(url_for('views.user_dashboard'))


@views.route('/new_project', methods=['GET', 'POST'])
@login_required
def new_project():
    if request.method == 'POST':
        title = request.form.get("title")
        content = request.form.get("content")
        new_project = Project(user_id=current_user.id,
                              title=title, content=content, status="Open")
        if not new_project:
            flash('Project not created.', 'error')
        else:
            db.session.add(new_project)
            db.session.commit()
            flash('Project created successfully.', 'success')
            return redirect(url_for('views.user_dashboard'))
    return render_template('new_project.html')


@views.route('/view_project/<int:project_id>')
def view_project(project_id):
    project = Project.query.filter_by(id=project_id).first()
    tasks = Task.query.filter_by(project_id=project_id).all()
    return render_template('view_project.html', project=project, tasks=tasks)


@views.route('/delete_task', methods=["POST"])
@login_required
def delete_task():
    task_id = request.form.get("task_id")
    task = Task.query.filter_by(id=task_id).first()
    project_id = task.project_id
    db.session.delete(task)
    db.session.commit()
    flash('Task deleted.', 'success')
    return redirect(url_for('views.view_project', project_id=project_id))


@views.route('/edit_task', methods=["GET", "POST"])
@login_required
def edit_task():
    if request.method == 'GET':
        task_id = request.args.get("task_id")
        task = Task.query.filter_by(id=task_id).first()
        if not task:
            project = Project.query.filter_by(user_id=current_user.id).first()
            project_id = project.id
            flash('(GET) Task not found.', 'error')
            return redirect(url_for('views.view_project', project_id=project_id))
        return render_template('edit_task.html', task=task)

    if request.method == "POST":
        task_id = request.form.get("task_id")
        task = Task.query.filter_by(id=task_id).first()
        if not task:
            project = Project.query.filter_by(user_id=current_user.id).first()
            project_id = project.id
            flash('(POST) Task not found.', 'error')
            return redirect(url_for('views.view_project', project_id=project_id))

        title = request.form.get("title")
        content = request.form.get("content")
        status = request.form.get("status")

        task.title = title
        task.content = content
        task.status = status
        db.session.commit()
        flash('Task updated.', 'success')
        return redirect(url_for('views.view_project', project_id=task.project_id))


@views.route('/new_task', methods=['GET', 'POST'])
@login_required
def new_task():
    if request.method == 'GET':
        return render_template('new_task.html')
    if request.method == 'POST':
        title = request.form.get("title")
        content = request.form.get("content")

        project = Project.query.filter_by(user_id=current_user.id).first()
        project_id = project.id
        if not project:
            flash('Project id not found.', 'error')
            return redirect(url_for('views.view_project', project_id=project_id))

        task = Task(project_id=project.id, title=title,
                    content=content, status="Open")
        if not task:
            flash('Task creation failed.', 'error')
            return redirect(url_for('views.view_project', project_id=project_id))

        db.session.add(task)
        db.session.commit()
        flash('Task creation successful.', 'success')
        return redirect(url_for('views.view_project', project_id=project_id))


@views.route('/user_details', methods=['GET'])
@login_required
def user_details():
    return render_template('user_details.html', user=current_user)


@views.route("/update_user_details", methods=['POST'])
@login_required
def update_user_details():
    if request.method == 'POST':
        # Get the form data
        email = request.form.get("email")
        password = request.form.get("password")

        # Retrieve the current user object
        from flask_login import current_user

        if not current_user:
            flash('Update details failed.', 'error')
            return redirect(url_for('views.user_details'))

        # Update the email and password fields
        current_user.email = email
        current_user.password = generate_password_hash(
            password, method='sha256')

        # Commit the changes to the database
        db.session.commit()

        flash('User updated.', 'success')
        return redirect(url_for('views.user_details'))


@views.route('/project_details', methods=['GET', 'POST'])
@login_required
def project_details():
    projects = db.session.query(Project).filter_by(
        user_id=current_user.id).all()
    return render_template('project_details.html', projects=projects)


# Invalid URL
@views.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404


# Internal Server Error
@views.errorhandler(500)
def page_not_found(e):
    return render_template("500.html"), 500
