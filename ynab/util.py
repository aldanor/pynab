# -*- coding: utf-8 -*-

import sys
import six


def force_encode(func):
    """
    This decorator is meant to be used on __repr__ and __str__ to provide py2/py3 compatibility
    (Python 2 expectes bytestrings whereas Python 3 expects unicode).
    """
    if six.PY2:
        def _func(*args, **kwargs):
            result = func(*args, **kwargs).encode(sys.stdout.encoding or 'utf-8')
            if isinstance(result, unicode):
                return result.encode('utf-8')
            return result
        return _func
    return func
