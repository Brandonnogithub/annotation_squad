import os
import argparse
from flask import Flask, request, render_template
from user import User


# init flask app and env variables
app = Flask(__name__)
host = os.getenv("HOST")
port = os.getenv("PORT")


ann_user = User()


@app.route("/")
def main():
    return render_template("main.html")


@app.route("/login/")
def login():
    global ann_user
    name = request.args.get("name", None)
    
    if name:
        ann_user.name = name
        ann_user.load_data()
        return render_template("ann.html")
    else:
        return render_template("main.html")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--local", "-l", action='store_true', help="run local")
    parser.add_argument("--port", "-p", default=5000, type=int, help="runnning port")
    args = parser.parse_args()

    if args.local:
        app.run(host='127.0.0.1', port=args.port)
    else:
        app.run(host='0.0.0.0', port=args.port)
