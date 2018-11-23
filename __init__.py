"""Wrapper to send emails in python."""
import logging
import logging.config
import os

io_folder = os.path.dirname(__file__)

LOGGER = logging.getLogger('mailer')
CONFIG_OBJ = {}

from .slack import Slack
from .mail import Mail
from .notify import Notification
from .s3 import S3Service
