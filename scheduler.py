import os
import json
import time
import datetime
import threading
from apscheduler.schedulers.background import BackgroundScheduler
from main import run_pipeline
from app.server import app

CONFIG_FILE = "output/scheduler_config.json"
LOG_FILE = "output/logs/pipeline.log"

scheduler = BackgroundScheduler()
current_job = None
last_config = None


def get_config():
    """
    Reads scheduler configuration from JSON file.
    """
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return {"enabled": False, "time": "09:00"}


def scheduled_run():
    """
    Scheduled job wrapper that executes the news pipeline.
    """
    print(f"[{datetime.datetime.now()}] APScheduler: Starting scheduled execution...")
    try:
        os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
        with open(LOG_FILE, "w", encoding="utf-8") as f:
            f.write(f"[{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] [Scheduled Run] Initializing...\n")
            
        def log_cb(msg):
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            with open(LOG_FILE, "a", encoding="utf-8") as f:
                f.write(f"[{timestamp}] {msg}\n")
                
        run_pipeline(progress_callback=log_cb)
        print(f"[{datetime.datetime.now()}] APScheduler: Scheduled execution completed successfully.")
    except Exception as e:
        print(f"[{datetime.datetime.now()}] APScheduler ERROR: Scheduled execution failed: {e}")


def watch_config_and_update_scheduler():
    """
    Background worker that monitors CONFIG_FILE and keeps the scheduler in sync.
    """
    global current_job, last_config
    
    print("Scheduler Watcher thread started.")
    
    while True:
        try:
            config = get_config()
            
            # If config changed, reload schedule
            if config != last_config:
                print(f"Scheduler: Config change detected -> {config}")
                
                # Clear existing job
                if current_job:
                    try:
                        scheduler.remove_job(current_job.id)
                        print("Scheduler: Existing job removed.")
                    except Exception:
                        pass
                    current_job = None
                
                # Add new job if enabled
                if config.get("enabled", False):
                    time_str = config.get("time", "09:00")
                    try:
                        hour, minute = map(int, time_str.split(":"))
                        
                        job = scheduler.add_job(
                            scheduled_run,
                            'cron',
                            hour=hour,
                            minute=minute,
                            id='daily_generation'
                        )
                        current_job = job
                        print(f"Scheduler: Scheduled daily run at {time_str} ({hour:02d}:{minute:02d}) successfully.")
                    except Exception as e:
                        print(f"Scheduler: Failed to set schedule: {e}")
                
                last_config = config
                
        except Exception as e:
            print(f"Scheduler: Error in configuration watcher loop: {e}")
            
        time.sleep(10)


if __name__ == "__main__":
    # Ensure logs folder exists
    os.makedirs("output/logs", exist_ok=True)
    
    # Start APScheduler
    scheduler.start()
    print("APScheduler started.")
    
    # Start watcher thread
    watcher_thread = threading.Thread(target=watch_config_and_update_scheduler, daemon=True)
    watcher_thread.start()
    
    # Start Flask Web Server
    print("Starting Flask Dashboard Web Server on http://localhost:5050")
    app.run(host="0.0.0.0", port=5050, debug=False)
