from django.contrib import messages
from django.shortcuts import redirect, render, reverse
from line_processing import *
from .models import Message, WhatsAppTextFile


# Create your views here.
def index(request):
    # Serve up the success page if upload is successful
    if request.method == "POST" and request.FILES:
        requestFiles = request.FILES['WhatsAppFile']
        # uploadedFile = request.FILES['WhatsAppFile']
        # fileContents = uploadedFile.read().decode('utf-8')
        # fileContentsList = fileContents.split('\n')
        # calculateMetrics()
        # return render(request, 'whatsanalyzer/upload.html', {'requestFiles': requestFiles})
        #                                                      # 'uploadedFile': uploadedFile,
        #                                                      # 'fileContents': fileContents,
        #                                                      # 'fileContentsList': fileContentsList})

        '''
        TODO
        1. CREATE WHATSAPP TEXT FILE OBJECT
        2. CREATE MESSAGE OBJECTS FOR THE UPLOADED FILE
        3. 
        '''
        return upload(request, requestFiles)
                                                               # 'uploadedFile': uploadedFile,
                                                               # 'fileContents': fileContents,
                                                               # 'fileContentsList': fileContentsList}))

    # Else, refresh the page
    return render(request, 'whatsanalyzer/homepage.html')


def upload(request, requestFiles):
    return render(request, 'whatsanalyzer/upload.html', {'requestFiles': requestFiles})

# Helper function to generate all relevant metrics
def calculateMetrics():
    for msg in Message.objects.all():
        msgDate = extractDate(msg.messageDate)
        msgSender = extractSender(msg.messageSender)
        msgTextBody = extractTextBody(msg.messageText)