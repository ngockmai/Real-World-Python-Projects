import random

def getIntegerFromUser(prompt):
    while True:
        number = input(prompt)
        try:
            number = int(number)
        except:
            print("Please enter a valid integer.")
            continue
        #everything is okay
        return number
    

myInteger = getIntegerFromUser("Enter an integer: ")
print(myInteger)

def getIntegerInRange(prompt, lowEnd, upToButNotIncludingHighEnd):
    while True:
        number = input(prompt)
        try
            number = int(number)
        except:
            print("Please enter a valid integer.")
            continue
        if number >= lowEnd and number < upToButNotIncludingHighEnd:
            return number
        else:
            print("Please enter a number between %d and %d." % (lowEnd, upToButNotIncludingHighEnd))