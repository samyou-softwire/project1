from flask import Flask, render_template, request, redirect, url_for

from todo_app.data.session_items import get_items, add_item, reset_items, get_item, save_item, delete_item, toggle
from todo_app.flask_config import Config

app = Flask(__name__)
app.config.from_object(Config())


@app.route('/')
def index():
    items = get_items()
    incomplete = [item for item in items if item['status'] == 'incomplete']
    complete = [item for item in items if item['status'] == 'complete']

    return render_template("index.html", incomplete=incomplete, complete=complete)


@app.route('/add', methods=['POST'])
def add():
    add_item(request.form.get("title"))
    return redirect(url_for("index"))


@app.route('/update', methods=['POST'])
def update():
    item = get_item(request.form.get("id"))

    if request.form.get("changestatus") is not None:
        item['status'] = toggle(request.form.get("status"))
        save_item(item)

    if request.form.get("delete") is not None:
        delete_item(item['id'])

    return redirect(url_for("index"))


@app.route('/reset')
def reset():
    reset_items()
    return "Done!"
