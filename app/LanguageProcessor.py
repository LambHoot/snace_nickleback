import csv
import Utils

vocabularyFilePath = "languageArtifacts/vocabulary.csv"
wordCountDictionary = {}

def initArtifacts():
    # clears the file if it already exists. This is desired behavior.
    vocabularyFile = open(vocabularyFilePath,"w+")
    # TODO: fill this with more artifacts to init

def processTextEntryForVocabulary(textEntry):
    # split text into "words"
    words = textEntry.split()
    for word in words:
        #if(Utils.checkIfCsvContainsId(word, 0, vocabularyFilePath)):
        if(word in wordCountDictionary):
            wordCountDictionary[word] += 1
            print("Found '" + word + "' already in vocabulary. Increased its count to " + str(wordCountDictionary[word]))
        else:
            # add new word
            wordCountDictionary[word] = 1
            print("Added new word '" + word + "' to vocabulary with count " + str(wordCountDictionary[word]))
            
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