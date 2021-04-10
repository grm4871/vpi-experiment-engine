from flask import Blueprint, render_template, request, session, redirect, url_for
from ..common import *


views = Blueprint('lori', __name__,
                  url_prefix='/lori',
                  static_folder='static', template_folder='templates')


create_main_route(views, lambda: dict(trials_done=0))


@views.route('/experiment')
def experiment():
    # if the user hasn't started the experiment,
    # redirect them to the questionnaire page
    if not is_experiment_started():
        return redirect(url_for('.main'))

    state = get_experiment_state()
    if state['trials_done'] == 3:
        return finish_experiment([1,2,3])
    else:
        state['trials_done'] += 1
        set_experiment_state(state)
        return render_template('experiment.html')
