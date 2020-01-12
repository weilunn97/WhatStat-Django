from datetime import datetime
from django.test import TestCase
from .line_processing import *

# Create your tests here.
class LineProcessingTestCase(TestCase):

    messageList = []

    def setUp(self):
        self.messageList.append('04/01/2016, 12:48 - Chris: Yes I saved your number are you proud of me')
        self.messageList.append('04/01/2016, 14:15 - Minhui Chin: ooo that phone is not bad uts gawains phone!')
        self.messageList.append('03/07/2019, 1:51 pm - weigee: nice waking up early')
        self.messageList.append('05/07/2019, 11:59 am - Pei Lun: Issokay just wanted to know where yall were at lol')
        self.messageList.append('23/08/2016, 9:35 pm - Wei Lun: Compassvale St lol. Relax can 🙄')
        self.messageList.append('26/08/2016, 10:16 am - Wei Lun: 2 small, 2med,1 large')

    def test_parse_date(self):
        self.assertEqual(extractDate(self.messageList[0]), datetime(2016, 1, 4, 12, 48))
        self.assertEqual(extractDate(self.messageList[1]), datetime(2016, 1, 4, 14, 15))
        self.assertEqual(extractDate(self.messageList[2]), datetime(2019, 7, 3, 13, 51))
        self.assertEqual(extractDate(self.messageList[3]), datetime(2019, 7, 5, 11, 59))
        self.assertEqual(extractDate(self.messageList[4]), datetime(2016, 8, 23, 21, 35))
        self.assertEqual(extractDate(self.messageList[5]), datetime(2016, 8, 26, 10, 16))

    def test_parse_sender(self):
        self.assertEqual(extractSender(self.messageList[0]), "Chris")
        self.assertEqual(extractSender(self.messageList[1]), "Minhui Chin")
        self.assertEqual(extractSender(self.messageList[2]), "weigee")
        self.assertEqual(extractSender(self.messageList[3]), "Pei Lun")
        self.assertEqual(extractSender(self.messageList[4]), "Wei Lun")
        self.assertEqual(extractSender(self.messageList[5]), "Wei Lun")

    def test_parse_textbody(self):
        self.assertEqual(extractTextBody(self.messageList[0]), "Yes I saved your number are you proud of me")
        self.assertEqual(extractTextBody(self.messageList[1]), "ooo that phone is not bad uts gawains phone!")
        self.assertEqual(extractTextBody(self.messageList[2]), "nice waking up early")
        self.assertEqual(extractTextBody(self.messageList[3]), "Issokay just wanted to know where yall were at lol")
        self.assertEqual(extractTextBody(self.messageList[4]), "Compassvale St lol. Relax can 🙄")
        self.assertEqual(extractTextBody(self.messageList[5]), "2 small, 2med,1 large")