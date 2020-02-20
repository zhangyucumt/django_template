from logging import getLogger

logger = getLogger(__name__)


class SMSMessage(object):
    def __init__(self, phone, message):
        self.phone = phone
        self.message = message

    def send(self):
        logger.info("send message to %s, message %s" % (self.phone, self.message))
        return True
