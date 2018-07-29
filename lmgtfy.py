import urllib.parse

def lmgtfy(query):
    return "Let me Google that for you... http://lmgtfy.com/?q=" + urllib.parse.quote_plus(query)
