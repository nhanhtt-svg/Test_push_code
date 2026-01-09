# test_codeql_vuln.py - Ví dụ gây fail chắc chắn

# 1. SQL injection rõ ràng với user input (Flask ví dụ)
from flask import Flask, request
import sqlite3

app = Flask(__name__)

@app.route('/user')
def get_user():
    user_id = request.args.get('id')  # User-controlled input
    conn = sqlite3.connect(':memory:')
    cursor = conn.cursor()
    query = f"SELECT * FROM users WHERE id = {user_id}"  # f-string injection
    cursor.execute(query)  # Sink rõ ràng
    return "Done"

# 2. Unsafe deserialization với remote input
import pickle
from flask import request

@app.route('/load')
def load_pickle():
    data = request.data  # User-controlled bytes
    obj = pickle.loads(data)  # Unsafe sink với remote source
    return str(obj)