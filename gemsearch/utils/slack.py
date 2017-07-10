from slacker import Slacker
import sys, os
from gemsearch.settings import SLACK_API_TOKEN
import json
import logging

from pprint import pprint

class SlackHandler(logging.Handler):
    """A logging handler that posts messages to a Slack channel.
    """
    def __init__(self, channel, **kwargs):
        super(SlackHandler, self).__init__()
        self.client = Slacker(SLACK_API_TOKEN)
        self.channel = channel
        self._kwargs = kwargs

    def emit(self, record):
        message = self.format(record)
        self.client.chat.post_message(
            self.channel, 
            text = message['title'] + ': ' + message['text'], 
            username = message['author_name']
        )

class SlackFormatter(logging.Formatter):
    ''' Log Formatter for Sack Logger.
    '''
    def format(self, record):
        ret = {}
        if record.levelname == 'INFO':
            ret['color'] = 'good'
        elif record.levelname == 'WARNING':
            ret['color'] = 'warning'
        elif record.levelname == 'ERROR':
            ret['color'] = '#E91E63'
        elif record.levelname == 'CRITICAL':
            ret['color'] = 'danger'

        ret['author_name'] = record.levelname
        ret['title'] = record.name
        ret['ts'] = record.created
        ret['text'] = super(SlackFormatter, self).format(record)
        return ret


def slack_send_message(msg):
    ''' Sends message to slack channel.
    '''
    slack = Slacker(SLACK_API_TOKEN)
    slack.chat.post_message('#job-notifications', msg)

def slack_error_message(msg, err):
    ''' Sends exception to slack channel.
    '''
    exc_type, exc_obj, exc_tb = sys.exc_info()
    fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
    errInfo = [exc_type, fname, exc_tb.tb_lineno, err]
    errMessage = " - ".join(list(map(lambda i: str(i), errInfo)))

    slack_send_message(msg + errMessage)

if __name__ == '__main__':
    slack_send_message('test me')