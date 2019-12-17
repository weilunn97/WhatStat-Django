from django.db import models


# Create your models here.
class LineProcessing(models.Model):
    @staticmethod
    def extractDate(text):
        pass

    @staticmethod
    def extractSender(text):
        pass

    @staticmethod
    def extractText(text):
        pass

    @staticmethod
    def parseDateString(date):
        pass


class CountAnalysis(models.Model):
    # Metrics to be calculated later (via single loop through messageList)
    senderOneTotalMessages = 0
    senderTwoTotalMessages = 0
    senderOneTotalWords = 0
    senderTwoTotalWords = 0

    @staticmethod
    def calculateCounts():
        pass


class ReplyTimingAnalysis(models.Model):
    # Setup all attributes related to reply timings
    _lineNumber = models.IntegerField()
    _messageSender = models.CharField(max_length=500)
    _replyDurationHours = models.FloatField()

    @staticmethod
    def calculateCounts():
        pass


class GraphAnalysis(models.Model):
    pass


class WhatsAppTextFile(models.Model):
    # Setup all attributes related to a WhatsAppTextFile
    _filePath = models.CharField(max_length=260)
    _fileName = models.CharField(max_length=260)
    _fileContents = models.TextField()

    def __str__(self):
        return self._fileName

    @property
    def getFilePath(self):
        return self._filePath

    @property
    def getFileName(self):
        return self._fileName

    @property
    def getFileContents(self):
        return self._fileContents

    @property
    def getFileMessages(self):
        return self._fileMessages


class Message(models.Model):
    # Setup all attributes related to a Message
    _lineNumber = models.IntegerField()
    _messageDate = models.DateTimeField()
    _messageSender = models.CharField(max_length=500)
    _messageText = models.TextField
    # Add a FK within Message to enforce that each Message must belong to a WhatsAppTextFile
    # Upon deletion of the file object, we shall also delete all Message objects
    _whatsAppTextFile = models.ForeignKey(WhatsAppTextFile, on_delete=models.CASCADE)

    @property
    def getLineNumber(self):
        return self._lineNumber

    @property
    def getMessageDate(self):
        return self._messageDate

    @property
    def getMessageSender(self):
        return self._messageSender

    @property
    def getMessageText(self):
        return self._messageText