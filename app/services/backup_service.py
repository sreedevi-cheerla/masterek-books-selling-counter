import os
import shutil
from datetime import datetime
from app.config import settings

class BackupService:
    @staticmethod
    def trigger_local_backup():
        source_db = os.path.join(settings.DATA_DIR, "guru_pooja.db")
        if not os.path.exists(source_db):
            return
            
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_filename = f"guru_pooja_backup_{timestamp}.db"
        dest_path = os.path.join(settings.BACKUP_DIR, backup_filename)
        
        shutil.copy2(source_db, dest_path)
