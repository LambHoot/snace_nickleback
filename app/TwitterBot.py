import twitter #actually fine
import sys
import json
import csv
import threading
import traceback
import logging
import datetime
import rnndriver
import random

print("twitter auth starting")
keysCfg = open("config/keys.acecfg", "r")
lines = keysCfg.read().splitlines()
keysCfg.close()
apiKey = lines[0]
apiKeySecret = lines[1]
accessToken = lines[2]
accessTokenSecret = lines[3]
aceId = "896115303289155590"

api = twitter.Api(
    consumer_key=apiKey,
    consumer_secret=apiKeySecret,
    access_token_key=accessToken,
    access_token_secret=accessTokenSecret,
    tweet_mode='extended')


def aceLog(message):
    timestamp = datetime.datetime.now().strftime("[%Y-%m-%d_%H:%M:%S]> ")
    print(timestamp + message)

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
    if True: #temporarily blocking tweets
        try:
            status = api.PostUpdate(text)
            tweetPosted = True
        except UnicodeDecodeError:
            aceLog("Tweet text could not be encoded.")
        if tweetPosted:
            aceLog("{0} just posted: {1}".format(status.user.name, status.text))

def randomTweetTask():
    tweetChance = random.randint(1,100)
    if(tweetChance <= 75):

        try:
            #LH script based tweet
            lhtweet = rnndriver.generateLhTweet()
            sendTweet( lhtweet )
        except Exception as e:
            aceLog("ERROR Occured while performing sendTweet")
            logging.error(traceback.format_exc())


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

    # TODO: generate random chance for new tweets
    randomTweetTask()

    # TODO: detect @'s and generate replies to them

    # etc

    aceLog("Completed Twitter Bot Tasks. Sleeping for " + str(sleepMinutes) + " minutes...")


runTwitterBotTasks()
