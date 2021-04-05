from flask import Blueprint, render_template, request, session, redirect, url_for
from ..common import create_main_route, initial_form_completed


views = Blueprint('quinn', __name__,
                  url_prefix='/quinn',
                  static_folder='static', template_folder='templates')


def init_experiment_state():
    return dict(trial_num=1)

create_main_route(views, init_experiment_state)


@views.route('/experiment')
def experiment():
    # if the user hasn't done the initial questions,
    # redirect them to the home page
    if not initial_form_completed():
        return redirect(url_for('.main'))

    return render_template('experiment.html')
