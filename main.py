# greg mockler
# quinn tucker

"""

main.py is the main class for the application

"""

from website import create_app
from waitress import serve

def create():
    return create_app()

app = create()

if __name__ == "__main__":
    serve(app, port=5000)
    #app.run(debug=True, threaded=False, host='0.0.0.0')
