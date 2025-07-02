from flask import Blueprint, render_template, request, redirect, flash
from app.forms.userForm import UserForm

asyncRoute = Blueprint('async', __name__)

@asyncRoute.route("/", methods=["GET", "POST"])
def submitAsync():
    from celeryWorker import saveUser  
    form = UserForm()

    if form.validate_on_submit():
        saveUser.delay(form.name.data, form.email.data)
        flash("Dane zostały zapisane.", "success")
        return redirect(request.path)

    return render_template("formAsync.html", form=form)
