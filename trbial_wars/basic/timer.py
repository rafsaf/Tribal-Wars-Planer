""" File with decorator to measure function time """
from time import time
from functools import wraps
from django.db import connection, reset_queries

def ti(lst=[], result=False, clear=False):
    if result:
        return lst
    if clear:
        lst.clear()
        return lst
    lst.append(time())
    return None

def timing(function):
    """ Time for a given function """
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
        time3 = round(time2 - time1, 5)
        print(f'\r\n Func: {function.__name__}')
        print(f'  Args:[{new_args}]')
        print(f'  Kwargs:[{new_kwargs}]')
        print(f'  Took: {time3} sec')
        print(f'  Number of Queries: {end_queries - start_queries}')
        print("  Line by line time: ")
        for i, actual in enumerate(ti(result=True)):
            try:
                print('   ', i, ' Period: ', round(actual - previous, 5))
            except UnboundLocalError:
                pass
            previous = actual
        ti(clear=True)
        return result

    return wrap
