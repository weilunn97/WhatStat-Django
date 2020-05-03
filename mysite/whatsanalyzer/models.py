

# class WhatsAppTextFile(models.Model):
#     # Setup all attributes related to a WhatsAppTextFile
#     fileName = models.CharField(max_length=260)
#     fileType = models.CharField(max_length=100)
#     fileContents = models.TextField()
#
#     def __str__(self):
#         return f"WhatsAppTextFile : {self.fileName}"


# class Message(models.Model):
#     # Setup all attributes related to a Message
#     lineNumber = models.IntegerField()
#     messageDate = models.DateTimeField()
#     messageSender = models.CharField(max_length=1000)
#     messageText = models.TextField()
#
#     # Add a FK within Message to enforce that each Message must belong to a WhatsAppTextFile
#     # Upon deletion of the file object, we shall also delete all Message objects
#     # whatsAppTextFile = models.ForeignKey(WhatsAppTextFile, on_delete=models.CASCADE)
#
#     def __str__(self):
#         return f"Message : {self.messageDate} | {self.messageSender} | {self.messageText}"
