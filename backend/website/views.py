from flask import Blueprint, render_template, request, session

# from connection import get_connection

views = Blueprint('views', __name__)


# gets landing page
@views.route("/")
def home():
    """
    :return: index template
    """
    return render_template("index.html")

INITIAL_QUESTION_FIELDS = ['name', 'age', 'sex', 'color', 'lenses']

# gets experiment
@views.route("/experiment", methods=['POST', 'GET'])
def experiment():
    if request.method == 'POST':
        # store the form data in the user's session
        form_data = request.form
        for field in INITIAL_QUESTION_FIELDS:
            session[field] = form_data[field]

        # show the experiment page
        return render_template("experiment.html")

    elif request.method == 'GET':
        # TODO: if the user hasn't done the initial questions,
        # redirect them to the home page

        # show the experiment page
        return render_template("experiment.html")
