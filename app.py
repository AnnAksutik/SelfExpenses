from requests import request
from flask import Flask, request
from service import ToDoService
from models import Schema

app = Flask(__name__)  # create an app instance


@app.route("/")  # at the end point /
def hello():  # call method hello
    return "Hello World!"  # which returns "hello world"


@app.route("/<name>")  # at the end point /<name>
def hello_name(name):  # call method hello_name
    return "Hello " + name  # which returns "hello + name


@app.route("/todo", methods=["POST"])
def create_todo():
    return ToDoService().create(request.get_json())


if __name__ == "__main__":  # on running python app.py
    Schema()
    app.run(debug=True)

    # conn = sqlite3.connect('todo.db')
    # # query = "create table lala(VARCHAR name)"
    # query = "select * from lala"
    # result = conn.execute(query).fetchall()
    # print(result)
