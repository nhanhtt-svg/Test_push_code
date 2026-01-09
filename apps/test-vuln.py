# Ví dụ lỗ hổng: Hard-coded secret (API key)
import pickle
API_KEY = "sk_live_1234567890abcdef"  # CodeQL sẽ flag là "Hard-coded credentials"

# Hoặc lỗ hổng SQL injection


def get_user(user_id):
    query = f"SELECT * FROM users WHERE id = {user_id}"
    cursor.execute(query)  # CodeQL flag "SQL injection"


# Hoặc unsafe deserialization
pickle.loads(user_input)  # CodeQL flag "Unsafe deserialization"
