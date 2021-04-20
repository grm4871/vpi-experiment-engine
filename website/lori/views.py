from flask import Blueprint, render_template, request, session, redirect, url_for
from ..common import *
from .static.facial_rec import create_experiment

views = Blueprint('lori', __name__,
                  url_prefix='/lori',
                  static_folder='static', template_folder='templates')

NUM_TRIALS = 2

def init_state():
    trial1_1, trial1_2, trial2_1, trial2_2 = create_experiment()
    return dict(intro_done=False, trials_done=0, results=[], trial_info=[trial1_1, trial1_2, trial2_1, trial2_2])
create_main_route(views, init_state)

@views.route('/experiment')
def experiment():
    # if the user hasn't started the experiment,
    # redirect them to the questionnaire page
    if not is_experiment_started():
        return redirect(url_for('.main'))
    state = get_experiment_state()
    if not state['intro_done']:
        result = render_template('lori/instructions.html', NUM_TRIALS=NUM_TRIALS)
    elif state['trials_done'] < NUM_TRIALS:
        state['trials_done'] += 1
        result = render_template('lori/experiment.html', TRIAL1_1=state['trial_info'][0], TRIAL1_2=state['trial_info'][1],
        TRIAL2_1=state['trial_info'][2], TRIAL2_2=state['trial_info'][3], SET_SIZE=10)
    else:
        result = finish_experiment([1,2,3])
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
    state['results'].append({
        'was_correct': form_data['was_correct'] == 'true',
        'blink_index': int(form_data['blink_index']),
        'blink_mag': float(form_data['blink_mag']),
        'correct_x': float(form_data['correct_x']),
        'correct_y': float(form_data['correct_y']),
        'picked_x': float(form_data['picked_x']),
        'picked_y': float(form_data['picked_y']),
    })
    state['trials_done'] += 1
    set_experiment_state(state)
    return redirect(url_for('.experiment'))