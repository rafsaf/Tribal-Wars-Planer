# Copyright: (c) 2020-2026, Rafał Safin <rafal.safin@rafsaf.pl>
# GNU Affero General Public License v3.0+ (see LICENSE or https://www.gnu.org/licenses/agpl-3.0.txt)

"""File with decorator to measure function time"""

import logging
from functools import wraps
from time import time

from django.db import connection, reset_queries


def timing(function):
    """Time for a given function"""

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
            new_args = str(args)
        if len(str(kwargs)) > 80:
            new_kwargs = str(kwargs)[0:80]
        else:
            new_kwargs = str(kwargs)
        end_queries = len(connection.queries)
        time3 = round(time2 - time1, 5)
        logging.debug(f"\r\n Func: {function.__name__}")
        logging.debug(f"  Args:[{new_args}]")
        logging.debug(f"  Kwargs:[{new_kwargs}]")
        logging.debug(f"  Took: {time3} sec")
        logging.debug(f"  Number of Queries: {end_queries - start_queries}")
        logging.debug("  Line by line time: ")
        return result

    return wrap
