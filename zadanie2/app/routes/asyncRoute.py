from flask import Blueprint, render_template, request

asyncRoute = Blueprint('async', __name__)

@asyncRoute.route("/")
def async_form():
    return render_template("formAsync.html")

@asyncRoute.route("/", methods=["POST"])
def submitAsync():
    from celeryWorker import saveUser
    data = request.get_json()
    name = data.get("name")
    email = data.get("email")
    saveUser.delay(name, email)
    return "Dane zostały wysłane do przetworzenia w tle."
