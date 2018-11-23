import boto3
import datetime
import os

from . import LOGGER


class Notification(object):

    def __init__(
            self,
            topic_arn,
            subject,
            text_content='',
    ):
        """
        Class to send notification mails.
        """
        self.aws_notification_client = boto3.client('sns', region_name='eu-west-1')
        self.subject = subject
        self.text = text_content
        self.topic_arn = topic_arn

    def send(self):
        # Send notification email
        try:
            self.aws_notification_client.publish(
                TopicArn=self.topic_arn,
                Message=self.text,
                Subject=self.subject
            )
            LOGGER.debug("Sent notification mail.")
        except Exception as e:
            LOGGER.error("Failed to send mail: " + str(e))


if __name__=="__main__":
    from . import Notification
    from . import CONFIG_OBJ

    Notification(CONFIG_OBJ.sentinel.topic_arn, "Double Items", 'test').send()
