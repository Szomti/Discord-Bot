from datetime import datetime

def log(text: str):
    print(f'\033[90m[{datetime.now()}]\033[0m {text}')