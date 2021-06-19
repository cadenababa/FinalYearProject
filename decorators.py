from functools import wraps
from flask_login import current_user
from flask import abort

def only_for_teacher(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_teacher:
            abort(403)
        return f(*args, **kwargs)
    return decorated_function

def only_for_student(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_student:
            abort(403)
        return f(*args, **kwargs)
    return decorated_function