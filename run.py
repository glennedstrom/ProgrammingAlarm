# run.py
import logging
from app import create_app
from app.utils.alarm_worker import AlarmWorker
from app.models.alarm import AlarmManager
from app.utils.challenge_manager import ChallengeManager

def setup_logging():
    """Configure logging for the application."""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler('flask_alarm.log')
        ]
    )

def main():
    """Application entry point."""
    # Setup logging
    setup_logging()
    logging.info("Starting Flask Programming Alarm Clock")
    
    try:
        # Create Flask app
        app = create_app()
        
        # Initialize managers
        alarm_manager = AlarmManager()
        challenge_manager = ChallengeManager()
        
        # Create and start alarm worker
        alarm_worker = AlarmWorker(alarm_manager, challenge_manager)
        alarm_worker.start()
        
        # Store worker in app context
        app.alarm_worker = alarm_worker
        
        # Run the application
        app.run(host='0.0.0.0', port=5000)
        
    except Exception as e:
        logging.error(f"Fatal error: {str(e)}", exc_info=True)
        raise
    finally:
        # Cleanup
        logging.info("Application shutdown")
        if 'alarm_worker' in locals():
            alarm_worker.stop()

if __name__ == '__main__':
    main()

