import logging
import colorlog

# Logging
logging.basicConfig(filename='autopilot.log', level=logging.DEBUG)
logger = colorlog.getLogger()
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler()
handler.setLevel(logging.DEBUG)
handler.setFormatter(
    colorlog.ColoredFormatter('%(log_color)s%(levelname)-8s%(reset)s %(white)s%(message)s',
                              log_colors={
                                  'DEBUG': 'fg_bold_cyan',
                                  'INFO': 'fg_bold_green',
                                  'WARNING': 'bg_bold_yellow,fg_bold_blue',
                                  'ERROR': 'bg_bold_red,fg_bold_white',
                                  'CRITICAL': 'bg_bold_red,fg_bold_yellow',
                              }, secondary_log_colors={}

                              ))
logger.addHandler(handler)

logger.debug('This is a DEBUG message. This information is usually used for troubleshooting')
logger.info('This is an INFO message. This information is usually used for conveying information')
logger.warning('This is a WARNING message. This information is usually used for warning')
logger.error('This is an ERROR message. This information is usually used for errors and should not happen')
logger.critical('This is a CRITICAL message. '
                'This information is usually used for critical error, and will usually result in an exception.')