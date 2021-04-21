from flask import Blueprint, render_template, request, session, redirect, url_for
import random as rand #paul

# from connection import get_connection

views = Blueprint('main', __name__)


NAMES = ['Greg', 'Lori', 'Quinn']

def is_experiment_completed(name):
    key = name.lower() + '_done'
    return key in session and session[key]

# gets landing page
@views.route("/")
def home():
    return render_template("site_home.html",
        completed_names=[name for name in NAMES if is_experiment_completed(name)],
        not_completed_names=[name for name in NAMES if not is_experiment_completed(name)])
