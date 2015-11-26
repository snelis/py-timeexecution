# -*- coding: utf-8 -*-
from functools import wraps


def get_qualified_name(func, classname=None):
    fqn = [func.__module__, func.__name__]
    if classname:
        fqn.insert(1, classname)
    return ".".join(fqn)


def time_execution(classname=None):
    def decorator(func):
        @wraps(func)
        def wrapped_func(*args, **kwargs):
            return func(*args, **kwargs)
        wrapped_func.__fqn__ = get_qualified_name(func, classname)
        return wrapped_func
    return decorator
