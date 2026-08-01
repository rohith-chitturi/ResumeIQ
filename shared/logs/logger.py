import logging
import sys

def setup_logger(name: str) -> logging.Logger:
    """
    Sets up a structured logger for the application.
    Replaces print statements with proper log levels (INFO, WARNING, ERROR, DEBUG).
    """
    logger = logging.getLogger(name)
    
    # Avoid adding multiple handlers if logger is already set up
    if not logger.handlers:
        logger.setLevel(logging.INFO)
        
        # Create console handler with formatting
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.INFO)
        
        # Create formatter and add it to the handler
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        console_handler.setFormatter(formatter)
        
        # Add the handler to the logger
        logger.addHandler(console_handler)
        
    return logger

# Create a default application logger
logger = setup_logger("resumeiq")
