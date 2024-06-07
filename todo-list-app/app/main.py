import os
import sys

project_root = os.getenv('PROJECT_ROOT')
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from flask import Flask, send_from_directory
from app.todo_api import todo_api_blueprint
from app.redis_conn import get_redis_connection

def create_app():
    app = Flask(__name__)

    # Initialize Redis connection within the application context
    with app.app_context():
        app.redis = get_redis_connection()

    # Register the blueprint from todo_api.py
    app.register_blueprint(todo_api_blueprint)

    @app.route('/')
    def serve_index():
        return send_from_directory('static', 'index.html')


    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=6000)
