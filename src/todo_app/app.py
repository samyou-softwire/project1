from flask import Flask, render_template, request, redirect, url_for

from todo_app.data.session_tasks import get_tasks, add_task, get_task, save_task, delete_task, toggle
from todo_app.data.view_model import ViewModel
from todo_app.flask_config import Config
from dateutil import parser as dateparser

app = Flask(__name__)
app.config.from_object(Config())


@app.route('/')
def index():
    tasks_view_model = ViewModel(get_tasks())

    return render_template("templates/index.html", view_model=tasks_view_model)


@app.route('/add', methods=['POST'])
def add():
    add_task(request.form.get("title"))
    return redirect(url_for("index"))


@app.route('/update', methods=['POST'])
def update():
    task = get_task(request.form.get("id"))
    submit_type = request.form.get("submittype")

    if submit_type == "changestatus":
        task.status = toggle(request.form.get("status"))

    if submit_type in ["changestatus", "update"]:
        task.description = request.form.get("description")

        due = request.form.get("due")
        if due == "":
            due = None
        task.due = dateparser.parse(due) if due is not None else None
        save_task(task)

    if submit_type == "delete" is not None:
        delete_task(task.id)

    return redirect(url_for("index"))
