from flask import Flask, render_template, request, redirect, url_for

from todo_app.data.session_items import get_items, add_item, reset_items, get_item, save_item
from todo_app.flask_config import Config

app = Flask(__name__)
app.config.from_object(Config())


@app.route('/')
def index():
    return render_template("index.html", items=get_items())


@app.route('/add', methods=['POST'])
def add():
    add_item(request.form.get("title"))
    return redirect(url_for("index"))


@app.route('/update', methods=['POST'])
def update():
    item = get_item(request.form.get("id"))
    item['status'] = request.form.get("status")
    save_item(item)

    return redirect(url_for("index"))


@app.route('/reset')
def reset():
    reset_items()
    return "Done!"
