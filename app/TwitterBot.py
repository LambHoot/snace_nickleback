import twitter #actually fine
import sys
import json
import csv
import threading
import traceback
import logging
import datetime
import random
import os
import time
from textgenrnn import textgenrnn

print("twitter auth starting")
keysCfg = open("config/keys.acecfg", "r")
lines = keysCfg.read().splitlines()
keysCfg.close()
apiKey = lines[0]
apiKeySecret = lines[1]
accessToken = lines[2]
accessTokenSecret = lines[3]
aceId = "896115303289155590"
lhId = "1197092900"
global lastMentionId
lastMentionId = ""
muted = False

textgen = textgenrnn(weights_path='lambhoot_weights.hdf5',
        vocab_path='lambhoot_vocab.json',
        config_path='lambhoot_config.json')

api = twitter.Api(
    consumer_key=apiKey,
    consumer_secret=apiKeySecret,
    access_token_key=accessToken,
    access_token_secret=accessTokenSecret,
    tweet_mode='extended')


def aceLog(message):
    timestamp = datetime.datetime.now().strftime("[%Y-%m-%d_%H:%M:%S]> ")
    print(timestamp + message)
    return timestamp + message

aceLog("twitter auth complete")


def logTimeline():
    # Note: GetHomeTimeline() includes ace's own tweets
    followingStatuses = api.GetHomeTimeline(count=20)
    # mock used for testing
    #    [ type('myTestTweet', (object,), 
    #       {'id_str': '112193458108155000008ehhhihihfihefihkfkekfekfekfe489',
    #           'full_text':'yo wassup'})() ]
    
    for status in followingStatuses:
        status_id = status.id_str
        status_full_text = status.full_text

        # reject if own tweet
        if (status.user.id_str == aceId):
            aceLog("Tweet id " + status_id + " is own, skipping.")
            continue

        # reject if already contained
        alreadyLogged = False
        with open("logs/twitter_log.csv", "r") as f:
            csvReader = csv.reader(f, delimiter=",")
            for row in csvReader:
                if len(row) > 1 and status_id in row[0]:
                    alreadyLogged = True
                    break
        if alreadyLogged:
            aceLog("Tweet id " + status_id + " already logged, skipping.")
            continue

        # reject if RT
        if status_full_text[0:2] == "RT":
            aceLog("Tweet id " + status_id + " is a retweet, skipping.")
            continue
        # reject if quote
        if status_full_text[0] == '"' and status_full_text[-1] == '"':
            aceLog("Tweet id " + status_id + " is a quote, skipping.")
            continue

        tweetData = [status_id, status_full_text]
        
        # write data to log file
        with open(r'logs/twitter_log.csv', 'a') as f:
            csvWriter = csv.writer(f)
            loggedTweet = False
            try:
                csvWriter.writerow(tweetData)
                loggedTweet = True
            except Exception as e:
                aceLog("Tweet id " + tweetData[0] + " has an encoding issue, skipping.")
            if loggedTweet :
                aceLog("Logged new Tweet:" +
                "\n id: " + tweetData[0]
                + "\n full_text: " + tweetData[1])

def sendTweet(text):
    tweetPosted = False
    if not muted:
        try:
            status = api.PostUpdate(text)
            tweetPosted = True
        except UnicodeDecodeError:
            aceLog("Tweet text could not be encoded.")
        if tweetPosted:
            aceLog("{0} just posted: {1}".format(status.user.name, status.text))
    else:
        aceLog("Muted, did not post tweet.")

def generateLhTweet():
    return textgen.generate(max_gen_length=140, n=1, return_as_list=True)[0]

def randomTweetTask():
    tweetChance = random.randint(1,100)
    if(tweetChance <= 40):

        try:
            #LH script based tweet
            lhtweet = generateLhTweet()
            sendTweet( lhtweet )
        except Exception as e:
            aceLog("ERROR Occured while performing sendTweet")
            logging.error(traceback.format_exc())

def respondTo(tweet, responseText):
    api.PostUpdate(responseText, in_reply_to_status_id=tweet.id_str, auto_populate_reply_metadata=True)

def responseTweetTask(sinceMentionId):
    mentions = None
    if len(sinceMentionId) > 0:
        mentions = api.GetMentions(count=10, since_id=sinceMentionId)
    else:
        mentions = api.GetMentions(count=1)

    sinceMentionId = mentions[0].id_str

    for mention in mentions:
        #LH script based tweet
        responseText = generateLhTweet()
        responsePosted = False
        if not muted:
            try:
                respondTo(mention, responseText)
                responsePosted = True
            except UnicodeDecodeError:
                aceLog("Reponse text could not be encoded.")
            if responsePosted:
                aceLog("Just posted reponse: '{0}' to {1}'s tweet '{2}'".format(responseText, mention.user.name, mention.text))
        else:
            aceLog("Muted, did not post response to {0}".format(mention.user.name))

def messageAdmin(message):
    api.PostDirectMessage(message, lhId)

def adminControlTask():
    # DirectMessage class:
    # https://python-twitter.readthedocs.io/en/latest/_modules/twitter/models.html#DirectMessage
    dms = []
    try:
        dms = api.GetDirectMessages()
    except Exception as e:
        aceLog("Couldn't get direct messages during adminControlTask")
        logging.error(traceback.format_exc())

    for dm in dms:
        aceLog("Got DIRECT MESSAGE '{0}' from {1}".format(dm.text, dm.sender_id))
        if dm.sender_id == lhId:
            adminCommand = dm.text
            aceLog("Got Admin command: {0}".format(adminCommand))
            if adminCommand == "mute":
                if not muted:
                    muted = True
                    messageAdmin(aceLog("admin, I am now muted"))
            if adminCommand == "unmute":
                if muted:
                    muted = False
                    messageAdmin(aceLog("admin, I am now unmuted"))
            if adminCommand == "shutdown":
                aceLog("Admin requested shutdown. Shutting down in 30 seconds.")
                time.sleep(30)
                os.system('shutdown -s')
    

# main Twitter Bot Tasks
def runTwitterBotTasks():
    
    sleepMinutes = 10
    threading.Timer(60.0 * sleepMinutes, runTwitterBotTasks).start()
    aceLog("Starting Twitter Bot Tasks")
    try:
        logTimeline()
    except Exception as e:
        aceLog("ERROR Occured while performing logTimeLine")
        logging.error(traceback.format_exc())
    
    # TODO: listen for admin commands via direct message
    try:
        adminControlTask()
    except Exception as e:
        aceLog("ERROR Occured while performing adminControlTask")
        logging.error(traceback.format_exc())

    # TODO: generate random chance for new tweets
    try:
        randomTweetTask()
    except Exception as e:
        aceLog("ERROR Occured while performing randomTweetTask")
        logging.error(traceback.format_exc())

    # TODO: detect @'s and generate replies to them
    try:
        responseTweetTask(lastMentionId)
    except Exception as e:
        aceLog("ERROR Occured while performing responseTweetTask")
        logging.error(traceback.format_exc())

    # etc

    aceLog("Completed Twitter Bot Tasks. Sleeping for " + str(sleepMinutes) + " minutes...")


runTwitterBotTasks()
