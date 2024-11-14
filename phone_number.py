import math
import pickle

# Phone keypad mapping for letters to numbers
keypad_mapping = {
    '2': 'ABC', '3': 'DEF', '4': 'GHI',
    '5': 'JKL', '6': 'MNO', '7': 'PQRS',
    '8': 'TUV', '9': 'WXYZ'
}

class ListNode:
    """Node for separate chaining in hash table."""
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.next = None

class HashTable:
    def __init__(self, size):
        self.size = size
        self.table = [None] * size  # Array of linked lists for separate chaining

    def hash_function(self, key):
        """Hash function using multiplication method."""
        A = 0.6180  # Approximation of the golden ratio
        fractional_part = (key * A) % 1
        return math.floor(self.size * fractional_part)

    def insert(self, key, value):
        """Insert a key-value pair into the hash table."""
        index = self.hash_function(key)
        if self.table[index] is None:
            self.table[index] = ListNode(key, value)
        else:
            current = self.table[index]
            while current.next is not None:
                current = current.next
            current.next = ListNode(key, value)

    def search(self, key):
        """Search for a key in the hash table and return the associated value."""
        index = self.hash_function(key)
        current = self.table[index]
        results = []
        while current is not None:
            if current.key == key:
                results.append(current.value)
            current = current.next
        return results  # Return list of matches

# Define separate hash tables for different number lengths
table_size = 5003
hash_tables = {
    10: HashTable(table_size),  # 10-digit numbers
    7: HashTable(table_size),   # 7-digit numbers
    3: HashTable(table_size),   # 3-digit exchanges
    4: HashTable(table_size)    # 4-digit numbers
}

def word_to_number(word):
    """Convert a word to a numeric phone number based on keypad mapping."""
    number = ""
    for char in word.upper():
        for key, letters in keypad_mapping.items():
            if char in letters:
                number += key
                break
    return int(number)

def insert_word(word):
    """Insert a word into the appropriate hash tables based on its length."""
    number = word_to_number(word)
    length = len(str(number))
    if length in hash_tables:
        hash_tables[length].insert(number, word)

def load_words_from_file(filename="all_words.txt"):
    """Load words from a file and insert them into the hash tables."""
    try:
        with open(filename, 'r') as file:
            for line in file:
                word = line.strip()
                if 2 <= len(word) <= 10:  # Only words with 2 to 10 letters
                    insert_word(word)
        print("All words loaded successfully.")
    except FileNotFoundError:
        print(f"File '{filename}' not found.")

def search_phone_number(phone_number):
    """Search for a word-based representation of a phone number."""
    phone_number = int(phone_number)
    
    # Check 10-digit representation
    if phone_number >= 10**9:  # Ensure it's a 10-digit number
        results = hash_tables[10].search(phone_number)
        if results:
            return [f"1-{word}" for word in results]
    
    # Check 7-digit representation
    exchange, number = divmod(phone_number, 10000)
    results = hash_tables[7].search(exchange * 10000 + number)
    if results:
        return [f"{exchange}-{word}" for word in results]
    
    # Check 3-digit exchange and 4-digit number separately
    exchange_results = hash_tables[3].search(exchange)
    number_results = hash_tables[4].search(number)
    if exchange_results and number_results:
        return [f"{exchange}-{ex}-{num}" for ex in exchange_results for num in number_results]
    
    # Only 3-digit exchange
    if exchange_results:
        return [f"{exchange}-{word}-{number}" for word in exchange_results]
    
    # Only 4-digit number
    if number_results:
        return [f"{exchange}-{number}" for word in number_results]

    # Default: return number in standard format
    return [f"1-{exchange}-{number}"]

# Load words from all_words.txt
load_words_from_file()

# Example usage of search_phone_number
phone_number_to_search = "6157862243"  # Replace with the phone number you want to search
print(search_phone_number(phone_number_to_search))
