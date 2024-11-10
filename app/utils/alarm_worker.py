# app/utils/alarm_worker.py

from datetime import datetime
import threading
import time
import logging
from typing import Dict, Optional
import pygame
from pynput import mouse, keyboard
from pathlib import Path
import sys
import os

class ActivityMonitor:
    def __init__(self, inactivity_timeout=30):
        self.last_activity = time.time()
        self.inactivity_timeout = inactivity_timeout
        self.monitoring = False
        self.mouse_listener = None
        self.keyboard_listener = None
    
    def on_activity(self, *args):
        """Update timestamp of last activity."""
        self.last_activity = time.time()
    
    def start_monitoring(self):
        """Start monitoring mouse and keyboard activity."""
        if not self.monitoring:
            self.mouse_listener = mouse.Listener(
                on_move=self.on_activity,
                on_click=self.on_activity,
                on_scroll=self.on_activity
            )
            self.keyboard_listener = keyboard.Listener(
                on_press=self.on_activity,
                on_release=self.on_activity
            )
            
            self.mouse_listener.start()
            self.keyboard_listener.start()
            self.monitoring = True
    
    def stop_monitoring(self):
        """Stop monitoring activity."""
        if self.monitoring:
            if self.mouse_listener:
                self.mouse_listener.stop()
            if self.keyboard_listener:
                self.keyboard_listener.stop()
            self.monitoring = False
    
    def is_inactive(self):
        """Check if user has been inactive beyond timeout."""
        return time.time() - self.last_activity > self.inactivity_timeout

class AlarmSound:
    def __init__(self):
        pygame.mixer.init()
        self.sound = None
        self.playing = False
        self.load_sound()
    
    def load_sound(self):
        """Load the alarm sound file."""
        sound_path = Path(__file__).parent.parent / 'static' / 'sounds' / 'alarm.mp3'
        try:
            self.sound = pygame.mixer.Sound(str(sound_path))
        except Exception as e:
            logging.error(f"Failed to load alarm sound: {e}")
    
    def play(self):
        """Play the alarm sound if not already playing."""
        if not self.playing and self.sound:
            self.sound.play(-1)  # -1 means loop indefinitely
            self.playing = True
    
    def stop(self):
        """Stop the alarm sound."""
        if self.playing and self.sound:
            self.sound.stop()
            self.playing = False

class AlarmWorker:
    """Background worker to check alarms and trigger challenges."""
    
    def __init__(self, alarm_manager, challenge_manager):
        self.alarm_manager = alarm_manager
        self.challenge_manager = challenge_manager
        self.active_alarms: Dict[str, Dict] = {}
        self.thread: Optional[threading.Thread] = None
        self.running = False
        self.lock = threading.Lock()
        
        # Initialize activity monitoring and sound
        self.activity_monitor = ActivityMonitor()
        self.alarm_sound = AlarmSound()
    
    def start(self):
        """Start the background worker thread."""
        if not self.running:
            self.running = True
            self.thread = threading.Thread(target=self._check_alarms_loop, daemon=True)
            self.thread.start()
            self.activity_monitor.start_monitoring()
            logging.info("Alarm worker started")
    
    def stop(self):
        """Stop the background worker thread."""
        self.running = False
        if self.thread:
            self.thread.join()
        self.activity_monitor.stop_monitoring()
        self.alarm_sound.stop()
        logging.info("Alarm worker stopped")
    
    def _check_alarms_loop(self):
        """Main loop to check for active alarms."""
        while self.running:
            try:
                current_time = datetime.now()
                current_time_str = current_time.strftime("%H:%M")
                current_date = current_time.date()
                
                with self.lock:
                    # Check for inactive user when alarm is active
                    if self.active_alarms and self.activity_monitor.is_inactive():
                        self.alarm_sound.play()
                    
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
                            
                            # Start playing alarm
                            self.alarm_sound.play()
                
                time.sleep(1)
                
            except Exception as e:
                logging.error(f"Error in alarm worker: {e}")
                time.sleep(5)
    
    def get_active_alarm(self) -> Optional[Dict]:
        """Get the currently active alarm if any."""
        with self.lock:
            if self.active_alarms:
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
                if not self.active_alarms:  # No more active alarms
                    self.alarm_sound.stop()
                    self.activity_monitor.last_activity = time.time()  # Reset activity timer

    def dismiss_sound(self):
        """Temporarily dismiss the alarm sound."""
        self.alarm_sound.stop()
        self.activity_monitor.last_activity = time.time()  # Reset activity timer
