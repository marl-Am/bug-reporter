from flask import Blueprint, flash, jsonify, redirect, render_template, request, url_for, jsonify
from flask_login import current_user, login_required
import json

from website.models import Project, Task

from . import db

views = Blueprint('views', __name__)


@views.route('/', endpoint='index')
def base():
    return render_template('index.html')


@views.route('/user_dashboard')
@login_required
def user_dashboard():
    projects = db.session.query(Project).filter_by(
        user_id=current_user.id).all()
    return render_template('user_dashboard.html', user=current_user, projects=projects)


# @views.route('/edit_project', methods=['GET', 'POST'])
# @login_required
# def edit_project():
#     project_id = request.args.get("project_id")
#     project = Project.query.filter_by(id=project_id).first()
#     if request.method == 'POST':
#         if not project:
#             flash('Project not found.', 'error')
#             return redirect(url_for('views.user_dashboard'))
#         else:
#             # Get the form data
#             title = request.form.get("title")
#             content = request.form.get("content")
#             status = request.form.get("status")
#             # Update the fields of the project
#             project.title = title
#             project.content = content
#             project.status = status
#             # Save the changes to the database
#             db.session.commit()
#             flash('Project details updated successfully.', 'success')
#             return redirect(url_for('views.user_dashboard'))
#     if request.method == 'GET':
#         return render_template('edit_project.html', project=project)

@views.route('/edit_project', methods=['GET', 'POST'])
@login_required
def edit_project():
    if request.method == 'GET':
        project_id = request.args.get("project_id")
        project = Project.query.filter_by(id=project_id).first()
        if not project:
            flash('(GET) Project not found.', 'error')
            return redirect(url_for('views.user_dashboard'))
        print(f'GET project_id = {project_id}')
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
    project = Project.query.filter_by(id=project_id).first()
    db.session.delete(project)
    db.session.commit()
    flash("Project deleted.")
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


@views.route('/delete_task', methods=["POST"])
@login_required
def delete_task():
    task = json.loads(request.data)
    taskId = task['taskId']
    task = Task.query.get(taskId)
    if task:
        if task.project_id == current_user.id:
            db.session.delete(task)
            db.session.commit()
    return jsonify({})


@views.route('/edit_task', methods=['GET', 'POST'])
@login_required
def edit_task():
    if request.method == 'POST':
        # Get the form data
        title = request.form.get("title")
        content = request.form.get("content")

        # Update the Task's details
        current_user.title = title
        current_user.content = content
        db.session.commit()

        flash("Task details updated successfully.")
        return redirect(url_for('views.user_dashboard'))
    return render_template('edit_task.html')


@views.route('/new_task', methods=['GET', 'POST'])
@login_required
def new_task():
    if request.method == 'POST':
        title = request.form.get("title")
        content = request.form.get("content")
        new_task = Task(project_id=current_user.id, title=title,
                        content=content, status="Open")
        if not new_task:
            flash('Task not created.', 'error')
        else:
            db.session.add(new_task)
            db.session.commit()
            flash('Task created successfully.', 'success')
            return redirect(url_for('views.user_dashboard'))
    return render_template('new_task.html')


@views.route('/view_tasks', methods=['GET', 'POST'])
@login_required
def view_tasks():
    if request.method == 'GET':
        return render_template('view_tasks.html')
    if request.method == 'POST':
        print("Posting tasks...")


@views.route('/user_details', methods=['GET'])
@login_required
def user_details():
    return render_template('user_details.html')


@views.route("/update_user_details", methods=["POST"])
@login_required
def update_user_details():
    if request.method == "POST":
        # Get the form data
        email = request.form.get("email")
        password = request.form.get("password")

        # Update the User's details
        current_user.email = email
        current_user.password = password
        db.session.commit()

        flash("User details updated successfully.")
        return redirect(url_for('views.update_user_details'))
    return redirect(url_for("views.dashboard"))


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
