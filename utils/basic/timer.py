# Copyright 2021 Rafał Safin (rafsaf). All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================

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
