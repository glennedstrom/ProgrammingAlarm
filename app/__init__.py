# app/__init__.py
from flask import Flask
from config import Config

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Register blueprints
    from app.routes import main_bp, api_bp
    app.register_blueprint(main_bp)
    app.register_blueprint(api_bp, url_prefix='/api')
    
    return app

# app/routes/main.py
from flask import Blueprint, render_template, jsonify, request
from app.utils.challenge_manager import ChallengeManager
from app.models.alarm import AlarmManager

main_bp = Blueprint('main', __name__)
alarm_manager = AlarmManager()
challenge_manager = ChallengeManager()

@main_bp.route('/')
def index():
    return render_template('index.html', alarms=alarm_manager.get_alarms())

@main_bp.route('/challenge/<challenge_id>')
def challenge(challenge_id):
    challenge = challenge_manager.get_challenge(challenge_id)
    if challenge:
        return render_template('challenge.html', challenge=challenge)
    return "Challenge not found", 404

# app/routes/api.py
from flask import Blueprint, jsonify, request
from app.models.alarm import AlarmManager

api_bp = Blueprint('api', __name__)
alarm_manager = AlarmManager()

@api_bp.route('/alarms', methods=['GET'])
def get_alarms():
    return jsonify(alarm_manager.get_alarms())

@api_bp.route('/alarms', methods=['POST'])
def add_alarm():
    data = request.get_json()
    time = data.get('time')
    if time:
        alarm_manager.add_alarm(time)
        return jsonify({"message": "Alarm added successfully"})
    return jsonify({"error": "Invalid time format"}), 400

@api_bp.route('/alarms/<alarm_id>', methods=['DELETE'])
def delete_alarm(alarm_id):
    if alarm_manager.delete_alarm(alarm_id):
        return jsonify({"message": "Alarm deleted successfully"})
    return jsonify({"error": "Alarm not found"}), 404

@api_bp.route('/verify-solution', methods=['POST'])
def verify_solution():
    data = request.get_json()
    challenge_id = data.get('challenge_id')
    solution = data.get('solution')
    
    if not all([challenge_id, solution]):
        return jsonify({"error": "Missing required fields"}), 400
    
    # Execute the solution and run tests
    results = challenge_manager.test_solution(challenge_id, solution)
    return jsonify(results)

# app/models/alarm.py
from datetime import datetime
import uuid

class Alarm:
    def __init__(self, time):
        self.id = str(uuid.uuid4())
        self.time = time
        self.active = True
        self.last_triggered = None

class AlarmManager:
    def __init__(self):
        self.alarms = {}
    
    def add_alarm(self, time):
        try:
            # Validate time format
            datetime.strptime(time, "%H:%M")
            alarm = Alarm(time)
            self.alarms[alarm.id] = alarm
            return alarm.id
        except ValueError:
            return None
    
    def delete_alarm(self, alarm_id):
        if alarm_id in self.alarms:
            del self.alarms[alarm_id]
            return True
        return False
    
    def get_alarms(self):
        return {
            id: {
                "time": alarm.time,
                "active": alarm.active,
                "last_triggered": alarm.last_triggered
            }
            for id, alarm in self.alarms.items()
        }

# config.py
import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your-secret-key-here'
    PROBLEMS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'app/problems')

# run.py
from app import create_app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
