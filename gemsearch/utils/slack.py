from slacker import Slacker
import sys, os

API_TOKEN = 'TOKEN'

def slack_send_message(msg):
    slack = Slacker(API_TOKEN)
    slack.chat.post_message('#job-notifications', msg)

def slack_error_message(msg, err):
    exc_type, exc_obj, exc_tb = sys.exc_info()
    fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
    errInfo = [exc_type, fname, exc_tb.tb_lineno, err]
    errMessage = " - ".join(list(map(lambda i: str(i), errInfo)))

    slack_send_message(msg + errMessage)

if __name__ == '__main__':
    slack_send_message('test me')