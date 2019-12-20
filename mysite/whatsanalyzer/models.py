from django.db import models
from whatsanalyzer.count_analysis import *
from whatsanalyzer.line_processing import *

# Create your models here.
class WhatsAppTextFile(models.Model):
    # Setup all attributes related to a WhatsAppTextFile
    _filePath = models.CharField(max_length=260)
    _fileName = models.CharField(max_length=260)
    _fileContents = models.TextField()

    def __str__(self):
        return f"WhatsAppTextFile : {self._fileName}"


class Message(models.Model):
    # Setup all attributes related to a Message
    lineNumber = models.IntegerField()
    messageDate = models.DateTimeField()
    messageSender = models.CharField(max_length=500)
    messageText = models.TextField
    # Add a FK within Message to enforce that each Message must belong to a WhatsAppTextFile
    # Upon deletion of the file object, we shall also delete all Message objects
    whatsAppTextFile = models.ForeignKey(WhatsAppTextFile, on_delete=models.CASCADE)

    def __str__(self):
        return f"Message : {self.messageDate} {self.messageSender} {self.messageText}"