from flask import render_template, request, session, redirect, url_for

__all__ = ['INITIAL_QUESTIONS', 'create_main_route', 'initial_form_completed']


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
            return render_template("index.html", questions=INITIAL_QUESTIONS)


def initial_form_completed():
    """Return whether the user has completed the initial questionnaire."""
    return all(field in session for field in INITIAL_QUESTIONS.keys())
