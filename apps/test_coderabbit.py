# test_coderabbit.py

# Issue 1: SQL Injection
def get_user(user_id):
    query = f"SELECT * FROM users WHERE id = {user_id}"
    return db.execute(query)

# Issue 2: Hardcoded secret
API_KEY = "sk-test-1234567890"

# Issue 3: No error handling
def fetch_data(url):
    response = requests.get(url)
    return response. json()

# Issue 4: Missing docstring
def calculate_total(items):
    return sum(item. price for item in items)


