from flask import Blueprint, render_template, request, session, redirect, url_for
from ..common import *


views = Blueprint('quinn', __name__,
                  url_prefix='/quinn',
                  static_folder='static', template_folder='templates')


create_main_route(views, lambda: dict(trial_num=1))


@views.route('/experiment')
def experiment():
    # if the user hasn't done the initial questions,
    # redirect them to the home page
    if not is_initial_form_completed():
        return redirect(url_for('.main'))

    finish_experiment([1,2,3])  # TODO: testing

    return render_template('experiment.html')
