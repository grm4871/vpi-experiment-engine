from flask import Blueprint, render_template, request, session, redirect, url_for
import random as rand #paul

# from connection import get_connection

views = Blueprint('views', __name__)


INITIAL_QUESTIONS = {
    'name': dict(
        type='text',
        label='Name:',
    ),
    'age': dict(
        type='number',
        label='Age:',
    ),
    'sex': dict(
        type='radio',
        label='Sex:',
        options=[
            ('female', 'Female'),
            ('male',   'Male'),
            ('other',  'Other'),
        ],
    ),
    'color': dict(
        type='radio',
        label='Do you have any form of color deficiency or colorblindness?',
        options=[
            ('no',  'No'),
            ('yes', 'Yes'),
        ],
    ),
    'lenses': dict(
        type='radio',
        label='Do you use corrective lenses (e.g. glasses or contacts)?',
        options=[
            ('no',              'No'),
            ('yes_wearing',     'Yes, and I am wearing them for this experiment'),
            ('yes_not_wearing', 'Yes, but I am NOT wearing them for this experiment'),
        ],
    ),
}


# gets landing page
@views.route("/")
def home():
    """
    :return: index template
    """
    return render_template("index.html", questions=INITIAL_QUESTIONS)

# gets experiment
@views.route("/experiment", methods=['POST', 'GET'])
def experiment():
    if request.method == 'POST':
        # store the form data in the user's session
        form_data = request.form
        for field in INITIAL_QUESTIONS.keys():
            session[field] = form_data[field]

    elif request.method == 'GET':
        # TODO: if the user hasn't done the initial questions,
        # redirect them to the home page
        ...

    # show the experiment page
    return render_template("experiment.html")


@views.route("/quinn/", methods=['POST', 'GET'])
def quinn():
    if request.method == 'POST':
        # store the form data in the user's session
        form_data = request.form
        for field in INITIAL_QUESTIONS.keys():
            session[field] = form_data[field]

        # redirect to the experiment page
        return redirect(url_for('.quinn_experiment'))

    elif request.method == 'GET':
        # show the experiment page
        return render_template("quinn/index.html", questions=INITIAL_QUESTIONS)

@views.route("/quinn/experiment")
def quinn_experiment():
    # if the user hasn't done the initial questions,
    # redirect them to the home page
    if not all(field in session for field in INITIAL_QUESTIONS.keys()):
        return redirect(url_for('.quinn'))

    return render_template("quinn/experiment.html")


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