_log = None

def init():
    global _log
    _log = open('py-virpu/log.txt', 'w')

def log(message:str):
    global _log
    _log.write(message + '\n')

def cleanup():
    global _log
    _log.close()