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
    # if the user hasn't started the experiment,
    # redirect them to the questionnaire page
    if not is_experiment_started():
        return redirect(url_for('.main'))

    experiment_data = get_experiment_state()

    # if there is form data
    if('button-0' in request.form.to_dict().keys()):
        experiment_data['results'] = []
        print(request.form.to_dict())
        for i in range(NUM_SAT_EXPERIMENTS):
            experiment_data['results'].append(request.form.to_dict()['button-' + str(i)])
        return finish_experiment(experiment_data)

    # do experiment RNG
    experiment_data['A'] = []
    experiment_data['B'] = []
    for i in range(NUM_SAT_EXPERIMENTS):
        original = 100
        altered = rand.choice([50,75,125,150])  
        experiment_data['A'].append(original)
        experiment_data['B'].append(altered)
        if rand.getrandbits(1):
            # swap
            experiment_data['A'][i], experiment_data['B'][i] = experiment_data['B'][i], experiment_data['A'][i]
        print(experiment_data)
    set_experiment_state(experiment_data)
    return render_template("greg/satexp.html", experiment_data=experiment_data)