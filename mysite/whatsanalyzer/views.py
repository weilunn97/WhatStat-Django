from .count_analysis import *
from datetime import timedelta
from django.shortcuts import render, redirect
import json
import pdb

# TODO
"""


2. Clean up the following debug
- DEBUG tags
- print(...) functions




6. Refactor-rename all _new template files to the original version

7. Delete all old unused html templates

8. Set flags to prevent further processing upon upload
"""


def index(request):
    # UPON SUCCESSFUL UPLOAD
    if request.method == "POST" and request.FILES:
        # DEBUG
        request.session.flush()

        # EXTRACT INTO LIST OF STRINGS (1 LINE = 1 STRING)
        fileContentsList = readFile(request)

        # PLACE FILE INTO BROWSER SESSION
        request.session['fileContentsList'] = fileContentsList

        # REDIRECT TO METRICS PAGE
        return redirect('metrics/')

    # Else, serve the page as per usual
    return render(request, 'whatsanalyzer/homepage.html')


def charts(request):
    senderOne = CountAnalysis.senderList[0]
    senderTwo = CountAnalysis.senderList[1]
    senderOneDates = CountAnalysis.senderOneTimeStamp
    senderTwoDates = CountAnalysis.senderTwoTimeStamp
    senderOneReplyTimingInMinutes = CountAnalysis.senderOneReplyTimingInMinutes
    senderTwoReplyTimingInMinutes = CountAnalysis.senderTwoReplyTimingInMinutes

    # Custom date formatter for x-axis
    def xAxisFormatter(date):
        # Convert to GMT+8 timezone
        date += timedelta(hours=8)
        return date.strftime("%d %b %Y, %H:%M")

    # Custom hour formatter for y-axis
    def yAxisFormatter(replyTimeInMinutes):
        return round(replyTimeInMinutes / 60, 2)

    return render(request, 'whatsanalyzer/charts.html',
                  {'senderOne': json.dumps(senderOne),
                   'senderTwo': json.dumps(senderTwo),
                   'senderOneDates': json.dumps(senderOneDates, indent=4, sort_keys=True, default=xAxisFormatter),
                   'senderOneReplyTimingInMinutes': list(map(yAxisFormatter, senderOneReplyTimingInMinutes)),
                   'senderTwoDates': json.dumps(senderTwoDates, indent=4, sort_keys=True, default=xAxisFormatter),
                   'senderTwoReplyTimingInMinutes': list(map(yAxisFormatter, senderTwoReplyTimingInMinutes))})


def metrics(request):

    # FROM CLOUD
    if request.method == "POST":
        print("CLOUD TRIGGERED")
        CountAnalysis.setInitialized(False)
        CountAnalysis.clearMetrics()
        MessageStorage.clearMessageList()
        textFile = request.POST.get('textFile')
        fileContentsList = textFile.split('\n')
        calculateMetrics(fileContentsList)

    # FROM LOCAL PC
    else:
        try:
            if request.session['fileContentsList']:
                print("LOCAL PC TRIGGERED")
                # CALCULATE THE METRICS FOR DISPLAY AND REMOVE IT
                calculateMetrics(request.session.pop('fileContentsList'))

        except KeyError:
            pass

    # RETRIEVE METRICS FROM CountAnalysis
    if CountAnalysis.getInitialized():
        s1 = CountAnalysis.senderList[0]
        s2 = CountAnalysis.senderList[1]
        s1TotalMsg = CountAnalysis.senderOneTotalMessages
        s1TotalWords = CountAnalysis.senderOneTotalWords
        s1WPM = CountAnalysis.senderOneWordsPerMsg
        s1AvgReply = sum(CountAnalysis.senderOneReplyTimingInMinutes) / len(CountAnalysis.senderOneReplyTimingInMinutes)
        s2TotalMsg = CountAnalysis.senderTwoTotalMessages
        s2TotalWords = CountAnalysis.senderTwoTotalWords
        s2WPM = CountAnalysis.senderTwoWordsPerMsg
        s2AvgReply = sum(CountAnalysis.senderTwoReplyTimingInMinutes) / len(CountAnalysis.senderTwoReplyTimingInMinutes)

        # TOTAL MESSAGES
        if s1TotalMsg > s2TotalMsg:
            # LARGE DIFF
            if s1TotalMsg / s2TotalMsg > 1.25:
                leftMessageText = f"Dear {s1}, you're obviously the more active person in this particular conversation, " \
                                  f"sending over {'%d' % ((s1TotalMsg / s2TotalMsg) * 100 - 100)}% more texts since the start of your conversation!"
                rightMessageText = f"Dear {s2}, guess you're more a quiet person, but that's okay! {s1} is definitely a really " \
                                   f"good friend and chat buddy you'll always wanna keep!"

            # SMALL DIFF
            else:
                leftMessageText = f"Mhm, {s1}, the both of you have sent nearly the same " \
                                  f"number of texts to each other so far!"
                rightMessageText = f"{s2}, seems like the both of you are equally invested in the conversation, that's good!"

        else:
            # LARGE DIFF
            if s2TotalMsg / s1TotalMsg > 1.25:
                leftMessageText = f"Dear {s1}, guess you're more a quiet person, but that's okay! {s2} is definitely a really " \
                                  f"good friend and chat buddy you'll always wanna keep around!"

                rightMessageText = f"Dear {s2}, you're obviously the more active person in this particular conversation, " \
                                   f"sending over {'%.2f' % (s2TotalMsg / s1TotalMsg)} times more texts since the start of your conversation!"
            # SMALL DIFF
            else:
                leftMessageText = f"Well, {s1}, you've both sent around the same number of texts so far!"

                rightMessageText = f"Ahh, {s2}, all your texts are getting responded to, so no worries there!"

        # TOTAL WORDS
        if s1TotalWords > s2TotalWords:
            # LARGE DIFF
            if s1TotalWords / s2TotalWords > 1.25:
                leftWordsText = f"You're quite a chatty person, {s1}, I hope {s2} likes it! Well, do keep up " \
                                f"this excellent chemistry you guys have!"
                rightWordsText = f"On behalf of {s1}, thanks for being such a great listener, {s2}, and try not to let {s1} " \
                                 f"dominate the conversation ;)"
            # SMALL DIFF
            else:
                leftWordsText = f"Well, {s1}, you're both equally chatty! So nothing you need to worry about here!"
                rightWordsText = f"Great, {s2}, you're both equally invested in your conversations so far, so keep that up!"
        else:
            # LARGE DIFF
            if s2TotalWords / s1TotalWords > 1.25:
                leftWordsText = f"On behalf of {s2}, thanks for being such a great listener, {s1}, and try not to let {s2} " \
                                f"dominate the conversation ;)"
                rightWordsText = f"You're quite a chatty person, {s2}! Do keep up this excellent chemistry you guys have!"

            # SMALL DIFF
            else:
                leftWordsText = f"Well, {s1}, both of you are equally chatty, so keep that up!"
                rightWordsText = f"Mhmm {s2}, great to see that you're both equally chatty!"

        # WPM
        if s1WPM > s2WPM:
            # LARGE DIFF
            if s1WPM / s2WPM > 1.25:
                leftWPMText = f"My my, {s1}, your texts are turning into essays!"

                rightWPMText = f"Well, {s2}, {s1} sure loves talking to you!"

            # SMALL DIFF
            else:
                leftWPMText = f"Ahh, {s1}, seems like the both of you are equally engaged in the conversation, so do keep that up!!"
                rightWPMText = f"Dear {s2}, seems like the both of you are equally engaged in the conversation, so do keep that up!!"
        else:
            # LARGE DIFF
            if s2WPM / s1WPM > 1.25:
                leftWPMText = f"Well, {s1}, {s2} sure loves talking to you!"

                rightWPMText = f"My my, {s2}, your texts are turning into essays!"

            # SMALL DIFF
            else:
                leftWPMText = f"Dear {s1}, seems like the both of you are equally engaged in the conversation, so do keep that up!!"
                rightWPMText = f"Ahh {s2}, seems like the both of you are equally engaged in the conversation, so do keep that up!!"

        # REPLY TIMINGS
        if s1AvgReply > s2AvgReply:
            # LARGE DIFF
            if s1AvgReply / s2AvgReply > 1.25:
                leftReplyText = f"You're a really busy person, {s1}! That's all right, but do make some time to respond to your texts :)"
                rightReplyText = f"{s2}, you must hate waiting for {s1}'s texts, don't you? But do give {s1} some space!"
            # SMALL DIFF
            else:
                leftReplyText = f"Seems like quite a healthy interaction going on here, nothing to worry about there, {s1}!"
                rightReplyText = f"Seems like quite a healthy interaction going on here, nothing to worry about there, {s2}!"
        else:
            # LARGE DIFF
            if s2AvgReply / s1AvgReply > 1.25:
                leftReplyText = f"{s1}, you must hate waiting for {s2}'s texts, don't you?  But do give {s2} some space!"
                rightReplyText = f"You're a really busy person, {s2}! That's all right, but do make some time to respond to your texts :)"

            # SMALL DIFF
            else:
                leftReplyText = f"Seems like quite a healthy interaction going on here, nothing to worry about there, {s1}!"
                rightReplyText = f"Seems like quite a healthy interaction going on here, nothing to worry about there, {s2}!"

        # PLACEHOLDERS
        chattierPerson = s1 if s1WPM > s2WPM else s2
        chattierWPM = s1WPM if s1WPM > s2WPM else s2WPM
        slowerPerson = s1 if s1AvgReply > s2AvgReply else s2
        slowerPercent = int(s1AvgReply / s2AvgReply * 100 - 100) if s1AvgReply > s2AvgReply else int(
            s2AvgReply / s1AvgReply * 100 - 100)

        # SERVE HTTP RESPONSE
        return render(request, 'whatsanalyzer/metrics.html', {'s1TotalMsg': s1TotalMsg,
                                                              's1TotalWords': s1TotalWords,
                                                              's1WPM': s1WPM,
                                                              's2TotalMsg': s2TotalMsg,
                                                              's2TotalWords': s2TotalWords,
                                                              's2WPM': s2WPM,
                                                              's1AvgReply': round(s1AvgReply / 60, 1),
                                                              's2AvgReply': round(s2AvgReply / 60, 1),
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
    else:
        return index(request)

def calculateMetrics(fileContentsList):
    # CLEAR HISTORY OF METRICS
    MessageStorage.clearMessageList()
    CountAnalysis.clearMetrics()

    # PERFORM ANALYSIS
    CountAnalysis.extractMessages(fileContentsList)
    CountAnalysis.calculateMetrics()

    # SET INITIALIZED IN COUNT_ANALYSIS
    CountAnalysis.setInitialized(True)


def readFile(request):
    uploadedFile = request.FILES['WhatsAppFile']
    fileContents = uploadedFile.read().decode('utf-8')
    fileContentsList = fileContents.split('\n')
    return fileContentsList


def stash(request):
    return render(request, 'whatsanalyzer/stash_new.html')
