'''
import logging
logging.debug('This is a debug message')
logging.info('This is an info message')
logging.warning('This is a warning message')
logging.error('This is an error message')
logging.critical('This is a critical message')

This is for capturing and routing log messages.

Log Levels:
The logging module defines five standard log levels (in increasing order of severity):

DEBUG: Detailed information, useful for diagnosing problems.
INFO: Confirmation that things are working as expected.
WARNING: An indication that something unexpected happened or may cause problems.
ERROR: A more serious problem; the program did not perform some function.
CRITICAL: A severe error that may prevent the program from continuing.

Each level has an associated numeric value (10 for DEBUG up to 50 for CRITICAL)
'''

import logging as log

log.basicConfig(
    level = log.INFO,
    format = "%(asctime)s - %(levelname)s - %(name)s - %(message)s"
)

def divide(a, b):
    log.info(f'Dividing {a} by {b}')
    try:
        result = a / b
        log.info(f'Result {result}')
        return result
    except ZeroDivisionError:
        log.error('Attempted to divide by zero')
        return None

divide(10, 2)
divide(10,0)

'''
1. Basic Usage:
    To start logging, we simply import the logging module and use its functions
'''