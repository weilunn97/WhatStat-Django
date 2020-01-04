from .count_analysis import *
from datetime import timedelta
from django.shortcuts import render, redirect
import json
import pdb

# TODO
"""
2. Retrieve all user files from Firebase Storage
3. Create ListView of FileName + FileDate
4. Allow user to select the file for analysis
5. Perform redirect to /metrics/ using this file
"""


def index(request):
    # UPON SUCCESSFUL UPLOAD
    if request.method == "POST" and request.FILES:
        # Retrieve the uploaded file
        uploadedFile = request.FILES['WhatsAppFile']
        fileContents = uploadedFile.read().decode('utf-8')
        fileContentsList = fileContents.split('\n')

        # CLEAR EXISTING MESSAGES AND METRICS, IF ANY
        MessageStorage.clearMessageList()
        CountAnalysis.clearMetrics()

        # PERFORM ANALYSIS
        CountAnalysis.extractMessages(fileContentsList)
        CountAnalysis.calculateMetrics()

        # Redirect to metrics
        return redirect('metrics/')

    # Else, serve the page as per usual
    return render(request, 'whatsanalyzer/homepage_new.html')


def charts(request):

    # DEBUG INFO
    # CountAnalysis.debugPrint()

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
    # RETRIEVE METRICS FROM CountAnalysis
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
                               f"good friend and chat buddy you'll always wanna keep around!"

        # SMALL DIFF
        else:
            leftMessageText = f"Well, well, {s1}, nothing much to see here I guess, both you guys have sent nearly the same " \
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
            leftWordsText = f"You're quite a chatty person, {s1}, I hope {s2} is okay with it! Well, do keep up " \
                            f"this excellent chemistry between the both of you!"
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
            rightWordsText = f"You're quite a chatty person, {s2}! Do keep up this excellent chemistry between the both of you!"

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
            rightReplyText = f"Ahh, {s2}, you must hate waiting for {s1}'s texts, don't you? But do give {s1} just that little understanding!"
        # SMALL DIFF
        else:
            leftReplyText = f"Seems like quite a healthy interaction going on here, nothing to worry about there, {s1}!"
            rightReplyText = f"Seems like quite a healthy interaction going on here, nothing to worry about there, {s2}!"
    else:
        # LARGE DIFF
        if s2AvgReply / s1AvgReply > 1.25:
            leftReplyText = f"Ahh, {s1}, you must hate waiting for {s2}'s texts, don't you? But do give {s2} just that little understanding!"
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


def stash(request):
    return render(request, 'whatsanalyzer/stash.html')


def upload(request, requestFiles):
    return render(request, 'whatsanalyzer/upload.html', {'requestFiles': requestFiles})
