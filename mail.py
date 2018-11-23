import os
import boto3
import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from email.mime.text import MIMEText
from email import encoders
from email.mime.base import MIMEBase

from . import LOGGER


class Mail(object):

    def __init__(
            self,
            subject,
            text_content='',
            from_email='',
            to=[],
            files=[],
            body_images=[]
    ):
        """
        Class to send notification mails.
        """
        self.aws_mail_client = boto3.client('ses', region_name='eu-west-1')
        self.sender = from_email
        self.recipients = to
        self.subject = subject
        self.text = text_content
        self.files = files
        self.body_images = body_images

    def __assemble(self):
        # Message
        self.message = MIMEMultipart()
        self.message['From'] = self.sender
        self.message['To'] = ', '.join(self.recipients)
        self.message['Subject'] = self.subject
        self.message.attach(MIMEText(self.text))
        # Attachments
        for file in self.files:
            part = MIMEBase('application', "octet-stream")
            part.set_payload(open(file, "rb").read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition', 'attachment; filename="%s"' % os.path.basename(file))
            self.message.attach(part)
        # Body Images
        for file in self.body_images:
            img = MIMEImage(open(file, "rb").read())
            img.add_header('Content-ID', '<{}>'.format(file))
            self.message.attach(img)
            picture = MIMEText('<br><img src="cid:%s"><br>' % file, 'html')
            self.message.attach(picture)

    def attach(self, files):
        for file in files:
            self.files.append(file)

    def add_image_to_body(self, files):
        for file in files:
            self.body_images.append(file)

    def send(self):
        """Send notification email."""
        assert self.aws_mail_client
        assert self.recipients
        self.__assemble()

        try:
            self.aws_mail_client.send_raw_email(
                RawMessage={
                    'Data': self.message.as_string()
                }
            )
            LOGGER.debug("Sent notification mail.")
        except Exception as e:
            LOGGER.error("Failed to send io: " + str(e))
            raise e


if __name__ == '__main__':
    from . import Mail
    m = Mail("Spells QA", from_email='louis.guitton@dojomadness.com', to=['louis.guitton@dojomadness.com'],
         text_content='Hello guys', body_images=['../research/summoners_rift.png'])
    m.send()

    m = Mail(
        "Guides Data",
        from_email="louis.guitton@dojomadness.com",
        to=["louis.guitton@dojomadness.com"],
    )
    m.attach(['lolsumodatascience/qa_tests/guides_situation.csv'])
    m.send()

    Mail("Guides QA", from_email='louis.guitton@dojomadness.com', to=['louis.guitton@dojomadness.com'],
         files=['lolsumodatascience/qa_tests/guide_scatter.html']).send()
