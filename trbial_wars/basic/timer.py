""" File with decorator to measure function time """
from time import time
from functools import wraps
from django.db import connection, reset_queries
import itertools

COUNT = itertools.count()
class memoize(dict):
    def __init__(self, func):
        self.func = func

    def __call__(self, *args):
        return self[args]

    def __missing__(self, key):
        result = self[key] = self.func(*key)
        return result
@memoize
def timer_(i: int):
    return time()

def t():
    i = next(COUNT)
    return timer_(i)
#

def timing(function):
    """ Time for given function """
    @wraps(function)
    def wrap(*args, **kwargs):
        reset_queries()
        start_queries = len(connection.queries)
        time1 = time()
        result = function(*args, **kwargs)
        time2 = time()
        if len(str(args)) > 80:
            new_args = str(args)[0:80]
        else:
            new_args = args
        if len(str(kwargs)) > 80:
            new_kwargs = str(kwargs)[0:80]
        else:
            new_kwargs = kwargs
        end_queries = len(connection.queries)
        time3 = round(time2 - time1, 3)
        print(f'\r\n Func: {function.__name__}')
        print(f'  Args:[{new_args}]')
        print(f'  Kwargs:[{new_kwargs}]')
        print(f'  Took: {time3} sec')
        print(f'  Number of Queries: {end_queries - start_queries}')
        l1 = len(timer_)
        if l1 > 0:
            print("  Line by line time: ")
            for i in range(1, l1):
                print(f'   t{i} - t{i-1}: ', round(timer_[(i,)] - timer_[(i-1,)],6), ' sec')
            print('')
            timer_.clear()
        return result

    return wrap

