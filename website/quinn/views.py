from flask import Blueprint, render_template, request, session, redirect, url_for
from ..common import *


views = Blueprint('quinn', __name__,
                  url_prefix='/quinn',
                  static_folder='static', template_folder='templates')


create_main_route(views, lambda: dict(trials_done=0))


@views.route('/experiment')
def experiment():
    # if the user hasn't done the initial questions,
    # redirect them to the home page
    if not is_initial_form_completed():
        return redirect(url_for('.main'))
    #TODO: what if the user finished the experiment but then goes to /experiment?
    # crash beacuse quinn_state is not in session

    state = get_experiment_state()
    if state['trials_done'] == 3:
        return finish_experiment([1,2,3])
    else:
        state['trials_done'] += 1
        set_experiment_state(state)
        return render_template('experiment.html')
