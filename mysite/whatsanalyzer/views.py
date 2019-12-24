from django.shortcuts import render
from .line_processing import *
from .count_analysis import *
from .models import Message, WhatsAppTextFile


import logging
logger = logging.getLogger(__name__)


# Create your views here.
def index(request):

    # Serve up the success page if upload is successful
    if request.method == "POST" and request.FILES:
        uploadedFile = request.FILES['WhatsAppFile']
        fileContents = uploadedFile.read().decode('utf-8')
        fileContentsList = fileContents.split('\n')

        # MAIN DRIVER FUNCTIONS
        updateWhatsAppTextFileDB(uploadedFile, fileContents)
        updateMessageDB(fileContentsList)
        CountAnalysis.calculateMetrics()

        # # DEBUG STATEMENTS
        # s1TotalMsg = CountAnalysis.senderOneTotalMessages
        # s1TotalWords = CountAnalysis.senderOneTotalWords
        # s1WPM = CountAnalysis.senderOneWordsPerMsg
        # s4 = len(CountAnalysis.senderOneTimeStamp)
        # s5 = len(CountAnalysis.senderOneReplyTimingInMinutes)
        # s2TotalMsg = CountAnalysis.senderTwoTotalMessages
        # s2TotalWords = CountAnalysis.senderTwoTotalWords
        # s2WPM = CountAnalysis.senderTwoWordsPerMsg
        # s9 = len(CountAnalysis.senderTwoTimeStamp)
        # s10 = len(CountAnalysis.senderTwoReplyTimingInMinutes)
        #
        #
        # # SERVE HTTP RESPONSE
        # return render(request, 'whatsanalyzer/upload.html', {'uploadedFile': uploadedFile,
        #                                                      'fileContents': fileContents,
        #                                                      'fileContentsList': fileContentsList,
        #                                                      'fileContentsListLength': len(fileContentsList),
        #                                                      's1TotalMsg': s1TotalMsg,
        #                                                      's1TotalWords': s1TotalWords,
        #                                                      's1WPM': s1WPM,
        #                                                      's4': s4,
        #                                                      's5': s5,
        #                                                      's2TotalMsg': s2TotalMsg,
        #                                                      's2TotalWords': s2TotalWords,
        #                                                      's2WPM': s2WPM,
        #                                                      's9': s9,
        #                                                      's10': s10})

        # Redirect to metrics
        return metrics(request)

    # Else, serve the page as per usual
    return render(request, 'whatsanalyzer/homepage.html')


def upload(request, requestFiles):
    return render(request, 'whatsanalyzer/upload.html', {'requestFiles': requestFiles})

# Helper function to generate all relevant metrics
def updateWhatsAppTextFileDB(uploadedFile, fileContents):

    # Update WhatsAppTextFile DB
    fn = uploadedFile.name
    ft = uploadedFile.content_type # Should be of type text/plain
    fc = fileContents
    myWhatsAppTextFile = WhatsAppTextFile(fileName=fn, fileType=ft, fileContents=fc)
    myWhatsAppTextFile.save()

def updateMessageDB(fileContentsList):

    # Update Message DB
    ln = 1
    for msg in fileContentsList:
        md = extractDate(msg)
        ms = extractSender(msg)
        mt = extractTextBody(msg)
        if md and ms and mt:
            myMessage = Message(lineNumber=ln, messageDate=md, messageSender=ms, messageText=mt)
            myMessage.save()
            ln += 1

def metrics(request):

    # DEBUG STATEMENTS
    s1TotalMsg = CountAnalysis.senderOneTotalMessages
    s1TotalWords = CountAnalysis.senderOneTotalWords
    s1WPM = CountAnalysis.senderOneWordsPerMsg
    # s4 = len(CountAnalysis.senderOneTimeStamp)
    # s5 = len(CountAnalysis.senderOneReplyTimingInMinutes)
    s2TotalMsg = CountAnalysis.senderTwoTotalMessages
    s2TotalWords = CountAnalysis.senderTwoTotalWords
    s2WPM = CountAnalysis.senderTwoWordsPerMsg
    s9 = len(CountAnalysis.senderTwoTimeStamp)
    s10 = len(CountAnalysis.senderTwoReplyTimingInMinutes)

    # SERVE HTTP RESPONSE
    return render(request, 'whatsanalyzer/metrics.html', {'s1TotalMsg': s1TotalMsg,
                                                          's1TotalWords': s1TotalWords,
                                                          's1WPM': s1WPM,
                                                          # 's4': s4,
                                                          # 's5': s5,
                                                          's2TotalMsg': s2TotalMsg,
                                                          's2TotalWords': s2TotalWords,
                                                          's2WPM': s2WPM})
                                                          # 's9': s9,
                                                          # 's10': s10})
