from . import api_views
from flask import abort, jsonify, make_response, request


@api_views.errorhandler(404)
def not_found(error):
    """Not found error"""
    return make_response(jsonify({"error": "Not found"}), 404)