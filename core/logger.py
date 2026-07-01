import os
from datetime import datetime

class SystemLogger:
    @staticmethod
    def log(event_type, message):
        log_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../logs'))
        os.makedirs(log_dir, exist_ok=True)
        
        log_file = os.path.join(log_dir, f"{event_type.lower()}.log")
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        with open(log_file, "a", encoding="utf-8") as file:
            file.write(f"[{timestamp}] {message}\n")
