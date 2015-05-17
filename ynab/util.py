# -*- coding: utf-8 -*-

import sys
import six


def force_encode(func):
    if six.PY2:
        def _func(*args, **kwargs):
            result = func(*args, **kwargs).encode(sys.stdout.encoding or 'utf-8')
            if isinstance(result, unicode):
                return result.encode('utf-8')
            return result
        return _func
    return func
