import sqlite3
import requests
from models import ToDoModel


def make_request():
    requests.post("http://localhost:5000/todo",
                  json={"Title": "my first todo",
                        "Description": "my first todo"})


if __name__ == "__main__":
    ToDoModel().create("hello", "malo")
    conn = sqlite3.connect('todo.db')
    # query = "create table lala(VARCHAR name)"
    query = "select * from Todo;"
    result = conn.execute(query).fetchall()
    print(result)

