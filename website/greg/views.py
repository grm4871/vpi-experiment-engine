from flask import Blueprint, render_template, request, session, redirect, url_for
from ..common import *
import random as rand #paul

views = Blueprint('greg', __name__,
                  url_prefix='/greg',
                  static_folder='static', template_folder='templates')

NUM_SAT_EXPERIMENTS = 12

create_main_route(views, lambda: dict(num=NUM_SAT_EXPERIMENTS, A=[], B=[]))

# gets sat_experiment
@views.route("/experiment", methods=['POST', 'GET'])
def experiment():
    # if the user hasn't done the initial questions,
    # redirect them to the home page
    if not is_initial_form_completed():
        return redirect(url_for('.main'))


    experiment_data = get_experiment_state()
    # do experiment RNG
    for i in range(NUM_SAT_EXPERIMENTS):
        original = 100
        altered = rand.choice([50,75,125,150])  
        experiment_data['A'].append(original)
        experiment_data['B'].append(altered) 
        if rand.getrandbits(1):
            # swap
            experiment_data['A'][i], experiment_data['B'][i] = experiment_data['B'][i], experiment_data['A'][i]
    set_experiment_state(experiment_data)
    return render_template("satexp.html", experiment_data=experiment_data)