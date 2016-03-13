def stdDevOfLengths(L):
    """
    L: a list of strings

    returns: float, the standard deviation of the lengths of the strings,
      or NaN if L is empty.
    """

    # Get word lengths and put them into a list
    wordInts = []
    for word in L:
        wordInts.append(len(word))

    # Calculate mean (else error out gracefully)
    try:
        mean = sum(wordInts)/float(len(wordInts))
    except ZeroDivisionError:
        return float('NaN')

    # Calculate STDEV
    listSum = 0.0
    for num in wordInts:
        listSum += (num - mean)**2

    # Try to return the STDEV
    return (listSum/len(wordInts))**0.5

# Test excecution
L = ['apples', 'oranges', 'kiwis', 'pineapples']
N = []
print stdDevOfLengths(L)
print stdDevOfLengths(N)
