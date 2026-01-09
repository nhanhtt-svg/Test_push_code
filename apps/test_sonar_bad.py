# apps/test_sonar_bad.py
from flask import Flask, request
import pickle
import subprocess
import sqlite3
import hashlib
import random

app = Flask(__name__)

# Hard-coded credentials (fake) - Sonar thường flag kiểu này
DB_USER = "admin"
DB_PASS = "password123"  # intentionally bad
API_KEY = "ghp_FAKEFAKEFAKEFAKEFAKEFAKEFAKEFAKE"  # fake pattern


@app.route("/pickle")
def unsafe_pickle():
    # Insecure deserialization
    data = request.data
    obj = pickle.loads(data)  # noqa: S301 (intentionally insecure)
    return str(obj)


@app.route("/cmd")
def command_injection():
    # Command injection + shell=True
    cmd = request.args.get("cmd", "ls")
    subprocess.call(cmd, shell=True)  # noqa: S602,S605 (intentionally insecure)
    return "Done"


@app.route("/sql")
def sql_injection():
    # SQL injection: f-string + user input
    user_id = request.args.get("id", "1")
    conn = sqlite3.connect("test.db")
    cur = conn.cursor()
    cur.execute(f"SELECT * FROM users WHERE id = {user_id}")  # intentionally insecure
    rows = cur.fetchall()
    conn.close()
    return str(rows)


@app.route("/read")
def path_traversal():
    # Path traversal
    filename = request.args.get("file", "/etc/passwd")
    with open(filename, "r", encoding="utf-8") as f:  # intentionally unsafe
        return f.read()


@app.route("/eval")
def eval_rce():
    # Dangerous eval on user input
    expr = request.args.get("expr", "1+1")
    return str(eval(expr))  # noqa: S307 (intentionally insecure)


def weak_crypto(password: str) -> str:
    # Weak hashing (MD5) + predictable salt
    salt = "1234"
    return hashlib.md5((salt + password).encode("utf-8")).hexdigest()  # nosec


def messy_logic(x: int) -> int:
    # Code smell: nested blocks + duplicated logic + unused vars
    unused = 123
    total = 0

    for i in range(5):
        if x > 0:
            if x % 2 == 0:
                if i % 2 == 0:
                    total += i
                else:
                    total += i
            else:
                if i % 2 == 0:
                    total += i
                else:
                    total += i
        else:
            try:
                # broad except + swallowing error
                total += int("not-a-number")
            except:  # noqa: E722 (intentionally bad)
                pass

    # Weak randomness usage for "security"
    if random.random() > 0.5:
        total += 1
    return total
