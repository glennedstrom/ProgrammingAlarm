# app/utils/alarm_worker.py

from datetime import datetime
import threading
import time
import logging
from typing import Dict, Optional
from app.models.alarm import AlarmManager
from app.utils.challenge_manager import ChallengeManager

class AlarmWorker:
    """Background worker to check alarms and trigger challenges."""
    
    def __init__(self, alarm_manager: AlarmManager, challenge_manager: ChallengeManager):
        self.alarm_manager = alarm_manager
        self.challenge_manager = challenge_manager
        self.active_alarms: Dict[str, Dict] = {}
        self.thread: Optional[threading.Thread] = None
        self.running = False
        self.lock = threading.Lock()
    
    def start(self):
        """Start the background worker thread."""
        if not self.running:
            self.running = True
            self.thread = threading.Thread(target=self._check_alarms_loop, daemon=True)
            self.thread.start()
            logging.info("Alarm worker started")
    
    def stop(self):
        """Stop the background worker thread."""
        self.running = False
        if self.thread:
            self.thread.join()
            logging.info("Alarm worker stopped")
    
    def _check_alarms_loop(self):
        """Main loop to check for active alarms."""
        while self.running:
            try:
                current_time = datetime.now()
                current_time_str = current_time.strftime("%H:%M")
                current_date = current_time.date()
                
                with self.lock:
                    alarms = self.alarm_manager.get_alarms()
                    for alarm_id, alarm_data in alarms.items():
                        if (current_time_str == alarm_data['time'] and 
                            (not alarm_data['last_triggered'] or 
                             alarm_data['last_triggered'] != str(current_date))):
                            
                            # Mark alarm as triggered
                            self.alarm_manager.mark_triggered(alarm_id, current_date)
                            
                            # Get random challenge
                            challenge = self.challenge_manager.get_random_challenge()
                            
                            # Store active alarm
                            self.active_alarms[alarm_id] = {
                                'time': alarm_data['time'],
                                'challenge_id': challenge.name,
                                'triggered_at': datetime.now().isoformat()
                            }
                
                time.sleep(1)
                
            except Exception as e:
                logging.error(f"Error in alarm worker: {e}")
                time.sleep(5)  # Wait before retrying on error
    
    def get_active_alarm(self) -> Optional[Dict]:
        """Get the currently active alarm if any."""
        with self.lock:
            if self.active_alarms:
                # Return the oldest active alarm
                alarm_id = min(self.active_alarms.keys())
                return {
                    'alarm_id': alarm_id,
                    **self.active_alarms[alarm_id]
                }
            return None
    
    def clear_alarm(self, alarm_id: str):
        """Clear an active alarm after challenge is completed."""
        with self.lock:
            if alarm_id in self.active_alarms:
                del self.active_alarms[alarm_id]
