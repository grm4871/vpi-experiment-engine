from flask import Blueprint, render_template, request, session, redirect, url_for
<<<<<<< Updated upstream
import random as rand #paul
=======
import random
>>>>>>> Stashed changes

# from connection import get_connection

views = Blueprint('main', __name__)


NAMES = ['Greg', 'Lori', 'Quinn']

def is_experiment_completed(name):
    key = name.lower() + '_done'
    return key in session and session[key]

<<<<<<< Updated upstream
# gets landing page
@views.route("/")
def home():
    return render_template("site_home.html",
        completed_names=[name for name in NAMES if is_experiment_completed(name)],
        not_completed_names=[name for name in NAMES if not is_experiment_completed(name)])
=======
# gets favicon
import os
from flask import send_from_directory

@views.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(views.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')

# gets landing page
@views.route("/")
def home():
    names_shuffled = NAMES.copy()
    random.shuffle(names_shuffled)
    return render_template("site_home.html",
        completed_names=[name for name in names_shuffled if is_experiment_completed(name)],
        not_completed_names=[name for name in names_shuffled if not is_experiment_completed(name)])
>>>>>>> Stashed changes
