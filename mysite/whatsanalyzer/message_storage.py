class MessageStorage:

    messageList = []

    @staticmethod
    def addMessage(m):
        MessageStorage.messageList.append(m)

    @staticmethod
    def countMessages():
        return len(MessageStorage.messageList)

    @staticmethod
    def getMessageList():
        return MessageStorage.messageList

    @staticmethod
    def clearMessageList():
        MessageStorage.messageList.clear()