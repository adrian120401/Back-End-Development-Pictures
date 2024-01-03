from . import app
import os
import json
from flask import jsonify, request, make_response, abort, url_for  # noqa; F401

SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
json_url = os.path.join(SITE_ROOT, "data", "pictures.json")
data: list = json.load(open(json_url))

######################################################################
# RETURN HEALTH OF THE APP
######################################################################


@app.route("/health")
def health():
    return jsonify(dict(status="OK")), 200

######################################################################
# COUNT THE NUMBER OF PICTURES
######################################################################


@app.route("/count")
def count():
    """return length of data"""
    if data:
        return jsonify(length=len(data)), 200

    return {"message": "Internal server error"}, 500


######################################################################
# GET ALL PICTURES
######################################################################
@app.route("/picture", methods=["GET"])
def get_pictures():
    return data

######################################################################
# GET A PICTURE
######################################################################


@app.route("/picture/<int:id>", methods=["GET"])
def get_picture_by_id(id):
    picture = next((picture for picture in data if picture['id'] == id), None)
    if picture is None:
        abort(404)
    return picture


######################################################################
# CREATE A PICTURE
######################################################################
@app.route("/picture", methods=["POST"])
def create_picture():
    picture = request.json
    if not picture:
        return {"message": "Invalid input parameter"}, 422
    # code to validate picture ommited
    isExist = next((obj for obj in data if obj['id'] == picture['id']), None)

    if isExist != None:
        print(picture)
        return {"Message": f"picture with id {picture['id']} already present"}, 302
    try:
        data.append(picture)
    except NameError:
        return {"message": "data not defined"}, 500
    print(picture)
    return jsonify(picture), 201

######################################################################
# UPDATE A PICTURE
######################################################################


@app.route("/picture/<int:id>", methods=["PUT"])
def update_picture(id):
    new_picture = request.json

    for index, picture in enumerate(data):
        if picture["id"] == id:
            data[index] = new_picture
            return picture, 201
    return {"message": "picture not found"}, 404

######################################################################
# DELETE A PICTURE
######################################################################
@app.route("/picture/<int:id>", methods=["DELETE"])
def delete_picture(id):
    isExist = next((obj for obj in data if obj['id'] == id), None)
    if isExist == None:
         return {"message": "picture not found"}, 404
    index = data.index(isExist)
    del data[index]
    return '', 204
