from flask import Flask, flash, redirect, render_template, request, url_for
from flask_login import LoginManager, UserMixin, current_user, login_required, login_user, logout_user
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
from werkzeug.security import generate_password_hash, check_password_hash
from env import SECRET_KEY, SQLALCHEMY_DATABASE_URI

app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
app.config['SECRET_KEY'] = SECRET_KEY

db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Authenticate


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        flash('You are already registered.', 'success')
        return redirect(url_for('user_dashboard'))
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        retype_password = request.form.get('retype_password')
        if ((len(email) < 7 or len(email) > 30) or (len(password) < 7 or len(password) > 30)):
            flash('Input should be between 7 and 30 characters.', category='error')
            return redirect(url_for('user_dashboard'))

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
            return redirect(url_for('user_dashboard'))
    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        flash('You are already logged in.', 'success')
        return redirect(url_for('user_dashboard'))
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in successfully!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('user_dashboard'))
            else:
                flash('Incorrect password.', category='error')
        else:
            flash('Account does not exist.', category='error')

    return render_template('login.html')


@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    flash('Logged out.', category='success')
    return redirect(url_for('login'))


@app.route('/delete_account/<int:id>', methods=['POST'])
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
        return redirect(url_for('login'))
    else:
        flash('Sorry, you can not delete that user!', 'error')
        return redirect(url_for('user_details'))

# Authenticate ends

# Views
@app.route('/', endpoint='index')
def base():
    return render_template('index.html')


@app.route('/user_dashboard/')
@login_required
def user_dashboard():
    projects = db.session.query(Project).filter_by(
        user_id=current_user.id).all()
    return render_template('user_dashboard.html', user=current_user, projects=projects)


@app.route('/edit_project', methods=['GET', 'POST'])
@login_required
def edit_project():
    if request.method == 'GET':
        project_id = request.args.get("project_id")
        project = Project.query.filter_by(id=project_id).first()
        if not project:
            flash('(GET) Project not found.', 'error')
            return redirect(url_for('user_dashboard'))
        return render_template('edit_project.html', project=project)

    if request.method == 'POST':
        project_id = request.form.get("project_id")
        project = Project.query.filter_by(id=project_id).first()
        if not project:
            flash('(POST) Project not found.', 'error')
            return redirect(url_for('user_dashboard'))

        if project.user_id != current_user.id:
            flash('You are not authorized to edit this project.', 'error')
            return redirect(url_for('user_dashboard'))

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
        return redirect(url_for('user_dashboard'))


@app.route('/delete_project', methods=["POST"])
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
    return redirect(url_for('user_dashboard'))


@app.route('/new_project', methods=['GET', 'POST'])
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
            return redirect(url_for('user_dashboard'))
    return render_template('new_project.html')


@app.route('/view_project/<int:project_id>')
def view_project(project_id):
    project = Project.query.filter_by(id=project_id).first()
    tasks = Task.query.filter_by(project_id=project_id).all()
    return render_template('view_project.html', project=project, tasks=tasks)


@app.route('/delete_task', methods=["POST"])
@login_required
def delete_task():
    task_id = request.form.get("task_id")
    task = Task.query.filter_by(id=task_id).first()
    project_id = task.project_id
    db.session.delete(task)
    db.session.commit()
    flash('Task deleted.', 'success')
    return redirect(url_for('view_project', project_id=project_id))


@app.route('/edit_task', methods=["GET", "POST"])
@login_required
def edit_task():
    if request.method == 'GET':
        task_id = request.args.get("task_id")
        task = Task.query.filter_by(id=task_id).first()
        if not task:
            project = Project.query.filter_by(user_id=current_user.id).first()
            project_id = project.id
            flash('(GET) Task not found.', 'error')
            return redirect(url_for('view_project', project_id=project_id))
        return render_template('edit_task.html', task=task)

    if request.method == "POST":
        task_id = request.form.get("task_id")
        task = Task.query.filter_by(id=task_id).first()
        if not task:
            project = Project.query.filter_by(user_id=current_user.id).first()
            project_id = project.id
            flash('(POST) Task not found.', 'error')
            return redirect(url_for('view_project', project_id=project_id))

        title = request.form.get("title")
        content = request.form.get("content")
        status = request.form.get("status")

        task.title = title
        task.content = content
        task.status = status
        db.session.commit()
        flash('Task updated.', 'success')
        return redirect(url_for('view_project', project_id=task.project_id))


@app.route('/new_task', methods=['GET', 'POST'])
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
            return redirect(url_for('view_project', project_id=project_id))

        task = Task(project_id=project.id, title=title,
                    content=content, status="Open")
        if not task:
            flash('Task creation failed.', 'error')
            return redirect(url_for('view_project', project_id=project_id))

        db.session.add(task)
        db.session.commit()
        flash('Task creation successful.', 'success')
        return redirect(url_for('view_project', project_id=project_id))


@app.route('/user_details', methods=['GET'])
@login_required
def user_details():
    return render_template('user_details.html', user=current_user)


@app.route("/update_user_details", methods=['POST'])
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
            return redirect(url_for('user_details'))

        # Update the email and password fields
        current_user.email = email
        current_user.password = generate_password_hash(
            password, method='sha256')

        # Commit the changes to the database
        db.session.commit()

        flash('User updated.', 'success')
        return redirect(url_for('user_details'))


@app.route('/project_details', methods=['GET', 'POST'])
@login_required
def project_details():
    projects = db.session.query(Project).filter_by(
        user_id=current_user.id).all()
    return render_template('project_details.html', projects=projects)


# Invalid URL
@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404


# Internal Server Error
@app.errorhandler(500)
def page_not_found(e):
    return render_template("500.html"), 500
# Views ends


# Models
class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    title = db.Column(db.String(255))
    content = db.Column(db.Text)
    status = db.Column(db.String(255))
    created_on = db.Column(db.DateTime(timezone=True), default=func.now())
    # tasks = db.relationship('Task', backref='project', lazy=True)

    def __init__(self, user_id, title, content, status):
        self.user_id = user_id
        self.title = title
        self.content = content
        self.status = status


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'))
    title = db.Column(db.String(255))
    content = db.Column(db.Text)
    status = db.Column(db.String(255))
    created_on = db.Column(db.DateTime(timezone=True), default=func.now())


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    created_on = db.Column(db.DateTime(timezone=True), default=func.now())
    # projects = db.relationship('Project', backref='user', lazy=True)

# Models end

if __name__ == '__main__':
    app.run()
