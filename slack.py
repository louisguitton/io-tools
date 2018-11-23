from slackclient import SlackClient
import pprint

from . import CONFIG_OBJ
from . import LOGGER


class Slack(object):
    def __init__(
            self,
            text_content,
            from_name='',
            to=[],
    ):
        """Class to send slack messages."""
        self.slack_client = SlackClient(CONFIG_OBJ.sentinel.slack)
        self.sender = from_name
        self.recipients = to
        self.text = text_content

    def send(self):
        assert self.slack_client
        assert self.recipients

        try:
            for recipient in self.recipients:
                resp = self.slack_client.api_call(
                    "chat.postMessage",
                    channel=recipient,
                    text=self.text,
                    username=self.sender,
                    icon_emoji=':lolsumo:'
                )
                LOGGER.debug(pprint.pformat(resp))
        except Exception as e:
            LOGGER.error("Failed to send slack message: " + str(e))
            raise e


if __name__ == '__main__':
    from . import Slack

    Slack('Hello Douche Lord!', 'Pirate_Face', ['@louis.guitton']).send()
