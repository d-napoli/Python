import json
import re

def romanNumbers(numberString):
    numberString = numberString.upper().replace(" ", "") # normalize the string to be all uppercase and without blank spaces
    p = "^M{0,4}(CM|CD|D?C{0,3})(XC|XL|L?X{0,3})(IX|IV|V?I{0,3})$" # regex pattern to match the string

    # the before of, means that if the letter comes before another one, it needs to be subtracted
    letterMeanings = { # object containing letters and values
        "I": { "value": 1, "rules": { "beforeOf": ['V', 'X'] } },
        "V": { "value": 5, "rules": { "beforeOf": [''] } },
        "X": { "value": 10, "rules": { "beforeOf": ['L', 'C'] } },
        "L": { "value": 50, "rules": { "beforeOf": [''] } },
        "C": { "value": 100, "rules": { "beforeOf": ['D', 'M'] } },
        "D": { "value": 500, "rules": { "beforeOf": [''] } },
        "M": { "value": 1000, "rules": { "beforeOf": [''] } }
    }

    m = len(numberString) # m equals the length of the informed string by the user
    i = 0 # initialize the i from the while as 0
    totalSum = 0 # initialize the total as 0
    
    if re.search(p, numberString): # if the informed string matches the roman string pattern
        while i < m: # while we still have characters to go on
            summed = False # initialize the control variable as false
            cur = numberString[i] # current letter
            if i + 1 < m: # more letters to come
                nextL = numberString[ i + 1] # next letter
                if i + 2 < m: # at least two letters more to come, so gotta check if the next two letters does not subtract each other
                    nextNextL = numberString[ i + 2 ] # two letters foward
                    if nextNextL in letterMeanings[ nextL ]['rules']['beforeOf']: # if the two next letter needs to be subtracted by the two letter foward
                        totalSum += letterMeanings[ cur ]['value'] # just sum the current letter value
                        i += 1 # increase to one te letter count
                        summed = True # set the conttrol variable to true, meaning that in this loop execution the values were already summed
                if not summed: # if it wasnt summed before, lets sum now
                    if letterMeanings[ cur ]['value'] < letterMeanings[ nextL ]['value']: # check if the values are lower
                        totalSum += letterMeanings[ nextL ]['value'] - letterMeanings[ cur ]['value'] # add to the new total the difference between the letters
                    else:
                        totalSum += letterMeanings[ cur ]['value'] + letterMeanings[ nextL ]['value'] # add to the new total the sum of the letters
                    i += 2 # always go two in two letters
            else: # if we dont have more letters to come
                totalSum += letterMeanings[ cur ]['value'] # add to the total the value of the last letter
                i += 1 # increase to one the i value so we can get out of the loop
        return json.dumps({'total': totalSum}) # return the total as json object
    else: # the string doesnt match the regex pattern
        return json.dumps({'error': "Informed string {} its not valid".format(numberString)}) # return json error informing that its not valid

# Examples
# numbers = "IVXLCDM" # Invalid
# numbers = "X" # 10
# numbers = "XVII" # 17
# numbers = "XIV" # 14
# numbers = "MCMLXIV" # 1964
# numbers = "MMCMXXXIX" # 2939
numbers = "XL    " # 40
print(romanNumbers(numbers)) # get the return of the function