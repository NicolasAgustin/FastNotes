"""Middleware module"""

# pylint: disable=broad-except

from functools import wraps

import jwt
from flask import current_app, jsonify, request
from resources.database import Database


def token_required(func):
    """_summary_

    Args:
        f (_type_): _description_

    Returns:
        _type_: _description_
    """

    @wraps(func)
    def decorated(*args, **kwargs):
        token = None
        if "Authorization" in request.headers:
            token = request.headers["Authorization"].split(" ")[1]
        if not token:
            return {
                "message": "Authentication token is missing.",
                "data": None,
                "error": "Unauthorized",
            }, 400
        try:
            data = jwt.decode(token, current_app.config["SECRET_KEY"], algorithms=["HS256"])

            _db: Database = current_app.config["DATABASE"]

            validated = _db.find_one(
                "users", {"user": data.get("user"), "password": data.get("password")}
            )

            if not validated:
                return (
                    jsonify(
                        {
                            "message": "Invalid Authentication token!",
                            "data": None,
                            "error": "Unauthorized",
                        }
                    ),
                    401,
                )

        except Exception as ex:
            return {"message": "Something went wrong", "data": None, "error": str(ex)}, 500

        return func(*args, **kwargs)

    return decorated
