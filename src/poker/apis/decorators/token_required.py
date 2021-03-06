from functools import wraps
from flask import request
from ...models.user import User


def token_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        token = None
        print(request.headers)
        if 'Authorization' in request.headers:
            print(request.headers)
            token = request.headers['Authorization']
            token = token.replace('Bearer ', '')
        if not token:
            return {'data': 'Token is missing'}, 401
        user = User.fetch(token=token)
        if not user:
            return {'data': 'Invalid or expired authentication token'}, 401
        else:
            kwargs['user'] = user
        return func(*args, **kwargs)
    return wrapper