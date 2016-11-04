"""Plugin: Notify Slack."""

import json
import requests
from nelmon.args.notifier import NotifierArguments
from nelmon.globals import NelmonGlobals

NelmonGlobals(PLUGIN_VERSION='1.0')

description = """This plugin sends notifications to Slack using an incoming
webhook in Slack.
"""

# For more information about this plugin visit:
# https://networklore.com/nelmon/


HEADERS = {
    'Content-Type': 'application/json',
    'Accept': 'application/json',
    'User-Agent': 'Nelmon'
}


class Notification(object):

    def __init__(self, host=None, notification_type=None, host_state=None,
                 service_state=None, host_address=None, host_output=None,
                 service_output=None, long_datetime=None, service_description=None):
        self.host = host
        self.notification_type = notification_type
        self.host_state = host_state
        self.service_state = service_state
        self.host_address = host_address
        self.host_output = host_output
        self.service_output = service_output
        self.long_datetime = long_datetime
        self.service_description = service_description

        self.message = ''
        self._parse_args()

    def _parse_args(self):
        message = ''
        if self.notification_type:
            message += "%s " % self.notification_type
        if self.host:
            message += "%s " % self.host
        if self.host_state:
            message += "%s " % self.host_state
        if self.host_output:
            message += "%s " % self.host_output
        if self.service_state:
            message += "%s " % self.service_state
        if self.service_description:
            message += "%s " % self.service_description
        if self.service_output:
            message += "%s " % self.service_output

        self.message = message


class Slack(object):
    """Send messages to Slack.

    Args:
    -----
        channel (str): The Channel in Slack where the message will appear
        key (str): The Slack webhook API key
        username (str): The username which will be shown as the sender of the message
        user_icon (str): The emoji will will be used as the user avatar, for example: :apple:
    """

    def __init__(self, channel=None, key=None, username=None, user_icon=None):
        """Send messages to Slack.

        Args:
        -----
            channel (str): The Channel in Slack where the message will appear
            key (str): The Slack webhook API key
            username (str): The username which will be shown as the sender of the message
            user_icon (str): The emoji will will be used as the user avatar, for example: :apple:
        """
        self.channel = channel
        self.key = key
        self.username = username
        self.user_icon = user_icon

    def _post(self, data):
        requests.post(
            'https://hooks.slack.com/services/' + self.key,
            headers=HEADERS,
            data=data)

    def send(self, message):
        """Send a text message to Slack."""
        data = {}
        data['text'] = message
        if self.channel:
            data['channel'] = self.channel
        if self.username:
            data['username'] = self.username
        if self.user_icon:
            data['icon_emoji'] = self.user_icon
        data['mrkdwn'] = False

        jdata = json.dumps(data)
        self._post(data=jdata)


def _get_args():
    argparser = NotifierArguments(description)

    argparser.parser.add_argument(
        '-t',
        help='Slack Webhook Token',
        type=str,
        required=True)
    argparser.parser.add_argument(
        '-c',
        help='Slack channel',
        type=str,
        default=None)
    argparser.parser.add_argument(
        '-u',
        help='Slack username',
        type=str,
        default=None)
    argparser.parser.add_argument(
        '-i',
        help='Slack user_icon',
        type=str,
        default=None)

    return argparser.parser.parse_nelmon_args()


def main():
    """Plugin: notify_slack."""
    args = _get_args()

    slack = Slack(key=args.t, channel=args.c, username=args.u, user_icon=args.i)

    n = Notification(
        host=args.H,
        notification_type=args.n,
        host_state=args.s,
        service_description=args.d,
        service_state=args.S,
        host_address=args.a,
        service_output=args.e,
    )

    slack.send(n.message)
