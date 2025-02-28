from flask import Flask, request, jsonify, render_template, Blueprint
import tn_funcs as t # found in same folder
from utils import validate # found in same folder
from waitress import serve

from routes.api_routes import api_routes
from routes.page_routes import page_routes

app = Flask(__name__)

#register blueprints
app.register_blueprint(api_routes)
app.register_blueprint(page_routes)


if __name__ == '__main__':
    app.run(debug=True)
    #serve(app,host="0.0.0.0",port=5000)
    print("Finished running")