"""Main module"""

# pylint: disable=broad-except

import json
import os
import traceback
from datetime import datetime, timedelta, timezone

import debugpy
import jwt
from bson import ObjectId
from decouple import config
from flask import Flask, jsonify, request

from resources.database import Database
from resources.middleware import token_required

app = Flask(__name__)

with app.app_context():
    app.config["SECRET_KEY"] = config("SECRET_KEY")
    app.config["DATABASE"] = Database()


if os.getenv("DEBUG") == "true":
    debugpy.listen(("0.0.0.0", 3002))
    print("DEBUGPY: Waiting for client to attach...")
    debugpy.wait_for_client()


@app.route("/get_notes/<userid>", methods=["GET"])
@token_required
def get_notes(userid: int):
    """_summary_

    Args:
        id (int): _description_

    Returns:
        _type_: _description_
    """

    if os.getenv("DEBUG") == "true":
        debugpy.breakpoint()

    try:
        _db: Database = app.config["DATABASE"]
        notes = _db.find("notes", {"created_by": int(userid)})

        for note in notes:
            note["_id"] = str(note["_id"])

        return jsonify(notes), 200

    except Exception as ex:
        traceback.print_exc()
        return jsonify({"message": "Something went wrong!", "error": str(ex), "data": None}), 500


@app.route("/update", methods=["POST"])
@token_required
def update_note():
    if os.getenv("DEBUG") == "true":
        debugpy.breakpoint()

    try:
        data = request.json

        text = data["text"]
        user_id = data["created_by"]

        _db: Database = app.config["DATABASE"]
        _db.update_one(
            "notes",
            {"_id": ObjectId(data["_id"]), "created_by": user_id},
            {"text": text}
        )

        return json.dumps({"success": True}), 200, {"ContentType": "application/json"}

    except Exception as ex:
        traceback.print_exc()
        return jsonify({"message": "Something went wrong!", "error": str(ex), "data": None}), 500


@app.route("/delete/<noteid>", methods=["GET"])
@token_required
def delete_note(noteid: str):
    if os.getenv("DEBUG") == "true":
        debugpy.breakpoint()

    try:
        _db: Database = app.config["DATABASE"]
        noteid = str(noteid)
        _db.delete("notes", {"_id": ObjectId(noteid)})

        return jsonify({"message": "OK"}), 200

    except Exception as ex:
        traceback.print_exc()
        return jsonify({"message": "Something went wrong!", "error": str(ex), "data": None}), 500


@app.route("/create", methods=["POST"])
@token_required
def create_note():
    """_summary_

    Returns:
        _type_: _description_
    """

    if os.getenv("DEBUG") == "true":
        debugpy.breakpoint()

    try:
        data = request.json

        text = data["text"]
        user_id = data["created_by"]

        _db: Database = app.config["DATABASE"]
        _db.insert("notes", {"text": text, "created_by": user_id, "closed": False})

        return json.dumps({"success": True}), 200, {"ContentType": "application/json"}

    except Exception as ex:
        traceback.print_exc()
        return jsonify({"message": "Something went wrong!", "error": str(ex), "data": None}), 500


@app.route("/auth", methods=["POST"])
def auth():
    """_summary_

    Returns:
        _type_: _description_
    """
    try:

        if os.getenv("DEBUG") == "true":
            debugpy.breakpoint()

        _db: Database = app.config["DATABASE"]

        data = request.json

        if not data:
            return {
                "message": "Please provide credentials",
                "data": None,
                "error": "Bad request",
            }, 400

        validated = _db.find_one(
            "users", {"user": data.get("user"), "password": data.get("password")}
        )

        if not validated:
            return (
                jsonify({"message": "Invalid credentials", "data": None, "error": validated}),
                400,
            )

        token = jwt.encode(
            {
                "user": validated["user"],
                "password": validated["password"],
                "exp": (datetime.now(tz=timezone.utc) + timedelta(hours=1)),
            },
            app.config["SECRET_KEY"],
            algorithm="HS256",
        )

        return jsonify({"message": "Successfully fetched auth token", "data": token}), 200

    except Exception as ex:
        traceback.print_exc()
        return jsonify({"message": "Something went wrong!", "error": str(ex), "data": None}), 500


@app.errorhandler(Exception)
def handle_exception(_ex: Exception):
    """_summary_

    Args:
        e (Exception): _description_

    Returns:
        _type_: _description_
    """

    if os.getenv("DEBUG") == "true":
        debugpy.breakpoint()

    return jsonify({"code": 500, "description": str(_ex)})


if __name__ == "__main__":
    app.run("0.0.0.0")
