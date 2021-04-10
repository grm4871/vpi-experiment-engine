from flask import Blueprint, render_template, request, session, redirect, url_for
import random as rand #paul

# from connection import get_connection

views = Blueprint('main', __name__)


# gets landing page
@views.route("/")
def home():
    return render_template("site_home.html")