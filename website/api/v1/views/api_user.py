from . import api_views
from website.models.user import User
from .errors import not_found
from flask import abort, jsonify, make_response, request


@api_views.route('/users')
def get_users():
    """Get a list of users"""
    all_users = User.query.all()

    if all_users:
        list_users = []

        for user in all_users:
            list_users.append(user.to_dict())

    return make_response(jsonify(list_users), 200)


@api_views.route('/users/<id>', methods=['GET'])
def get_user(id):
    """get a specific user by its id"""
    user = User.query.filter_by(id=id).first()

    if user:
        return make_response(jsonify(user.to_dict()), 200)
    return not_found(404)
