from re import findall
from datetime import datetime


def extractDate(entireLine):
    # PM times (hours) are non zero-padded
    if entireLine[18] == "m":
        return parseDateString(entireLine[:19])
    # AM times (hours) are zero-padded
    elif entireLine[19] == "m":
        return parseDateString(entireLine[:20])
    # For multi-line message bodies
    else:
        return None


def parseDateString(date):
    try:
        date = date.replace('pm', 'PM', 1).replace('am', 'AM')
        return datetime.strptime(date, '%d/%m/%Y, %H:%M %p')
    except ValueError:
        return None


def extractSender(entireLine):
    matchList = findall("m - .*?:")
    try:
        if matchList:
            return matchList[0][4:-1]
        else:
            return None
    except IndexError:
        return None


def extractTextBody(entireLine):
    # Extract first half of redundant string
    matchList = findall(".*?m - .*?: ")
    try:
        if matchList:
            return entireLine[len(matchList[0]):]
        else:
            return None
    except IndexError:
        return None


def countWords(textBody):
    return len(textBody.split(' '))
