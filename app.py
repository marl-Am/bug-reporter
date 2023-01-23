from flask import Flask, redirect, render_template, request, url_for

app = Flask(__name__)


class Project():
    def __init__(self, id, title, content, created_on):
        self.id = id
        self.title = title
        self.content = content
        self.complete_count = 0
        self.created_on = created_on
        self.finished_on = None
        self.status = 0
        self.tasks = []

    def add_tasks(self, tasks):
        self.tasks.append(tasks)

    def update_status(self):
        for task in self.tasks:
            if task.status == "Complete":
                self.complete_count += 1
        self.status = (self.complete_count / len(self.tasks)) * 100


class Tasks():
    def __init__(self, id, project_id, title, content, status, created_on, updated_on):
        self.id = id
        self.project_id = project_id
        self.title = title
        self.content = content
        self.status = status
        self.created_on = created_on
        self.updated_on = updated_on


class User():
    def __init__(self, id, email, password, created_on, updated_on):
        self.id = id
        self.email = email
        self.password = password
        self.created_on = created_on
        self.updated_on = updated_on


############# Display homepage #############
@app.route('/')
def index():
    return render_template('index.html')

 
############# Log in user #############
@app.route('/login', methods=['GET', 'POST'])
def login():
    # message = session.get('message', None)
    if request.method == 'POST':
        email = request.form.get("email")
        password = request.form.get("password")
        print("Login successful")
    return render_template('login.html')


############# Register user #############
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form.get("email")
        password = request.form.get("password")
        print("Registering...")
    return render_template('register.html')


############# Display user dashboard #############
@app.route('/user', methods=['GET', 'POST'])
def user():
    if request.method == 'POST':
        print("User...")
    return render_template('user_dashboard.html')


############# Project creation/edit #############
@app.route('/edit_project', methods=['GET', 'POST'])
def edit_project():
    if request.method == 'POST':
        print("Edit project...")
    return render_template('edit_project.html')


@app.route('/new_project', methods=['GET', 'POST'])
def new_project():
    if request.method == 'POST':
        print("New project...")
    return render_template('new_project.html')


############# Task creation/edit #############
@app.route('/edit_task', methods=['GET', 'POST'])
def edit_task():
    if request.method == 'POST':
        print("Edit task...")
    return render_template('edit_task.html')


@app.route('/new_task', methods=['GET', 'POST'])
def new_task():
    if request.method == 'POST':
        print("New task...")
    return render_template('new_task.html')


############# User details #############
@app.route('/user_details', methods=['GET', 'POST'])
def user_details():
    if request.method == 'POST':
        print("User details...")
    return render_template('user_details.html')


@app.route("/update_user_details", methods=["POST"])
def update_user_details():
    # Get the form data
    email = request.form.get("email")
    password = request.form.get("password")
    retype_password = request.form.get("retype-password")

    # Perform the necessary actions
    # ...

    return redirect(url_for("user_details"))
############# User details ends #############


############# Project details #############
@app.route('/project_details', methods=['GET', 'POST'])
def project_details():
    if request.method == 'POST':
        print("Project details...")
    return render_template('project_details.html')

############# Project details ends #############

if __name__ == "__main__":
    app.run(debug=True)
