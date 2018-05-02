
# Author: Steven C. Dang

# Convenience class and functions for supporting logging in Workflow components

import logging
from logging.handlers import SysLogHandler
from logging import StreamHandler
from logging import FileHandler
from datetime import datetime as dt
import os.path as path
import os
import sys

logger = logging.getLogger('ls_logging')

def setup_logging(lgr, config, workingDir=None, is_test=False):
    """
    Basic logging configuration. Takes 3 parameters:

    Inputs
        logger - a logger given from logging.getLogger()
        config - a dictionary that expects 4 values:
            log_level: {TRACE, DEBUG, INFO, WARNING, ERROR}
            enable_syslog = True/False enable logging to local syslog
            enable_file_log = True/False enable writing logs to file
            file_log_path = file path string of where to write a log file
        is_test - True/False flag to support logging to file when testing 
            outside a workflow component.
    Output: returns the given logger with appropriate adjustments

    """
    # Set the workingDir to current Directory if none is given
    if workingDir is None:
        logger.warning("Not working directory given. Using cwd")
        workingDir = os.getcwd()
    
    # Setup Logging to file in working directory
    lgr.setLevel(config['log_level'])

    # Set log msg format
    formatter = logging.Formatter('%(levelname)s\t%(name)s\t%(asctime)s\t: %(message)s')
    
    # Write log msgs to sysLog if logging is enabled
    if config['enable_syslog']:
        ch = SysLogHandler()
        ch.setLevel(config['log_level'])
        ch.setFormatter(formatter)
        lgr.addHandler(ch)
    # Write log msgs to file if enabled
    if config['enable_file_log']:
        log_id = dt.now().isoformat()
        if config['file_log_path'] is None:
            log_file = path.join(workingDir, 'log-%s.txt' % log_id)
        else:
            log_file = path.join(config['file_log_path'], 'log-%s.txt' % log_id)
        ch = FileHandler(filename=log_file)
        ch.setLevel(config['log_level'])
        ch.setFormatter(formatter)
        lgr.addHandler(ch)

    # Add extra logging to file
    if is_test:
        logger.debug("not running as a tigris component")
        # Add explicit file log
        log_file = path.join(workingDir, 'test.log')
        logger.debug("Writing logs to : %s" % str(log_file))
        ch = FileHandler(filename=log_file)
        ch.setLevel(config['log_level'])
        ch.setFormatter(formatter)
        lgr.addHandler(ch)

    # Create stream handler to output error messages to stderr
    ch = StreamHandler(sys.stderr)
    ch.setLevel(logging.ERROR)
    ch.setFormatter(formatter)
    lgr.addHandler(ch)
   
    # Create separator in log file to make it easier to parse
    for i in range(3):
        lgr.info("####################################################")

    return lgr


