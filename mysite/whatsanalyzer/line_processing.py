'''
This raw-string-processing utility module serves a single purpose : to extract the
following 3 attributes from each message in a WhatsApp conversation text file.
1. Message Datetime
2. Message Sender
3. Message Content/Text
'''

from dateutil.parser import parse
from re import findall, search


def extractDate(entireLine):
    '''
    Extracts a Python naive datetime object from the line.
    :param entireLine:
            The line we obtain after performing str.split('\n') on the entire file contents
    :return:
            Returns a :class:`datetime.datetime` object
    '''

    try:
        # AM/PM TIMESTAMP
        lineDatetime = search(r'^.*?(am|pm)', entireLine).group()
        return parse(lineDatetime, dayfirst=True)
    except (AttributeError, ValueError):
        # 24-HOUR TIMESTAMP
        try:
            lineDatetime = search(r'^.*?(-)', entireLine).group()
            return parse(lineDatetime[:-2], dayfirst=True)
        except (AttributeError, ValueError):
            return None


def extractSender(entireLine):
    '''
    Extracts the message sender's name, as a string, from the line.
    :param entireLine:
            The line we obtain after performing str.split('\n') on the entire file contents
    :return:
            Returns the sender's name as a string
    '''

    matchList = findall("m - .*?:", entireLine)
    try:
        if matchList:
            return matchList[0][4:-1]
        else:
            matchList = findall(" - .*?:", entireLine)
            if matchList:
                return matchList[0][3:-1]
            else:
                return None
    except IndexError:
        return None


def extractTextBody(entireLine):
    '''
    Extracts the message contents, as a string, from the line.
    :param entireLine:
            The line we obtain after performing str.split('\n') on the entire file contents
    :return:
            Returns the message contents as a string
    '''

    # Extract first half of redundant string
    matchList = findall(".*?m - .*?: ", entireLine)
    try:
        if matchList:
            return entireLine[len(matchList[0]):]
        else:
            matchList = findall(".* - .*?: ", entireLine)
            if matchList:
                return entireLine[len(matchList[0]):]
            else:
                return None
    except IndexError:
        return None
