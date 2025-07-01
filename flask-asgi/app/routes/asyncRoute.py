from flask import Blueprint, render_template, request

asyncRoute = Blueprint('async', __name__)

@asyncRoute.route("/")
def async_form():
    return render_template("formAsync.html")

@asyncRoute.route("/", methods=["POST"])
def submitAsync():
    from celeryWorker import saveUser
    name = request.form.get("name")
    email = request.form.get("email")
    saveUser.delay(name, email)
    return render_template("formAsync.html")
