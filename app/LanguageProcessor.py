import csv
import Utils

vocabularyFilePath = "languageArtifacts/vocabulary.csv"
wordCountDictionary = {}
global totalWords
global totalUniqueWords

def initArtifacts():
    # clears the file if it already exists. This is desired behavior.
    vocabularyFile = open(vocabularyFilePath,"w+")
    # TODO: fill this with more artifacts to init

def processTextEntryForVocabulary(textEntry):
    totalWords = 0
    totalUniqueWords = 0

    # split text into "words"
    words = textEntry.split()

    for i in range(len(words)):
        word = words[i]
        #if(Utils.checkIfCsvContainsId(word, 0, vocabularyFilePath)):
        if(word in wordCountDictionary):
            wordCountDictionary[word] += 1
            totalWords += 1
            print("Found '" + word + "' already in vocabulary. Increased its count to " + str(wordCountDictionary[word]))
        else:
            # add new word
            wordCountDictionary[word] = 1
            totalWords += 1
            totalUniqueWords += 1
            print("Added new word '" + word + "' to vocabulary with count " + str(wordCountDictionary[word]))
        
        # TODO: iterate through the rest of the words past current word
        # then start building some sort of ngram structures (probably a list of ngram datas)
        # finally, export the ngrams to csv files



            
def createVocabularyFromLog(logFileName):
    print("creating the vocabulary")

    with open("logs/" + logFileName + ".csv", "r") as logFile:
        logReader = csv.reader(logFile, delimiter=",")
        for row in logReader:
            if len(row) < 1 or len(row[1]) < 1:
                continue
            processTextEntryForVocabulary(row[1])
    
    # export to csv
    print("Exporting word count data to csv")
    with open(r'' + vocabularyFilePath, 'a') as f:
        vocabularyWriter = csv.writer(f)
        for word in wordCountDictionary:
            vocabularyWriter.writerow([word, wordCountDictionary[word]])


def processLog(logFileName):
    print('processing log...')
    initArtifacts()

    createVocabularyFromLog(logFileName)
    # createNGramsFromVocabulary



# temp main

processLog('twitter_log')