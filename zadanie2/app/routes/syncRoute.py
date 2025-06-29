from flask import Blueprint, render_template, redirect, flash, request
from app.model import SyncUser
from app import db
from app.forms.userForm import UserForm


syncRoute = Blueprint('sync', __name__)

@syncRoute.route("/sync", methods=["GET", "POST"])
def submitSync():
    form = UserForm()
    if form.validate_on_submit():
        user = SyncUser(name=form.name.data, email=form.email.data)
        db.session.add(user)
        db.session.commit()
        flash("Dane zostały zapisane.", "success")
        return redirect("/sync")
    

    if request.method == "POST":
        for field, errors in form.errors.items():
            for error in errors:
                flash(f"{field.capitalize()}: {error}", "error")
    
    return render_template("formSync.html", form=form)
