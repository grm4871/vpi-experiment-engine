from flask import render_template, request, session, redirect, url_for
from pathlib import Path
import json

__all__ = ['INITIAL_QUESTIONS', 'create_main_route', 'is_initial_form_completed', 'is_experiment_started', 'get_experiment_state', 'set_experiment_state', 'get_data_file_path', 'finish_experiment']


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


def create_main_route(blueprint, init_state_func):
    """
    Create the main route that renders the initial questionnaire form.

    :param blueprint:
        the Blueprint object to add the route to
    :param init_state_func:
        a function that returns the initial experiment state for a new user
    """

    @blueprint.route("/", methods=['POST', 'GET'])
    def main():
        if request.method == 'POST':
            # store the form data in the user's session
            form_data = request.form
            for field in INITIAL_QUESTIONS.keys():
                session[field] = form_data[field].strip()

            # initialize the experiment state
            session[blueprint.name + '_state'] = init_state_func()

            # redirect to the experiment page
            return redirect(url_for('.experiment'))

        elif request.method == 'GET':
            # show the experiment page
            return render_template(blueprint.name + "/index.html", questions=INITIAL_QUESTIONS)


def is_initial_form_completed():
    """Return whether the user has completed the initial questionnaire."""
    return all(field in session for field in INITIAL_QUESTIONS.keys())


def is_experiment_started():
    """Return whether the user has started (and not yet finished) the experiment."""
    return (request.blueprint + '_state' in session) and is_initial_form_completed()


def get_experiment_state():
    """Gets the current experiment state."""
    return session[request.blueprint + '_state']


def set_experiment_state(state):
    """Sets the current experiment state."""
    session[request.blueprint + '_state'] = state


def get_data_file_path():
    """Return the path of this experiment's data log file."""
    return Path('data') / (request.blueprint + '.json')


def finish_experiment(results):
    """
    Mark the experiment as done for this user, and return a redirect to the
    top-level home page. The data in results, along with the user's initial
    questionnaire answers, are saved to the next line in the data file as JSON.

    :param results:
        the experiment result data to save with the user metadata
    :return:
        a redirect to the top-level home page
    """

    # record the results along with the user's initial questionnaire answers
    data = {field: session[field] for field in INITIAL_QUESTIONS.keys()}
    data['results'] = results
    data_file = get_data_file_path()
    data_file.parent.mkdir(exist_ok=True)
    with data_file.open('a') as f:
        json.dump(data, f)
        f.write('\n')

    # mark the experiment as done in the user's session
    del session[request.blueprint + '_state']
    session[request.blueprint + '_done'] = True

    return redirect(url_for('main.home'))
