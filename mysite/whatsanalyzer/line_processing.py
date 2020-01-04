from dateutil.parser import parse
from re import findall, search


def extractDate(entireLine):

    try:
        lineDatetime = search(r'^.*?(am|pm)', entireLine).group()
        return parse(lineDatetime)
    except (AttributeError, ValueError):
        return None


def extractSender(entireLine):
    matchList = findall("m - .*?:", entireLine)
    try:
        if matchList:
            return matchList[0][4:-1]
        else:
            return None
    except IndexError:
        return None


def extractTextBody(entireLine):
    # Extract first half of redundant string
    matchList = findall(".*?m - .*?: ", entireLine)
    try:
        if matchList:
            return entireLine[len(matchList[0]):]
        else:
            return None
    except IndexError:
        return None