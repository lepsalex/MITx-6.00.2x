import random

def genEven():
    '''
    Returns a random even number x, where 0 <= x < 100
    '''
    # Generate list of all even numbers from 0 to 100
    return random.randrange(0, 100, 2)

print genEven()
