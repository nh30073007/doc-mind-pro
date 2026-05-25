# config/logging_config.py
import logging
import sys
from pathlib import Path
from logging.handlers import RotatingFileHandler

from .settings import get_settings

def setup_logging(module_name: str = "doc_mind") -> logging.Logger:
    """
    সব লগ হ্যান্ডলার সেটআপ করে এবং লগার রিটার্ন করে।
    """
    settings = get_settings()
    log_dir = settings.LOG_DIR
    log_dir.mkdir(parents=True, exist_ok=True)
    
    log_file = log_dir / "app.log"
    
    # ফরম্যাট নির্ধারণ
    formatter = logging.Formatter(
        fmt="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    
    # ফাইল হ্যান্ডলার (রোটেশন: সর্বোচ্চ 5MB, 3টি ব্যাকআপ)
    file_handler = RotatingFileHandler(
        log_file, maxBytes=5_242_880, backupCount=3, encoding="utf-8"
    )
    file_handler.setFormatter(formatter)
    file_handler.setLevel(logging.DEBUG)  # ফাইলে সব ডিটেইল রাখবে
    
    # কনসোল হ্যান্ডলার (স্ট্যান্ডার্ড আউটপুটে)
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    console_handler.setLevel(getattr(logging, settings.LOG_LEVEL, logging.INFO))
    
    # লগার তৈরি
    logger = logging.getLogger(module_name)
    logger.setLevel(logging.DEBUG)  # রুট লেভেল সব ধরবে, হ্যান্ডলার ফিল্টার করবে
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    # ডুপ্লিকেট এড়াতে (যদি আবার কল হয়) ফ্ল্যাগ চেক করা যায়, কিন্তু এটুকুই যথেষ্ট
    return logger

# সরাসরি ব্যবহারের জন্য একটি ডিফল্ট লগার
default_logger = setup_logging("doc_mind")