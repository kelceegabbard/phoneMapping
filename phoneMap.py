from itertools import product

# map digits to letters 
digit_to_letters = {
    '2': 'ABC', '3': 'DEF', '4': 'GHI', '5': 'JKL', '6': 'MNO',
    '7': 'PQRS', '8': 'TUV', '9': 'WXYZ'
}

# working on loading, this doesnt work yet 
def load_words(filename):
    with open(filename, 'r') as f:
        return set(word.strip().upper() for word in f if word.strip())

# valid words for testing, get rid of this after loding zip file correctly
valid_words = {"ABNORMALLY", "AMERICA", "RUN", "ACHE", "ACID", "CAGE", "WAX", "WAY", "THAT"}

# converts string into list of possible letter combos 
def possible_letters(digits):    
    letters_list = [digit_to_letters[d] for d in digits if d in digit_to_letters]
    return letters_list

# valid word combos for digit string from input
def generate_combo(digits):
    letters_list = possible_letters(digits)
    combos = [''.join(letters) for letters in product(*letters_list)]
    return [word for word in combos if word in valid_words]

#finds the word rep for inputted phone number
def find_word_rep(phone_num):
    
    #break num into 3 parts for easier checking 
    area, exchange, num = phone_num[:3], phone_num[3:6], phone_num[6:]
    
    # check 10 digit rep 
    full_10_digit = generate_combo(phone_num)
    if full_10_digit:
        return [f"1-{word}" for word in full_10_digit]
    
    # check 7 digit rep 
    full_7_digit = generate_combo(exchange + num)
    if full_7_digit:
        return [f"1-{area}-{word}" for word in full_7_digit]
    
    # check for 3 & 4 digit rep 

    #generate for exchange part of the phone number 
    three_digit_words = generate_combo(exchange)

    #generate for num part of phone number 
    four_digit_words = generate_combo(num)

    #if exchange and num have valid reps, return all combos 
    if three_digit_words and four_digit_words:
        return [f"1-{area}-{ex}-{num}" for ex in three_digit_words for num in four_digit_words]
    
    #if only exchange has valid reps
    if three_digit_words:
        return [f"1-{area}-{ex}-{num}" for ex in three_digit_words]
    
    #if only num has valid reps 
    if four_digit_words:
        return [f"1-{area}-{exchange}-{num}" for num in four_digit_words]
    
    #if no valid combos are found 
    return [f"1-{area}-{exchange}-{num}"]


def main():
    phone_num = input("Enter a phone number: ")
    
    # check if the user has input an  11 digit num, already having the leading 1
    if len(phone_num) == 11 and phone_num[0] == "1":
        phone_num = phone_num[1:]  # get rid of leading 1 
    elif not phone_num.isdigit() or len(phone_num) < 7 or len(phone_num) > 10:
        print("Invalid phone number. Enter a 7-10 digit number.")
        return

    
    # Find word representation
    result = find_word_rep(phone_num)
    print("Possible word representations:")
    for item in result:
        print(item)

main()
