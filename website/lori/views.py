from flask import Blueprint, render_template, request, session, redirect, url_for
from ..common import *


views = Blueprint('lori', __name__,
                  url_prefix='/lori',
                  static_folder='static', template_folder='templates')

NUM_TRIALS = 2

create_main_route(views, lambda: dict(intro_done=False, trials_done=0))


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
        result = render_template('lori/experiment.html')
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