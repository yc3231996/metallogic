from utils.api_key_manager import load_api_keys, API_KEYS_FILE

print(f"API密钥文件路径: {API_KEYS_FILE}")
api_keys = load_api_keys()
print(f"加载的API密钥: {api_keys}") 