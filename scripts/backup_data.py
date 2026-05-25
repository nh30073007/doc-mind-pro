#!/usr/bin/env python
import shutil
from datetime import datetime
from config import get_settings

settings = get_settings()
backup_name = f"backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.zip"
shutil.make_archive(backup_name.replace('.zip', ''), 'zip', settings.PROJECT_ROOT, "data")
shutil.make_archive(backup_name.replace('.zip', '_chroma'), 'zip', settings.PROJECT_ROOT, "chroma_db")
print(f"✅ ব্যাকআপ তৈরি: {backup_name} এবং chromat.zip")