import sys

from flask import Flask

app = Flask(__name__)
from app import routes


if __name__ == "__main__":
    if sys.version_info < (3, 7):
        print("This program requires python version 3.7+.")
        exit(-1)
    app.run(debug=True)
