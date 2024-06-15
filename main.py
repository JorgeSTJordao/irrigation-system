from smartsprout import app
from smartsprout.create_db import create_db

if __name__ == "__main__":
    create_db(app)
    app.run(host='0.0.0.0', debug=False)