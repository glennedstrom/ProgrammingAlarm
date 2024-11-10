# app/models/alarm.py
from datetime import datetime
import uuid
from typing import Dict, Optional, Any

class Alarm:
    """Represents a single alarm."""
    def __init__(self, time: str):
        self.id = str(uuid.uuid4())
        self.time = time
        self.active = True
        self.last_triggered = None
        self.created_at = datetime.now().isoformat()
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'time': self.time,
            'active': self.active,
            'last_triggered': self.last_triggered,
            'created_at': self.created_at
        }

class AlarmManager:
    """Manages multiple alarms."""
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(AlarmManager, cls).__new__(cls)
            cls._instance.alarms: Dict[str, Alarm] = {}
        return cls._instance
    
    def add_alarm(self, time: str) -> Optional[str]:
        """Add a new alarm."""
        try:
            # Validate time format
            datetime.strptime(time, "%H:%M")
            alarm = Alarm(time)
            self.alarms[alarm.id] = alarm
            return alarm.id
        except ValueError:
            return None
    
    def delete_alarm(self, alarm_id: str) -> bool:
        """Delete an alarm."""
        if alarm_id in self.alarms:
            del self.alarms[alarm_id]
            return True
        return False
    
    def get_alarms(self) -> Dict[str, Dict[str, Any]]:
        """Get all alarms."""
        return {
            id: alarm.to_dict()
            for id, alarm in self.alarms.items()
        }
    
    def mark_triggered(self, alarm_id: str, trigger_date) -> bool:
        """Mark an alarm as triggered for today."""
        if alarm_id in self.alarms:
            self.alarms[alarm_id].last_triggered = str(trigger_date)
            return True
        return False
    
    def get_active_alarms(self) -> Dict[str, Dict[str, Any]]:
        """Get all active alarms."""
        return {
            id: alarm.to_dict()
            for id, alarm in self.alarms.items()
            if alarm.active
        }
