from datetime import datetime

def log(text: str):
    print(f'\033[90m[{datetime.now()}]\033[0m {text}')
    f = open('./data/logs.txt', 'a')
    f.write(f'\n[{datetime.now()}] {text}')
    f.close()