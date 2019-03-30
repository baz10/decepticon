import time, string, random, re
from bad_words import BAD_WORDS
from datetime import datetime, timedelta
from pattern.en import parsetree, singularize
from pattern.search import search

# Random response sets
no_response = ["*scratch my head* :(", "How do I respond to that... :O", "I can be not-so-smart from time to time... :(", "Err... you know I'm not human, right? :O"]
error = ["Sorry I've got a little bit sick. BRB in 2 min :(", "Oops... 404 My Witty Mind Not Found :O", "Oops... My brain went MIA in the cloud, BRB in 2 :(", "Hmm... How should I respond to that... :O"]
looking_replies = ["Sure, give me a few seconds... B-)", "Scanning the world... :D", "Zoom zoom zoom...", "Going into the Food Cerebro... B-)", "Believe me, I'm a foodie, not an engineer... B-)"]
# END random response sets


def isAskingBotInformation(sentence):
    m = search('what *+ your name', sentence)
    if len(m) > 0:
        return True

    m = search('VP+ *+ your name', sentence)
    if len(m) > 0:
        return True

    m = search('who *+ your creator|dad|mom|father|mother|papa|mama|daddy|mommy', sentence)
    if len(m) > 0:
        return True

    m = search('VP+ *+ your creator|dad|mom|father|mother', sentence)
    if len(m) > 0:
        return True

    m = search('who made|create|wrote|built you', sentence)
    if len(m) > 0:
        return True

    return False

def badWords(string):
    for word in string.split(" "):
        if word.lower() in BAD_WORDS:
            return True
    return False


def oneOf(arr):
    rand_idx = random.randint(0,len(arr) - 1)
    return arr[rand_idx]    


def handleBotInfo(sentence):
    name = ["Decepticon... ah no, Decepticon The Bot :D", "I.am.the.legendary.Decepticon B-)", "I am the Supreme Leader.. Lol ... Jk... I am Decepticon The Bot! B-)", "You knew already *tsk tsk*"]
    creator = ["It's a mystery :O", "Are you sure you wanna know? ;)", "You are among the few who I tell: All I know about my creator is the initials SH :)", "It remains a mystery to me even :(","Only my Master can answer your question :(", "It was erased from my memory from the start :("]

    m = search('what *+ your name', sentence)
    if len(m) > 0:
        return oneOf(name)

    m = search('VP+ *+ your name', sentence)
    if len(m) > 0:
        return oneOf(name)

    m = search('who *+ your creator|dad|mom|father|mother|papa|mama|daddy|mommy', sentence)
    if len(m) > 0:
        return oneOf(creator)

    m = search('VP+ *+ your creator|dad|mom|father|mother|papa|mama|daddy|mommy', sentence)
    if len(m) > 0:
        return oneOf(creator)

    m = search('who *+ creates|created|gave_birth *+ you', sentence)
    if len(m) > 0:
        return oneOf(creator)

    return "Can you guess? ;)"
