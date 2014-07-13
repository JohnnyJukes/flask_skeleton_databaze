import functools
from threading import Thread

from flask import flash, redirect, request, url_for

from data.db import db
from data.models import UserPasswordToken

def async(f):
    @functools.wraps(f)
    def wrapper(*args, **kwargs):
        thr = Thread(target=f, args=args, kwargs=kwargs)
        thr.start()
    return wrapper

def reset_token_required(f):
    @functools.wraps(f)
    def wrapper():
        userid = request.args.get('userid')
        value = request.args.get('value')

        reset_token = db.session.query(UserPasswordToken).filter_by(value=value).scalar()
        user_token = UserPasswordToken.valid_token(db.session, userid)
        if reset_token and reset_token == user_token:
            return f(userid, user_token)
        elif reset_token:
            flash("This token is no longer valid.", 'warning')
        return redirect(url_for('home.index'))
    return wrapper
