import json
import secrets
import sys

API_KEYS_FILE = 'api_keys.json'

def load_api_keys():
    try:
        with open(API_KEYS_FILE, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def save_api_keys(api_keys):
    with open(API_KEYS_FILE, 'w') as f:
        json.dump(api_keys, f, indent=2)

def generate_api_key(user_id):
    api_keys = load_api_keys()
    new_key = secrets.token_urlsafe(32)
    api_keys[new_key] = user_id
    save_api_keys(api_keys)
    print(f"New API key for user {user_id}: {new_key}")

def delete_api_key(api_key):
    api_keys = load_api_keys()
    if api_key in api_keys:
        del api_keys[api_key]
        save_api_keys(api_keys)
        print(f"API key {api_key} deleted.")
    else:
        print(f"API key {api_key} not found.")

def list_api_keys():
    api_keys = load_api_keys()
    for key, user_id in api_keys.items():
        print(f"User {user_id}: {key}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python api_key_manager.py [generate <user_id> | delete <api_key> | list]")
    elif sys.argv[1] == "generate" and len(sys.argv) == 3:
        generate_api_key(sys.argv[2])
    elif sys.argv[1] == "delete" and len(sys.argv) == 3:
        delete_api_key(sys.argv[2])
    elif sys.argv[1] == "list":
        list_api_keys()
    else:
        print("Invalid command")