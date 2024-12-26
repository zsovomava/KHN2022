import threading

from django.core.mail import send_mail


class MailThread(threading.Thread):
    def __init__(self, *args):
        self.args = args
        super(MailThread, self).__init__()

    def run(self):
        send_mail(*self.args)


def send_mail_async(subject, message, from_email, recipient_list):
    MailThread(subject, message, from_email, recipient_list).start()
