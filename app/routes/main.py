# app/routes/main.py
from flask import Blueprint, render_template, jsonify, current_app
from app.utils.challenge_manager import ChallengeManager
from app.models.alarm import AlarmManager

main_bp = Blueprint('main', __name__)
manager = AlarmManager()

@main_bp.route('/')
def index():
    """Render the main page with alarm settings."""
    return render_template('index.html', alarms=manager.get_alarms())

@main_bp.route('/challenge/<challenge_id>')
def challenge(challenge_id):
    """Render the challenge page."""
    challenge_manager = ChallengeManager()
    challenge = challenge_manager.get_challenge(challenge_id)
    if challenge:
        return render_template('challenge.html', challenge=challenge)
    return "Challenge not found", 404

