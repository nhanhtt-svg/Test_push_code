from flask import Flask, request
import pickle
import subprocess
import os

app = Flask(__name__)

# 1. RULE: python.flask.security.audit.avoid-pickle.avoid-pickle
@app.route('/pickle')
def unsafe_pickle():
    data = request.data  # User-controlled input
    obj = pickle.loads(data)  # 🚨 SEMGREP WILL CATCH: python.lang.security.deserialization.pickle.avoid-pickle
    return str(obj)

# 2. RULE: python.lang.security.audit.subprocess-shell-true.subprocess-shell-true
@app.route('/cmd')
def command_injection():
    cmd = request.args.get('cmd')  # User input
    subprocess.call(cmd, shell=True)  # 🚨 SEMGREP WILL CATCH: python.lang.security.command-injection
    return "Done"

# 3. RULE: python.lang.security.audit.tainted-format-string.tainted-format-string  
@app.route('/format')
def format_string():
    user_input = request.args.get('input')
    return "Hello %s" % user_input  # 🚨 Có thể bị format string attack

# 4. RULE: secrets (phát hiện API keys, tokens)
@app.route('/secret')
def leak_secret():
    # 🚨 SEMGREP SECRETS RULES sẽ phát hiện:
    API_KEY = "ghp_1234567890abcdefGHJKLMNOP"  # GitHub token pattern
    AWS_KEY = "AKIAIOSFODNN7EXAMPLE"  # AWS key
    return f"Keys: {API_KEY[:5]}...{AWS_KEY[:5]}..."

# 5. RULE: python.lang.security.audit.path-traversal.path-traversal
@app.route('/read')
def path_traversal():
    filename = request.args.get('file')
    with open(filename, 'r') as f:  # 🚨 Path traversal vulnerability
        return f.read()

# 6. RULE: python.lang.security.audit.sql-injection.sql-injection  
@app.route('/sql')
def sql_injection():
    import sqlite3
    user_id = request.args.get('id')
    conn = sqlite3.connect('test.db')
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM users WHERE id = {user_id}")  # 🚨 SQL injection
    return str(cursor.fetchall())