class Message:

    def __init__(self, date, sender, text):
        self.messageDate = date
        self.messageSender = sender
        self.messageText = text

    @property
    def getMessageDate(self):
        return self.messageDate

    @property
    def addMessageSender(self):
        return self.messageSender

    @property
    def getMessageText(self):
        return self.messageText



