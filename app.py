import os
import argparse
from flask import Flask, request, render_template
from user import User


# init flask app and env variables
app = Flask(__name__)
host = os.getenv("HOST")
port = os.getenv("PORT")

app.jinja_env.auto_reload = True
app.config['TEMPLATES_AUTO_RELOAD'] = True

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
        curr_data = ann_user.next()
        token_list = curr_data["context_tokens"].split(" ")
        doc_id = ann_user.get_curr_docID()
        doc_total = ann_user.total_num
        return render_template("ann.html", doc=token_list, doc_id=doc_id, doc_total=doc_total)
        # return render_template("test.html")
    else:
        return render_template("main.html")


@app.route("/pages/", methods=['GET'])
def next_page():
    global ann_user
    page_id = int(request.args.get("page_id"))
    if page_id < 1:
        page_id = 1
    if page_id > ann_user.total_num:
        page_id = ann_user.total_num

    curr_data = ann_user.get_data(page_id)
    token_list = curr_data["context_tokens"].split(" ")
    doc_total = ann_user.total_num
    return render_template("ann.html", doc=token_list, doc_id=page_id, doc_total=doc_total)


@app.route('/savepost', methods=['GET', 'POST'])
def savepost():
    print("get")
    data = request.form.get("array")
    print(data)
    return "2333"


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--local", "-l", action='store_true', help="run local")
    parser.add_argument("--port", "-p", default=5000, type=int, help="runnning port")
    args = parser.parse_args()

    if args.local:
        app.run(host='127.0.0.1', port=args.port)
    else:
        app.run(host='0.0.0.0', port=args.port)
