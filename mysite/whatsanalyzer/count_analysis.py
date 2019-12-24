from .models import Message

import logging

logger = logging.getLogger(__name__)


class CountAnalysis():
    '''
    The CountAnalysis class serves as a utility class with purely static logic methods
    and attributes that we shall subsequently access and serve to the user on request

    Attributes:
        senderOneTotalMessages (int): Total messages sent by sender 1
        senderTwoTotalMessages (int): Total messages sent by sender 2
        senderOneTotalWords (int): Total words sent by sender 1
        senderTwoTotalWords (int): Total words sent by sender 2
        senderOneWordsPerMsg (int): Average words per message of sender 1
        senderTwoWordsPerMsg (int): Average words per message of sender 2
        senderList (List<String>): A list (containing only 2 elements)
        of the 2 parties in the conversation
    '''
    # General Metrics
    senderOneTotalMessages = 0
    senderTwoTotalMessages = 0

    senderOneTotalWords = 0
    senderTwoTotalWords = 0

    senderOneWordsPerMsg = 0
    senderTwoWordsPerMsg = 0

    senderList = []

    # Reply Timing Specific Metrics
    senderOneTimeStamp = []
    senderOneReplyTimingInMinutes = []

    senderTwoTimeStamp = []
    senderTwoReplyTimingInMinutes = []

    @staticmethod
    def calculateMetrics():
        '''
        Logic function to process all Message objects in our backend SQL DB.
        :return: None, performs in-place modification of General Metrics (above)
        '''

        # Setup pointer to first message in a string of messages
        firstMessage = None

        # Loop through all Message objects
        for msg in Message.objects.all():

            # 1. Add to Sender List
            if len(CountAnalysis.senderList) == 0:
                CountAnalysis.senderList.append(msg.messageSender)
            elif len(CountAnalysis.senderList) == 1:
                if msg.messageSender not in CountAnalysis.senderList:
                    CountAnalysis.senderList.append(msg.messageSender)

            # 2. Messages & Words Count
            if msg.messageSender == CountAnalysis.senderList[0]:
                CountAnalysis.senderOneTotalMessages += 1
                CountAnalysis.senderOneTotalWords += len(msg.messageText.split(' '))
            else:
                CountAnalysis.senderTwoTotalMessages += 1
                CountAnalysis.senderTwoTotalWords += len(msg.messageText.split(' '))

            # 3. Reply Timings Analysis
            if not firstMessage:
                firstMessage = msg
            elif firstMessage.messageSender != msg.messageSender:
                # Trigger reply timing analysis
                CountAnalysis.analyzeReplyTimings(firstMessage, msg)
                # Update firstMessage
                firstMessage = msg

        # 4. WPM Count
        try:
            CountAnalysis.senderOneWordsPerMsg = int(CountAnalysis.senderOneTotalWords / CountAnalysis.senderOneTotalMessages)
        except ZeroDivisionError:
            CountAnalysis.senderOneWordsPerMsg = 0   
        try:
            CountAnalysis.senderTwoWordsPerMsg = int(CountAnalysis.senderTwoTotalWords / CountAnalysis.senderTwoTotalMessages)
        except ZeroDivisionError:
            CountAnalysis.senderTwoWordsPerMsg = 0

    @staticmethod
    def analyzeReplyTimings(mOne, mTwo):
        '''
        Processes the reply timing of the sender who sent the message "mTwo", and stores it
        into the Reply Timing Specific Metrics attributes of this class.

        :param mOne (Message): First message from the "earlier" sender
        :param mTwo (Message): First message from the "later" sender
        :return: None, None, performs in-place modification of Reply Timing Specific Metrics (above)
        '''
        # Do not process further if messageList is not filled
        if len(CountAnalysis.senderList) < 2: return

        # Get reply timings difference
        try:
            dateDiff = mTwo.messageDate - mOne.messageDate
            dateDiffInMins = dateDiff.seconds / 60
            if dateDiffInMins < 0:
                raise ValueError("Negative DateDiff")
        except:
            print("dateDiff FAILED")
            print(f"mOne : {mOne}")
            print(f"mTwo : {mTwo}")

        if mTwo.messageSender == CountAnalysis.senderList[0]:
            CountAnalysis.senderOneTimeStamp.append(mTwo.messageDate)
            CountAnalysis.senderOneReplyTimingInMinutes.append(dateDiffInMins)
        else:
            CountAnalysis.senderTwoTimeStamp.append(mTwo.messageDate)
            CountAnalysis.senderTwoReplyTimingInMinutes.append(dateDiffInMins)

    @staticmethod
    def debugFunction():
        print(CountAnalysis.senderOneTotalMessages)
        print(CountAnalysis.senderOneTotalWords)
        print(CountAnalysis.senderOneWordsPerMsg)
        print(CountAnalysis.senderOneTimeStamp)
        print(CountAnalysis.senderOneReplyTimingInMinutes)
        print("\n\n")
        print(CountAnalysis.senderTwoTotalMessages)
        print(CountAnalysis.senderTwoTotalWords)
        print(CountAnalysis.senderTwoWordsPerMsg)
        print(CountAnalysis.senderTwoTimeStamp)
        print(CountAnalysis.senderTwoReplyTimingInMinutes)
