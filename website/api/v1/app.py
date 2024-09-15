"""Flask app"""


from views import api_views
from flask import Flask, jsonify, make_response


app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
app.register_blueprint(api_views)


@app.errorhandler(404)
def not_found(error):
    """Not found error"""
    return make_response(jsonify({"error": "Not found"}), 404)


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)
