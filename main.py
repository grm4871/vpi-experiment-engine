# greg mockler
# quinn tucker
# lori liu

"""

main.py is the main class for the application

"""

from website import create_app

# from connection import add_songs
app = create_app()

# add_songs()
if __name__ == "__main__":
    app.run(debug=True, threaded=False, host='0.0.0.0')
