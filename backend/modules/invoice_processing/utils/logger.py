import logging
import os
import sys
from datetime import datetime
from logging.handlers import TimedRotatingFileHandler
import json
import traceback

class JSONFormatter(logging.Formatter):
    """Custom JSON formatter for structured logging"""
    
    def format(self, record):
        log_record = {
            'timestamp': datetime.now().isoformat(),
            'level': record.levelname,
            'message': record.getMessage(),
            'module': record.module,
            'function': record.funcName,
            'line': record.lineno
        }
        
        if record.exc_info:
            log_record['exception'] = {
                'type': str(record.exc_info[0]),
                'message': str(record.exc_info[1]),
                'stack_trace': traceback.format_exc()
            }
            
        return json.dumps(log_record)

def setup_logger():
    """Configure and return enhanced logger instance"""
    logs_dir = 'logs'
    if not os.path.exists(logs_dir):
        os.makedirs(logs_dir)
        
    log_file = os.path.join(logs_dir, 'invoice_processing.log')
    
    # Create rotating file handler
    file_handler = TimedRotatingFileHandler(
        log_file,
        when='midnight',
        backupCount=7,
        encoding='utf-8'
    )
    file_handler.setFormatter(JSONFormatter())
    
    # Create console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(JSONFormatter())
    
    # Configure logger
    logger = logging.getLogger('invoice_processing')
    logger.setLevel(logging.DEBUG)
    
    # Clear existing handlers
    if logger.hasHandlers():
        logger.handlers.clear()
        
    # Add handlers
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    # Add exception hook for uncaught exceptions
    def handle_exception(exc_type, exc_value, exc_traceback):
        logger.critical(
            "Uncaught exception",
            exc_info=(exc_type, exc_value, exc_traceback)
        )
        
    sys.excepthook = handle_exception
    
    return logger
