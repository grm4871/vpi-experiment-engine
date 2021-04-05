from flask import Blueprint, render_template, request, session, redirect, url_for
import random as rand #paul

# from connection import get_connection

views = Blueprint('views', __name__)


# gets landing page
@views.route("/")
def home():
    return render_template("site_home.html")


NUM_SAT_EXPERIMENTS = 12

# gets sat_experiment
@views.route("/satexp", methods=['POST', 'GET'])
def satexp():
    experiment_data = {}
    experiment_data['num'] = NUM_SAT_EXPERIMENTS
    if request.method == 'POST':
        # do experiment RNG
        for i in range(NUM_SAT_EXPERIMENTS):
            original = 100
            altered = rand.choice([50,75,125,150])  
            experiment_data['A'].append(original)
            experiment_data['B'].append(altered) 
            if rand.getrandbits(1):
                # swap
                experiment_data['A'][i], experiment_data['B'][i] = experiment_data['B'][i], experiment_data['A'][i]
        return render_template("satexp.html", experiment_data)
    else:
        pass
        # todo go back home