__author__ = 'kiryam'
__version__ = '0.1'

__log_level__=1

# 0 - message
# 1 - notice
# 2 - error

def log(str, level=0):
    if level >= __log_level__:
        print(str)