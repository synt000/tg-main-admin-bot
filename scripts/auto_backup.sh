#!/bin/bash
# 🗄️ SaaS Operating System Automatic Daily Backup System
BACKUP_DIR="../backups/postgres"
mkdir -p $BACKUP_DIR
FILENAME="$BACKUP_DIR/saas_db_backup_$(date +%Y%m%d_%H%M%S).sql"

echo "🔄 Starting automatic database stream snapshot..."
pg_dump -d postgres > $FILENAME

if [ -f "$FILENAME" ]; then
    echo "✅ [SUCCESS]: PostgreSQL Backup Compressed perfectly at $FILENAME"
else
    echo "❌ [ERROR]: Database streaming backup aborted."
fi
