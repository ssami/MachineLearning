import redis

from flask import g


def get_db():
    # if 'db' not in g:
    #     g.db = redis.Redis(
    #         host="localhost",
    #         port=6379,
    #         password=None
    #     )
    # return g.db
    # TODO: make sure DB connection is created and cached
    return redis.Redis(
            host="localhost",
            port=6379,
            password=None
        )


def close_db():
    db = g.pop('db', None)
    if db is not None:
        db.close()


def init_app(app):
    app.teardown_appcontext(close_db)