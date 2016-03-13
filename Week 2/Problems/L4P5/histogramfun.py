import pylab

# You may have to change this path
WORDLIST_FILENAME = "words.txt"

VOWELS = 'aeiou'

def loadWords():
    """
    Returns a list of valid words. Words are strings of uppercase letters.

    Depending on the size of the word list, this function may
    take a while to finish.
    """
    print "Loading word list from file..."
    # inFile: file
    inFile = open(WORDLIST_FILENAME, 'r', 0)
    # wordList: list of strings
    wordList = []
    for line in inFile:
        wordList.append(line.strip().lower())
    print "  ", len(wordList), "words loaded."
    return wordList

def vowelProps(wordlist):
    """
    Returns a list of proportions (vowels in words vs consonants)
    """
    propslist = []
    # For each word in wordList ...
    for word in wordList:
        length = float(len(word))
        vowelCount = 0.0
        # For each character in the word ...
        for c in word:
            if c in VOWELS:
                vowelCount += 1.0
        propslist.append(vowelCount / length)
    print "  ", len(propslist), "proportions calculated."
    return propslist

def plotVowelProportionHistogram(wordList, numBins=15):
    """
    Plots a histogram of the proportion of vowels in each word in wordList
    using the specified number of bins in numBins
    """
    data = vowelProps(wordList)
    pylab.hist(data, bins=numBins)
    pylab.title('Proportion of vowels vs. consonants per word in list of Words')
    pylab.xlabel('Proportion of Vowels in Word')
    pylab.ylabel('Occurances')
    pylab.show()


if __name__ == '__main__':
    wordList = loadWords()
    plotVowelProportionHistogram(wordList)
