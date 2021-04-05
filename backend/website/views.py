from flask import Blueprint, render_template, request, session
import random as rand #paul

# from connection import get_connection

views = Blueprint('views', __name__)


# gets landing page
@views.route("/")
def home():
    """
    :return: index template
    """
    return render_template("index.html")

INITIAL_QUESTION_FIELDS = ['name', 'age', 'sex', 'color', 'lenses']

# gets experiment
@views.route("/experiment", methods=['POST', 'GET'])
def experiment():
    if request.method == 'POST':
        # store the form data in the user's session
        form_data = request.form
        for field in INITIAL_QUESTION_FIELDS:
            session[field] = form_data[field]

        # show the experiment page
        return render_template("experiment.html")

    elif request.method == 'GET':
        # TODO: if the user hasn't done the initial questions,
        # redirect them to the home page

        # show the experiment page
        return render_template("experiment.html")

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