# -*- coding: utf-8 -*-
import functools
import inspect
import socket
import time

import sys

import os


class Settings(object):

    def __init__(self, backends=None):
        self.backends = backends or []

settings = Settings()
def configure(**kwargs):
    global settings
    settings = Settings(**kwargs)



SHORT_HOSTNAME = socket.gethostname()
ENV = 'test'


def write_metric(key, duration, **kwargs):
    metric = dict(
        hostname=SHORT_HOSTNAME,
        env=ENV,
        call=key,
        duration=duration,
    )
    metric.update(kwargs)

    for backend in settings.backends:
        backend.write(key, metric)


def get_qualified_name(func):
    """
    For python 3 we should use __qualname__ but its not available in python 2
    so in order to be consistent until we upgrade we keep of basic
    """
    path = [func.__module__]
    if sys.version_info[0] > 2:
        qualname = getattr(func, '__qualname__', None)
        path.append(qualname.replace('<locals>.', ''))
    else:
        im_class = getattr(func, 'im_class', None)
        path.append(getattr(im_class, '__name__', None))
        path.append(func.__name__)
    return '.'.join(filter(None, path))


class time_execution(object):
    def __init__(self, func, *args, **kwargs):
        self.func = func
        self.fqn = get_qualified_name(self.func)
        functools.update_wrapper(self, func)

    def __get__(self, obj, type=None):
        return self.__class__(self.func.__get__(obj, type))

    def __call__(self, *args, **kwargs):
        start_time = time.time()
        status_code = '200'
        try:
            response = self.func(*args, **kwargs)
        except Exception as exception:
            # Do something before we raise it ?
            raise
        finally:
            duration = round(time.time() - start_time, 3) * 1000
            fqn = get_qualified_name(self.func)
            write_metric(
                key=fqn,
                duration=duration,
                code=status_code
            )

        return response
