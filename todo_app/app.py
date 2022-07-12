from flask import Flask, render_template, request, redirect, url_for

from todo_app.data.session_tasks import get_tasks, add_task, get_task, save_task, delete_task, toggle
from todo_app.flask_config import Config

app = Flask(__name__)
app.config.from_object(Config())


@app.route('/')
def index():
    tasks = get_tasks()
    incomplete = [task for task in tasks if task.status == 'incomplete']
    complete = [task for task in tasks if task.status == 'complete']

    return render_template("index.html", incomplete=incomplete, complete=complete)


@app.route('/add', methods=['POST'])
def add():
    add_task(request.form.get("title"))
    return redirect(url_for("index"))


@app.route('/update', methods=['POST'])
def update():
    task = get_task(request.form.get("id"))

    if request.form.get("changestatus") is not None:
        task.status = toggle(request.form.get("status"))

    if request.form.get("update") is not None or request.form.get("changestatus") is not None:
        task.description = request.form.get("description")
        task.due = request.form.get("due")
        save_task(task)

    if request.form.get("delete") is not None:
        delete_task(task.id)

    return redirect(url_for("index"))
