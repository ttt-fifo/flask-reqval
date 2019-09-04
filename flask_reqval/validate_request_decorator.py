"""
@validate_request(...) decorator
"""
from functools import wraps
from flask import request
from flask import abort
from .exceptions import InvalidRequest


class validate_request(object):
    """
    @validate_request(...) decorator

    Usage:
        decorate flask view function

        ....
        @validate_request(validator_callback)
        def index(...):
            ....

    Validator Callback:
        Can be any python callable, for example function
        or class which implements __call__(self,...) method.
        The validator should raise InvalidRequest exception if detects invalid
        payload.
        The validator does not need to return anything.
        See README for validator design best practices.
    """

    def __init__(self, validator_callback):
        self.validator_callback = validator_callback

    def __call__(self, func):
        @wraps(func)
        def wrapper(*arg, **kwarg):

            payload = request.get_json()

            try:
                self.validator_callback(payload)
            except InvalidRequest as e:
                abort(400, 'Invalid Request: %s' % str(e))
            except Exception:
                raise

            return func(*arg, **kwarg)
        return wrapper
