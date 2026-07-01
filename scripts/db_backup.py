import os
from datetime import datetime
from config.settings import AppConfig
from core.logger import SystemLogger

def run_automated_backup():
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    backup_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../backups/postgres'))
    backup_file = os.path.join(backup_dir, f"business_os_backup_{timestamp}.sql")
    
    # PGPASSWORD Environment ကိုသုံး၍ pg_dump အား အလိုအလျောက် သွေဖည်မောင်းနှင်ခြင်း
    os.environ['PGPASSWORD'] = AppConfig.DB_PASSWORD
    command = f"pg_dump -h {AppConfig.DB_HOST} -U {AppConfig.DB_USER} -d {AppConfig.DB_NAME} -p {AppConfig.DB_PORT} -F c -b -v -f {backup_file} >/dev/null 2>&1"
    
    status = os.system(command)
    if status == 0:
        SystemLogger.log("BACKUP", f"Database dump created successfully: {backup_file}")
    else:
        SystemLogger.log("ERROR", f"Database backup failed with status code: {status}")

if __name__ == "__main__":
    run_automated_backup()
