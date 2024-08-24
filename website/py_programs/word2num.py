ones_place = {"zero": 0, "one": 1, "two": 2, "three": 3, "four": 4, 
              "five": 5, "six": 6, "seven": 7, "eight": 8, "nine": 9,
              "ten": 10, "eleven": 11, "twelve": 12, "thirteen": 13,
              "fourteen": 14, "fifteen": 15, "sixteen": 16, 
              "seventeen": 17, "eighteen": 18, "nineteen": 19}

tens_place = {"twenty": 20, "thirty": 30, "forty": 40, "fifty": 50,
              "sixty": 60, "seventy": 70, "eighty": 80, "ninety": 90}

hundreds_place = {"hundred": 10**2, "thousand": 10**3, "million": 10**6, "billion": 10**9,
                  "trillion": 10**12, "quadrillion": 10**15, "quintillion": 10**18}

def digit_in_word(word):
    digits = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    digits = [str(digit) for digit in digits]
    for char in word:
        if char in digits:
            return True
    return False

# Convert word form to numbers
# Works for numbers up to the quintillions
# Also works for dates like nineteen sixty three of twenty twenty four
def word2num(word):
    if digit_in_word(word):
        return word
    digits = word.split()
    num = 0
    
    has_ones = False
    has_tens = False
    tens = 0
    hundreds = 0
    for i in range(len(digits)):
        digit = digits[i]
        
        if digit in ones_place:
            # In a real number, there would never be a ones place or tens place next to another ones place
            # For example, there is never nine nineteen or four ninety
            # However, this is seen in a year such as nineteen forty one
            if (has_tens and ones_place[digit] >= 10) or has_ones:
                num *= 100
                
            num += ones_place[digit]
            # Store the tens place and hundreds place in case there is a thousand or million in front of them
            tens += ones_place[digit]
            hundreds += ones_place[digit]
            # Store boolean values to see if there has been a tens place or ones place
            has_ones = True
            has_tens = False
    
        elif digit in tens_place:
            if has_ones or has_tens:
                # If someone enters a year(eighteen twelve works different than one thousand eight hundred twelve)
                num *= 100
                has_tens = False
            else:
                has_tens = True
            
            num += tens_place[digit]
            tens += tens_place[digit]
            hundreds += tens_place[digit]
            has_ones = False
            
        elif digit in hundreds_place:
            if digit != "hundred" and hundreds:
                num += hundreds * hundreds_place[digit] - hundreds
                hundreds = 0
                tens = 0
            else:
                num += tens * hundreds_place[digit] - tens
                hundreds = tens * hundreds_place[digit]
                tens = 0
            has_ones = False
            has_tens = False
        
    return num