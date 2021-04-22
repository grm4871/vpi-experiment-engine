from flask import Blueprint, render_template, request, session, redirect, url_for
from ..common import *
from .static.facial_rec import create_experiment

views = Blueprint('lori', __name__,
                  url_prefix='/lori',
                  static_folder='static', template_folder='templates')

NUM_TRIALS = 2

def init_state():
    trial1_1, trial1_2, correct1, trial2_1, trial2_2, correct2 = create_experiment()
    return dict(intro_done=False, trials_done=0, results=[], trial_info=[trial1_1, trial1_2, trial2_1, trial2_2],
    correct=[correct1, correct2])

create_main_route(views, init_state)

@views.route('/experiment')
def experiment():
    # if the user hasn't started the experiment,
    # redirect them to the questionnaire page
    if not is_experiment_started():
        return redirect(url_for('.main'))
    state = get_experiment_state()
    if not state['intro_done']:
        if state['trials_done'] == 0:
            result = render_template('lori/instructions.html', NUM_TRIALS=NUM_TRIALS, 
            IMAGE='static/images/ex/1.jpeg', TRIALS_DONE=state['trials_done'])
        else:
            result = render_template('lori/instructions.html',
            IMAGE='static/images/ex/1_masked.jpg', TRIALS_DONE=state['trials_done'])
    elif state['trials_done'] == 0:
        result = render_template('lori/experiment.html', TRIAL1=state['trial_info'][0], TRIAL2=state['trial_info'][1], CORRECT=state['correct'][0], SET_SIZE=10, TRIAL=0)
    elif state['trials_done'] == 1:
        result = render_template('lori/experiment.html', TRIAL1=state['trial_info'][2], TRIAL2=state['trial_info'][3], CORRECT=state['correct'][1], SET_SIZE=10, TRIAL=1)
    else:
        result = finish_experiment(state['results'])
    set_experiment_state(state)
    return result

@views.route('/begin', methods=['POST'])
def begin():
    # mark the intro as done and redirect back to the experiment
    state = get_experiment_state()
    state['intro_done'] = True
    set_experiment_state(state)
    return redirect(url_for('.experiment'))

@views.route('/submit-trial', methods=['POST'])
def submit_trial():
    # record the trial data and redirect back to the experiment
    state = get_experiment_state()
    form_data = request.form
    if (state['trials_done'] == 0):
        state['results'].append({
        'trial1_right': int(form_data['correct']),
        'trial1_wrong': int(form_data['incorrect'])
        })
    elif (state['trials_done'] == 1):
        state['results'].append({
        'trial2_right': int(form_data['correct']),
        'trial2_wrong': int(form_data['incorrect'])
        })
    state['trials_done'] += 1
    if state['trials_done'] != NUM_TRIALS:
        state['intro_done'] = False
    set_experiment_state(state)
    return redirect(url_for('.experiment'))

    