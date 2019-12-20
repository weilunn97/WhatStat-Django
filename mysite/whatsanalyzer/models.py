from django.db import models
from whatsanalyzer.count_analysis import *
from whatsanalyzer.line_processing import *

# Create your models here.
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


class Message(models.Model):
    # Setup all attributes related to a Message
    _lineNumber = models.IntegerField()
    _messageDate = models.DateTimeField()
    _messageSender = models.CharField(max_length=500)
    _messageText = models.TextField
    # Add a FK within Message to enforce that each Message must belong to a WhatsAppTextFile
    # Upon deletion of the file object, we shall also delete all Message objects
    _whatsAppTextFile = models.ForeignKey(WhatsAppTextFile, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self._messageDate} {self._messageSender} {self._messageText}"