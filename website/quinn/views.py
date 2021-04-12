from flask import Blueprint, render_template, request, session, redirect, url_for
from ..common import *


views = Blueprint('quinn', __name__,
                  url_prefix='/quinn',
                  static_folder='static', template_folder='templates')

NUM_TRIALS = 10

create_main_route(views, lambda: dict(intro_done=False, trials_done=0, results=[]))


@views.route('/experiment')
def experiment():
    # if the user hasn't started the experiment,
    # redirect them to the questionnaire page
    if not is_experiment_started():
        return redirect(url_for('.main'))

    state = get_experiment_state()
    if not state['intro_done']:
        return render_template('quinn/instructions.html', NUM_TRIALS=NUM_TRIALS)
    elif state['trials_done'] < NUM_TRIALS:
        return render_template('quinn/experiment.html', trial_num=state['trials_done']+1, NUM_TRIALS=NUM_TRIALS)
    else:
        return finish_experiment(state['results'])

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
