""" File with decorator to measure function time """

from functools import wraps
from time import time


def timing(function):
    """ Time for given function """
    @wraps(function)
    def wrap(*args, **kwargs):
        time_before = time()
        result = function(*args, **kwargs)
        time_after = time()
        if len(str(args)) > 150:
            new_args = str(args)[0:150]
        else:
            new_args = args
        if len(str(kwargs)) > 150:
            new_kwargs = str(kwargs)[0:150]
        else:
            new_kwargs = kwargs
        print(
            "func:%r args:[%r, %r] took: %2.4f sec"
            % (function.__name__, new_args, new_kwargs, time_after - time_before))
        return result

    return wrap
