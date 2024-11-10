# app/routes/api.py
from flask import Blueprint, jsonify, request, current_app
from app.models.alarm import AlarmManager
from app.utils.challenge_manager import ChallengeManager
from datetime import datetime

api_bp = Blueprint('api', __name__)
alarm_manager = AlarmManager()
challenge_manager = ChallengeManager()

@api_bp.route('/alarms', methods=['GET'])
def get_alarms():
    """Get all alarms."""
    return jsonify(alarm_manager.get_alarms())

@api_bp.route('/alarms', methods=['POST'])
def add_alarm():
    """Add a new alarm."""
    data = request.get_json()
    time = data.get('time')
    
    if not time:
        return jsonify({"error": "Time is required"}), 400
    
    try:
        alarm_id = alarm_manager.add_alarm(time)
        if alarm_id:
            return jsonify({
                "message": "Alarm added successfully",
                "alarm_id": alarm_id
            })
        return jsonify({"error": "Invalid time format"}), 400
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

@api_bp.route('/alarms/<alarm_id>', methods=['DELETE'])
def delete_alarm(alarm_id):
    """Delete an alarm."""
    if alarm_manager.delete_alarm(alarm_id):
        return jsonify({"message": "Alarm deleted successfully"})
    return jsonify({"error": "Alarm not found"}), 404

@api_bp.route('/check-alarms', methods=['GET'])
def check_alarms():
    """Check for triggered alarms."""
    alarm = current_app.alarm_worker.get_active_alarm()
    if alarm:
        return jsonify({
            "alarm_triggered": True,
            "challenge_id": alarm['challenge_id']
        })
    return jsonify({"alarm_triggered": False})

@api_bp.route('/verify-solution', methods=['POST'])
def verify_solution():
    """Verify a challenge solution."""
    data = request.get_json()
    challenge_id = data.get('challenge_id')
    solution = data.get('solution')
    
    if not all([challenge_id, solution]):
        return jsonify({"error": "Missing required fields"}), 400
    
    results = challenge_manager.test_solution(challenge_id, solution)
    
    if results.get('all_passed'):
        # Clear the alarm if all tests passed
        active_alarm = current_app.alarm_worker.get_active_alarm()
        if active_alarm and active_alarm['challenge_id'] == challenge_id:
            current_app.alarm_worker.clear_alarm(active_alarm['alarm_id'])
    
    return jsonify(results)

@api_bp.route('/challenges', methods=['GET'])
def list_challenges():
    """Get list of available challenges."""
    return jsonify({
        "challenges": challenge_manager.list_challenges(),
        "count": challenge_manager.get_challenge_count()
    })

@api_bp.route('/dismiss-sound', methods=['POST'])
def dismiss_sound():
    """Temporarily dismiss the alarm sound."""
    if current_app.alarm_worker:
        current_app.alarm_worker.dismiss_sound()
        return jsonify({"message": "Sound dismissed"})
    return jsonify({"error": "Alarm worker not available"}), 500
