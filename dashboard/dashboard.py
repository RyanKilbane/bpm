from flask import Flask, Blueprint, render_template

dashboard_point = Blueprint("dashboard", __name__)

@dashboard_point.route("/")
def dashboard():
    return render_template("./dashboard.html")