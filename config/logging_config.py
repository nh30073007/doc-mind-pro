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
    
    # ফাইল হ্যান্ডলার 
    file_handler = RotatingFileHandler(
        log_file, maxBytes=5_242_880, backupCount=3, encoding="utf-8"
    )
    file_handler.setFormatter(formatter)
    file_handler.setLevel(logging.DEBUG) ে
    
    # কনসোল হ্যান্ডলার 
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    console_handler.setLevel(getattr(logging, settings.LOG_LEVEL, logging.INFO))
    
    # লগার তৈরি
    logger = logging.getLogger(module_name)
    logger.setLevel(logging.DEBUG)    
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    
    return logger

# সরাসরি ব্যবহারের জন্য একটি ডিফল্ট লগার
default_logger = setup_logging("doc_mind")
