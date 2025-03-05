import threading

class SendEmailThread(threading.Thread):
    def __init__(self,email):
        threading.Thread.__init__(self)
        super().__init__()
        self.email = email

    def run(self):
            return self.email.send()
