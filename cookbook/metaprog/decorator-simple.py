#!/usr/bin/python3

import time
from functools import wraps

def timethis(func):
    """Decorator that reports the execution time.
    """
    @wraps(func)   # !! Very important in order to preserve original function metadata
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(func.__name__, end-start)

    return wrapper

# Test the wrapper
@timethis
def countdown(n):
    """Count down.
    """
    print("Counting down from " + str(n))
    while n > 0:
        n -= 1

countdown(1999000)

print("Name of wrapped function: " + countdown.__name__)
print("Docstring of wrapped function: " + countdown.__doc__)
print("Annotations of wrapped function: " + str(countdown.__annotations__))

# gaining access to the original wrapped function
print("Calling the original unwrapped function")
cntd = countdown.__wrapped__
cntd(200010)



