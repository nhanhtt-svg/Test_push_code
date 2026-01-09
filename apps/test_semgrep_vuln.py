from flask import Flask, request
import pickle
import subprocess

app = Flask(__name__)

@app.route('/pickle')
def unsafe_pickle():
    data = request.data  # User-controlled input
    obj = pickle.loads(data)  # Semgrep sẽ flag "dangerous-pickle-use" (critical)
    return str(obj)

@app.route('/cmd')
def command_injection():
    cmd = request.args.get('cmd')  # User input
    subprocess.call(cmd, shell=True)  # Semgrep flag "command-injection" (high)

@app.route('/secret')
def leak_secret():
    API_KEY = "ghp_1234567890abcdefGHJKLMNOP"  # GitHub token pattern
    return API_KEY  # Semgrep flag secret leak nếu dùng p/secrets