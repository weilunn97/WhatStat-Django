from django.shortcuts import render, redirect
from .line_processing import *
from .count_analysis import *
from .models import Message, WhatsAppTextFile


import logging
logger = logging.getLogger("myLogger")


# Create your views here.
def index(request):

    # Serve up the success page if upload is successful
    if request.method == "POST" and request.FILES:
        uploadedFile = request.FILES['WhatsAppFile']
        fileContents = uploadedFile.read().decode('utf-8')
        fileContentsList = fileContents.split('\n')

        # CLEAR METRICS FIRST
        CountAnalysis.clearMetrics()

        # Delete all existing messages
        Message.objects.all().delete()

        # MAIN DRIVER FUNCTIONS
        updateWhatsAppTextFileDB(uploadedFile, fileContents)
        updateMessageDB(fileContentsList)
        CountAnalysis.calculateMetrics()

        # # Redirect to metrics
        # return metrics(request)

        # Redirect to metrics
        return redirect('WhatsAnalyzer/metrics/')

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

    # VALUES
    s1 = CountAnalysis.senderList[0]
    s2 = CountAnalysis.senderList[1]
    s1TotalMsg = CountAnalysis.senderOneTotalMessages
    s1TotalWords = CountAnalysis.senderOneTotalWords
    s1WPM = CountAnalysis.senderOneWordsPerMsg
    # s4 = len(CountAnalysis.senderOneTimeStamp)
    s1AvgReply = sum(CountAnalysis.senderOneReplyTimingInMinutes)/len(CountAnalysis.senderOneReplyTimingInMinutes)
    s2TotalMsg = CountAnalysis.senderTwoTotalMessages
    s2TotalWords = CountAnalysis.senderTwoTotalWords
    s2WPM = CountAnalysis.senderTwoWordsPerMsg
    s9 = len(CountAnalysis.senderTwoTimeStamp)
    s2AvgReply = sum(CountAnalysis.senderTwoReplyTimingInMinutes)/len(CountAnalysis.senderTwoReplyTimingInMinutes)

    # TEXT DESCRIPTION

    # TOTAL MESSAGES
    if s1TotalMsg > s2TotalMsg:
        # LARGE DIFF
        if s1TotalMsg / s2TotalMsg > 1.25:
            leftMessageText = f"Dear {s1}, you're obviously the more active person in this particular conversation, " \
                f"sending over {'%.2f' % (s1TotalMsg/s2TotalMsg)} times more texts since the start of your conversation!"
            rightMessageText = f"Dear {s2}, guess you're more a quiet person, but that's okay! {s1} is definitely a really " \
                f"good friend and chat buddy you'll always wanna keep around!"

        # SMALL DIFF
        else:
            leftMessageText = f"Well, well, {s1}, nothing much to see here I guess, both you guys have sent nearly the same " \
                f"number of texts to each other so far!"
            rightMessageText = f"Well, well, {s2}, nothing much to see here I guess, both you guys have sent nearly the same " \
                f"number of texts to each other so far!"

    else:
        # LARGE DIFF
        if s2TotalMsg / s1TotalMsg > 1.25:
            leftMessageText = f"Dear {s1}, guess you're more a quiet person, but that's okay! {s2} is definitely a really " \
                f"good friend and chat buddy you'll always wanna keep around!"

            rightMessageText = f"Dear {s2}, you're obviously the more active person in this particular conversation, " \
                f"sending over {'%.2f' % (s2TotalMsg / s1TotalMsg)} times more texts since the start of your conversation!"
        # SMALL DIFF
        else:
            leftMessageText = f"Well, well, {s1}, nothing much to see here I guess, both you guys have sent nearly the same " \
                f"number of texts to each other so far!"

            rightMessageText = f"Well, well, {s2}, nothing much to see here I guess, both you guys have sent nearly the same " \
                f"number of texts to each other so far!"


    # TOTAL WORDS
    if s1TotalWords > s2TotalWords:
        # LARGE DIFF
        if s1TotalWords / s2TotalWords > 1.25:
            leftWordsText = f"You're quite a chatty person, {s1}, I hope {s2} is okay with it! Well, do keep up " \
                f"this excellent chemistry between the both of you!"
            rightWordsText = f"On behalf of {s1}, thanks for being such a great listener, {s2}, and try not to let {s1} " \
                f"dominate the conversation ;)"
        # SMALL DIFF
        else:
            leftWordsText = f"Well, well, {s1}, I guess the both of you are equally talkative in your conversations so far, " \
                f"so keep that up!"
            rightWordsText = f"Well, well, {s2}, I guess the both of you are equally talkative in your conversations so far, " \
                f"so keep that up!"
    else:
        # LARGE DIFF
        if s2TotalWords / s1TotalWords > 1.25:
            leftWordsText = f"On behalf of {s2}, thanks for being such a great listener, {s1}, and try not to let {s2} " \
                f"dominate the conversation ;)"

            rightWordsText = f"You're quite a chatty person, {s2}, I hope {s1} is okay with it! Do keep up " \
                f"this excellent chemistry between the both of you!"

        # SMALL DIFF
        else:
            leftWordsText = f"Well, well, {s1}, I guess the both of you are equally talkative in your conversations so far, " \
                f"so keep that up!"

            rightWordsText = f"Well, well, {s2}, I guess the both of you are equally talkative in your conversations so far, " \
                f"so keep that up!"


    # WPM
    if s1WPM > s2WPM:
        # LARGE DIFF
        if s1WPM / s2WPM > 1.25:
            leftWPMText = f"My my, {s1}, your texts are turning into essays! Glad to see that you're enjoying" \
                f"your conversations with {s2}!"

            rightWPMText = f"Well, {s2}, {s1} sure loves talking to you!"

        # SMALL DIFF
        else:
            leftWPMText = f"Ahh, seems like the both of you are equally engaged in the conversation!"
            rightWPMText = f"Ahh, seems like the both of you are equally engaged in the conversation!"
    else:
        # LARGE DIFF
        if s2WPM / s1WPM > 1.25:
            leftWPMText = f"Well, {s1}, {s2} sure loves talking to you!"

            rightWPMText = f"My my, {s2}, your texts are turning into essays! Glad to see that you're enjoying" \
                f"your conversations with {s1}!"

        # SMALL DIFF
        else:
            leftWPMText = f"Ahh, seems like the both of you are equally engaged in the conversation!"
            rightWPMText = f"Ahh, seems like the both of you are equally engaged in the conversation!"


    # REPLY TIMINGS
    if s1AvgReply > s2AvgReply:
        # LARGE DIFF
        if s1AvgReply / s2AvgReply > 1.25:
            leftReplyText = f"You're a really busy person, {s1}! That's all right, but do make some time to respond to your texts :)"
            rightReplyText = f"Ahh, {s2}, you must hate waiting for {s1}'s texts, don't you? But do give {s1} just that little understanding!"
        # SMALL DIFF
        else:
            leftReplyText = f"Seems like quite a healthy interaction going on here, nothing to worry about!"
            rightReplyText = f"Seems like quite a healthy interaction going on here, nothing to worry about!"
    else:
        # LARGE DIFF
        if s2AvgReply / s1AvgReply > 1.25:
            leftReplyText = f"Ahh, {s1}, you must hate waiting for {s2}'s texts, don't you? But do give {s2} just that little understanding!"
            rightReplyText = f"You're a really busy person, {s2}! That's all right, but do make some time to respond to your texts :)"

        # SMALL DIFF
        else:
            leftReplyText = f"Seems like quite a healthy interaction going on here, nothing to worry about!"
            rightReplyText = f"Seems like quite a healthy interaction going on here, nothing to worry about!"


    # PLACEHOLDERS
    chattierPerson = s1 if s1WPM > s2WPM else s2
    chattierWPM = s1WPM if s1WPM > s2WPM else s2WPM
    slowerPerson = s1 if s1AvgReply > s2AvgReply else s2
    slowerPercent = int(s1AvgReply/s2AvgReply * 100) if s1AvgReply > s2AvgReply else int(s2AvgReply/s1AvgReply * 100)
    # SERVE HTTP RESPONSE
    return render(request, 'whatsanalyzer/metrics.html', {'s1TotalMsg': s1TotalMsg,
                                                          's1TotalWords': s1TotalWords,
                                                          's1WPM': s1WPM,
                                                          's2TotalMsg': s2TotalMsg,
                                                          's2TotalWords': s2TotalWords,
                                                          's2WPM': s2WPM,
                                                          's1AvgReply': int(s1AvgReply/60),
                                                          's2AvgReply': int(s2AvgReply/60),
                                                          'leftMessageText': leftMessageText,
                                                          'rightMessageText': rightMessageText,
                                                          'leftWordsText': leftWordsText,
                                                          'rightWordsText': rightWordsText,
                                                          'leftWPMText': leftWPMText,
                                                          'rightWPMText': rightWPMText,
                                                          'leftReplyText': leftReplyText,
                                                          'rightReplyText': rightReplyText,
                                                          'chattierPerson': chattierPerson,
                                                          'chattierWPM': chattierWPM,
                                                          'slowerPerson': slowerPerson,
                                                          'slowerPercent': slowerPercent})
