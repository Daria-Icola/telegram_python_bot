import logging
import logging.config
import os

logging.config.fileConfig('./logging/logging.conf')

# create logger
logger = logging.getLogger('reports_bot')

# 'application' code
logger.debug('DEBUG. only')
logger.info('INFO')
logger.warning('WARNING!')
logger.error('ATTENTION! ATTENTION!')
logger.critical('CRITICAL!')