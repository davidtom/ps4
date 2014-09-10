# 6.00 Problem Set 4
#
# Caesar Cipher Skeleton
#
import string
import random

WORDLIST_FILENAME = "words.txt"

# -----------------------------------
# Helper code
# (Created by MIT6 Team)
def load_words():
    """
    Returns a list of valid words. Words are strings of lowercase letters.
    
    Depending on the size of the word list, this function may
    take a while to finish.
    """
    print "Loading word list from file..."
    # inFile: file
    inFile = open(WORDLIST_FILENAME, 'r', 0)
    # line: string
    line = inFile.readline()
    # wordlist: list of strings
    wordlist = line.split()
    print "  ", len(wordlist), "words loaded."
    return wordlist

wordlist = load_words()

def is_word(wordlist, word):
    """
    Determines if word is a valid word.

    wordlist: list of words in the dictionary.
    word: a possible word.
    returns True if word is in wordlist.

    Example:
    >>> is_word(wordlist, 'bat') returns
    True
    >>> is_word(wordlist, 'asdf') returns
    False
    """
    word = word.lower()
    word = word.strip(" !@#$%^&*()-_+={}[]|\:;'<>?,./\"")
    return word in wordlist

def random_word(wordlist):
    """
    Returns a random word.

    wordlist: list of words  
    returns: a word from wordlist at random
    """
    return random.choice(wordlist)

def random_string(wordlist, n):
    """
    Returns a string containing n random words from wordlist

    wordlist: list of words
    returns: a string of random words separated by spaces.
    """
    return " ".join([random_word(wordlist) for _ in range(n)])

def random_scrambled(wordlist, n):
    """
    Generates a test string by generating an n-word random string
    and encrypting it with a sequence of random shifts.

    wordlist: list of words
    n: number of random words to generate and scamble
    returns: a scrambled string of n random words


    NOTE:
    This function will ONLY work once you have completed your
    implementation of apply_shifts!
    """
    s = random_string(wordlist, n) + " "
    shifts = [(i, random.randint(0, 26)) for i in range(len(s)) if s[i-1] == ' ']
    return apply_shifts(s, shifts)[:-1]

def get_fable_string():
    """
    Returns a fable in encrypted text.
    """
    f = open("fable.txt", "r")
    fable = str(f.read())
    f.close()
    return fable


# (end of helper code)
# -----------------------------------

#
# Problem 1: Encryption
#
def build_coder(shift):
    """
    Returns a dict that can apply a Caesar cipher to a letter.
    The cipher is defined by the shift value. Ignores non-letter characters
    like punctuation and numbers.

    shift: -27 < int < 27
    returns: dict

    Example:
    >>> build_coder(3)
    {' ': 'c', 'A': 'D', 'C': 'F', 'B': 'E', 'E': 'H', 'D': 'G', 'G': 'J',
    'F': 'I', 'I': 'L', 'H': 'K', 'K': 'N', 'J': 'M', 'M': 'P', 'L': 'O',
    'O': 'R', 'N': 'Q', 'Q': 'T', 'P': 'S', 'S': 'V', 'R': 'U', 'U': 'X',
    'T': 'W', 'W': 'Z', 'V': 'Y', 'Y': 'A', 'X': ' ', 'Z': 'B', 'a': 'd',
    'c': 'f', 'b': 'e', 'e': 'h', 'd': 'g', 'g': 'j', 'f': 'i', 'i': 'l',
    'h': 'k', 'k': 'n', 'j': 'm', 'm': 'p', 'l': 'o', 'o': 'r', 'n': 'q',
    'q': 't', 'p': 's', 's': 'v', 'r': 'u', 'u': 'x', 't': 'w', 'w': 'z',
    'v': 'y', 'y': 'a', 'x': ' ', 'z': 'b'}
    (The order of the key-value pairs may be different.)
    """

    coder = {} #creates empty dict to be used
    letters=['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z',' ']
    for letter in letters: #iterates over above letters
        cipher_number = (letters.index(letter)+shift)%27 #gives the positional location of the original letters new shifted letter, according to the shift value (see wikipedia article on caesar cipher for formula)
        cipher_letter = letters[cipher_number] #applies positional value to give the actual shifted letter, which is assigned to cipher_letter variable
        coder[letter]=cipher_letter #in the coder dictionary, the original letter is mapped to the shifted letter
        if letter != ' ': #checks to make sure the letter is not a space (space is only mapped to lower case letters)
            coder[letter.upper()]=cipher_letter.upper() #creates matching upper case key:value pairs in the coder dictionary
    return coder

def build_encoder(shift):
    """
    Returns a dict that can be used to encode a plain text. For example, you
    could encrypt the plain text by calling the following commands
    >>>encoder = build_encoder(shift)
    >>>encrypted_text = apply_coder(plain_text, encoder)
    
    The cipher is defined by the shift value. Ignores non-letter characters
    like punctuation and numbers.

    shift: 0 <= int < 27
    returns: dict

    Example:
    >>> build_encoder(3)
    {' ': 'c', 'A': 'D', 'C': 'F', 'B': 'E', 'E': 'H', 'D': 'G', 'G': 'J',
    'F': 'I', 'I': 'L', 'H': 'K', 'K': 'N', 'J': 'M', 'M': 'P', 'L': 'O',
    'O': 'R', 'N': 'Q', 'Q': 'T', 'P': 'S', 'S': 'V', 'R': 'U', 'U': 'X',
    'T': 'W', 'W': 'Z', 'V': 'Y', 'Y': 'A', 'X': ' ', 'Z': 'B', 'a': 'd',
    'c': 'f', 'b': 'e', 'e': 'h', 'd': 'g', 'g': 'j', 'f': 'i', 'i': 'l',
    'h': 'k', 'k': 'n', 'j': 'm', 'm': 'p', 'l': 'o', 'o': 'r', 'n': 'q',
    'q': 't', 'p': 's', 's': 'v', 'r': 'u', 'u': 'x', 't': 'w', 'w': 'z',
    'v': 'y', 'y': 'a', 'x': ' ', 'z': 'b'}
    (The order of the key-value pairs may be different.)

    HINT : Use build_coder.
    """

    return build_coder(shift) #builds encoding dictionary using given shift value

def build_decoder(shift):
    """
    Returns a dict that can be used to decode an encrypted text. For example, you
    could decrypt an encrypted text by calling the following commands
    >>>encoder = build_encoder(shift)
    >>>encrypted_text = apply_coder(plain_text, encoder)
    >>>decrypted_text = apply_coder(plain_text, decoder)
    
    The cipher is defined by the shift value. Ignores non-letter characters
    like punctuation and numbers.

    shift: 0 <= int < 27
    returns: dict

    Example:
    >>> build_decoder(3)
    {' ': 'x', 'A': 'Y', 'C': ' ', 'B': 'Z', 'E': 'B', 'D': 'A', 'G': 'D',
    'F': 'C', 'I': 'F', 'H': 'E', 'K': 'H', 'J': 'G', 'M': 'J', 'L': 'I',
    'O': 'L', 'N': 'K', 'Q': 'N', 'P': 'M', 'S': 'P', 'R': 'O', 'U': 'R',
    'T': 'Q', 'W': 'T', 'V': 'S', 'Y': 'V', 'X': 'U', 'Z': 'W', 'a': 'y',
    'c': ' ', 'b': 'z', 'e': 'b', 'd': 'a', 'g': 'd', 'f': 'c', 'i': 'f',
    'h': 'e', 'k': 'h', 'j': 'g', 'm': 'j', 'l': 'i', 'o': 'l', 'n': 'k',
    'q': 'n', 'p': 'm', 's': 'p', 'r': 'o', 'u': 'r', 't': 'q', 'w': 't',
    'v': 's', 'y': 'v', 'x': 'u', 'z': 'w'}
    (The order of the key-value pairs may be different.)

    HINT : Use build_coder.
    """
    shift = shift *-1 #function takes positive integers, but decoding is done by shift left (negative)
    return build_coder(shift) #builds decoding dictionary

def apply_coder(text, coder):
    """
    Applies the coder to the text. Returns the encoded text.

    text: string
    coder: dict with mappings of characters to shifted characters
    returns: text after mapping coder chars to original text

    Example:
    >>> apply_coder("Hello, world!", build_encoder(3))
    'Khoor,czruog!'
    >>> apply_coder("Khoor,czruog!", build_decoder(3))
    'Hello, world!'
    """

    cipher_text = ''
    for character in text: #goes through each character in text
        if character in coder: #if the character is in the coder dictionary (ie a space, lowercase letter, or uppercase letter)
            cipher_text += coder[character] #the corresponding value of the coder dictionary is added (applying shift)
        else: #if the character is not in the coder dictionary
            cipher_text += character #it is added as is
    return cipher_text #when every character of text has been gone through, the encrypted text is returned

####Testing apply_coder()
##plain_text = 'Hello, world!'
##print 'Plain text: %s' % plain_text
##encoder = build_encoder(3)
##encrypted_text = apply_coder(plain_text, encoder)
##print 'Encrypted text: %s' % encrypted_text
##decoder = build_decoder(3)
##decrypted_text = apply_coder(encrypted_text, decoder)
##print 'Decrypted text: %s' % decrypted_text

def apply_shift(text, shift):
    """
    Given a text, returns a new text Caesar shifted by the given shift
    offset. The empty space counts as the 27th letter of the alphabet,
    so spaces should be replaced by a lowercase letter as appropriate.
    Otherwise, lower case letters should remain lower case, upper case
    letters should remain upper case, and all other punctuation should
    stay as it is.
    
    text: string to apply the shift to
    shift: amount to shift the text
    returns: text after being shifted by specified amount.

    Example:
    >>> apply_shift('This is a test.', 8)
    'Apq hq hiham a.'
    """
    return apply_coder(text, build_encoder(shift)) #Assuming a shift is only for encoding, this simply encodes the text by the given shift

####Testing apply_shift()
##plain_txt = 'This is a test.'
##print 'Original text: %s' % plain_txt
##encr_txt = apply_shift(plain_txt, 8)
##print 'Encrypted text: %s' % encr_txt
##print 'Decrypted text: %s' % apply_coder(encr_txt, build_decoder(8))
  
#
# Problem 2: Codebreaking.
#
def find_best_shift(wordlist, text):
    """
    Decrypts the encoded text and returns the plaintext.

    text: string
    returns: 0 <= int 27

    Example:
    >>> s = apply_coder('Hello, world!', build_encoder(8))
    >>> s
    'Pmttw,hdwztl!'
    >>> find_best_shift(wordlist, s) returns
    8
    >>> apply_coder(s, build_decoder(8)) returns
    'Hello, world!'
    """

    max_words_found = 0 #integer that will count the number of valid words found in each shift
    best_shift = 0 #when Valid_words_found is greater than the previous value, the shift will be assigned to this
    for shift in range(28): #Test each decode value from 0 to 27
        #print "current shift is: " , shift
        shifted_text = apply_coder(text, build_decoder(shift)) #decode the text
        #print "shifted text: %s" % shifted_text
        decrypted_words = shifted_text.split() #split the decoded text into individual words by spaces
        #print 'decrypted_words: %s' % decrypted_words
        valid_word_count = 0 
        for word in decrypted_words: #counts number of valid words produced by shift
            if is_word(wordlist, word):
                valid_word_count += 1
                #print "Valid word count: %d" % valid_word_count
        if valid_word_count > max_words_found: #if there are more valid words in this shift than the last:
            max_words_found = valid_word_count #it sets the number of words to the new max
            best_shift = shift #and the current shift to the best shift
        #print "max_words_found is: " , max_words_found
        #print "Best shift is: " , best_shift
    return best_shift #returns the shift that produced the most words after all shifts have been tried
            
####Testing find_best_shift()
##text = 'Pmttw,hdwztl!'
##bs = find_best_shift(wordlist, text)
##print 'Best shift is: ' , bs

####Can change this at will:
##text = random_string(wordlist, 4)
##for shift in (3, 6, 8, 14, 25):
##    #Mapping the process (dont change):
##    print "Original text: " , text
##    print "Shift: " , shift
##    encrypted_text = apply_shift(text, shift)
##    print "Encrypted text: ", encrypted_text
##    bs = find_best_shift(wordlist, encrypted_text)
##    print "Best shift: " , bs
##    decrypted_text = apply_coder(encrypted_text, build_decoder(bs))
##    print "Decrypted text: " , decrypted_text
   
#
# Problem 3: Multi-level encryption.
#
def apply_shifts(text, shifts):
    """
    Applies a sequence of shifts to an input text.

    text: A string to apply the Ceasar shifts to 
    shifts: A list of tuples containing the location each shift should
    begin and the shift offset. Each tuple is of the form (location,
    shift) The shifts are layered: each one is applied from its
    starting position all the way through the end of the string.  
    returns: text after applying the shifts to the appropriate
    positions

    Example:
    >>> apply_shifts("Do Androids Dream of Electric Sheep?", [(0,6), (3, 18), (12, 16)])
    'JufYkaolfapxQdrnzmasmRyrpfdvpmEurrb?'
    """

    #Easiest way to think about this problem is that it applies the shift from the start of the tupe onward,
    #so we will break up the text into two pieces (determined by the start of the tupe) and encrypt the second part
    #To finish, the first part will be added to the (newly encrypted) second part and either passed through again
    # or returned
    
    for tup in shifts: #goes through the tups specifying the shift locations and shifts
        first_segment = text[:tup[0]] #breaks text up from start to start of tup location
        #print 'first segment: ' , first_segment
        second_segment = text[tup[0]:] #breaks text up from start of tup location to end
        #print 'second segment: ' , second_segment
        text = first_segment + apply_shift(second_segment, tup[1]) #adds the first segment of the text to the second segment (which is encrypted by the number of shifts designated by the tupes)
        #print 'shifted text:' , text
    return text
    
#### Testing apply_shifts
##print 'apply_shifts("Do Androids Dream of Electric Sheep?", [(0,6), (3, 18), (12, 16)]):'
##print apply_shifts("Do Androids Dream of Electric Sheep?", [(0,6), (3, 18), (12, 16)])
 
#
# Problem 4: Multi-level decryption.
#

def find_best_shifts(wordlist, text):
    """
    Given a scrambled string, returns a shift key that will decode the text to
    words in wordlist, or None if there is no such key.

    Hint: Make use of the recursive function
    find_best_shifts_rec(wordlist, text, start)

    wordlist: list of words
    text: scambled text to try to find the words for
    returns: list of tuples.  each tuple is (position in text, amount of shift)
    
    Examples:
    >>> s = random_scrambled(wordlist, 3)
    >>> s
    'eqorqukvqtbmultiform wyy ion'
    >>> shifts = find_best_shifts(wordlist, s)
    >>> shifts
    [(0, 25), (11, 2), (21, 5)]
    >>> apply_shifts(s, shifts)
    'compositor multiform accents'
    >>> s = apply_shifts("Do Androids Dream of Electric Sheep?", [(0,6), (3, 18), (12, 16)])
    >>> s
    'JufYkaolfapxQdrnzmasmRyrpfdvpmEurrb?'
    >>> shifts = find_best_shifts(wordlist, s)
    >>> print apply_shifts(s, shifts)
    Do Androids Dream of Electric Sheep?
    """
    #TO DO.
    
    global shifts_list
    shifts_list = []
    for shift in range(28):
        print
        print "Current shift: " , shift
        s = apply_shift(text, shift)
        print "shifted text(s): %s" % s
        try:
            space = s.index(' ')
            print "Space = " , space
            print
            if is_word(wordlist, s[:space]):
                print "Valid word found from position 0 with shift %d" % shift
                #shifts_list.append(find_best_shifts_rec(wordlist, s, space+1)) #recursive call is not return correctly (or shifts_list is being deleted)
                find_best_shifts_rec(wordlist, s, space+1)
                print "(OG)Shifts_list just before checking for none:" , shifts_list
                if None in shifts_list:
                    print "None in shifts_list - clearing shifts_list"
                    shifts_list = []
                    print "About to pass"
                    print
                    pass
                else:
                    print "None not found in shifts list"
                    shifts_list.append((0,shift))
                    print "Shifts list currently: %s" % shifts_list
                    shifts_list = shifts_list[::-1]
                    print "flipped:" , shifts_list
                    return shifts_list                   
        except ValueError:
            print "value error - substring not found"
            if is_word(wordlist, s):
                print "End of sentence found"
                shifts_list.append((0, shift))
                break
            else:
                print "No space and no words"
    print "Total process about to return: " , shifts_list
    print shifts_list
    return shifts_list        

def find_best_shifts_rec(wordlist, text, start):
    """
    Given a scrambled string and a starting position from which
    to decode, returns a shift key that will decode the text to
    words in wordlist, or None if there is no such key.

    Hint: You will find this function much easier to implement
    if you use recursion.

    wordlist: list of words
    text: scambled text to try to find the words for
    start: where to start looking at shifts
    returns: list of tuples.  each tuple is (position in text, amount of shift)
    """
    ### TODO.
    
    global shifts_list
    print
    print "Text passed in: " , text
    print "Start passed in: " , start
    print "Shifts_list passed in:" , shifts_list
    print
    passed_shifts_list = shifts_list[:]
    print "Passed_shifts_list at this level of recursion:" , passed_shifts_list
    s_pre = text[:start]
    s_post = text[start:] 
    for shift in range(28):
        s = s_pre + apply_shifts(s_post, [(0, shift)])
        print "Starting at: " , start
        print "current shift is: " , shift
        print "shifted text(s): %s" % s
        try:
            space = s.index(' ', start)
            print "Space = " , space
            print
            if is_word(wordlist, s[start:space]):
                print "Recursive function will return: (%s,%s)" % (start, shift)
                print "Recursive function about to pass text with start = %d + 1" %space
                #shifts_list.append(find_best_shifts_rec(wordlist, s, space+1))
                find_best_shifts_rec(wordlist, s, space+1)
                if None in shifts_list:
                    print "None in shifts_list:", shifts_list
                    print "Resetting shifts_list to what it was at this level of recursion:" , passed_shifts_list
                    shifts_list = passed_shifts_list
                    print "Shifts_list now equals:" , shifts_list
                    print "About to pass"
                    print
                    pass
                else:
                    print "None not found in shifts_list:" , shifts_list
                    shifts_list.append((start,shift)) #change
                    return #change
                    #return (start,shift)
        except ValueError:
            print "value error - substring not found"
            if is_word(wordlist, s[start:]):
                print "End of sentence found"
                print
                print "Recursive function about to return: (%s,%s)" % (start,shift)
                print
                shifts_list.append((start,shift)) #it works when doing this...except function ends up returning none!
                return #change
                #return (start,shift)
            
    print "Recursive loop has completed with no words found"
    print
    shifts_list.append(None) #change
    return #change
    #return None

####Testing find_best_shifts and rec with test case given in specification
##s = 'eqorqukvqtbmultiform wyy ion'
##find_best_shifts(wordlist, s)

########Checking with random scrambles
##for i in range(10):
##    s = random_scrambled(wordlist, 2)
##    print "Original string: " , s
##    shifts = find_best_shifts(wordlist, s)
##    print "Returned shift list is: " , shifts
##    print "Applied Shifts:" , apply_shifts(s, shifts)
##    print "#####################################"

#Create a function to test accuracy - have it use is_word

    

####Example where recursive functions need to complete if proper end word is not found:
##s= ' nycbjkugihgnnkpi'
##print "Original string: " , s
##shifts = find_best_shifts(wordlist, s)
##print "Returned shift list is: " , shifts
##print apply_shifts(s, shifts)

####
####print "Oritinal string: " , s
####print "Shifts: " , shifts
####print "Decrypted text using shifts:" , apply_shifts(s, shifts)
####
####
########    print "Complete Round"
########    print
########    print

####Test where one correct word is found, but not another. Next correct word yields too many correct words, but should return them anyway according to rules
##s = 'ingttkrrkjfsteeds'
##print "Original string: " , s
##shifts = find_best_shifts(wordlist, s)
##print "Returned shift list is: " , shifts
##print apply_shifts(s, shifts)

def test_best_shifts(wordlist, trials, words):
    number = 1
    for i in range(trials):
        print "Trial number: %d" % number
        number += 1
        s = random_scrambled(wordlist, words)
        print "Original string: " , s
        shifts = find_best_shifts(wordlist, s)
        s2 = apply_shifts(s, shifts)       
        print "Decrypted text:" , s2
        valid_words = 0
        for i in s2.split(' '):
            if is_word(wordlist, i):
                valid_words +=1
        if valid_words == len(s2.split(' ')):
            print "Success: All Valid Words"
            print
        else:
            print "#####FAILED: NOT ALL VALID WORDS#####"
            break
        

#test_best_shifts(wordlist, 10, 10)

s = "l tkrzlxkiqrkyfloavsx"
print "Original string: " , s
shifts = find_best_shifts(wordlist, s)
print "Returned shift list is: " , shifts
print apply_shifts(s, shifts)

def decrypt_fable():
     """
    Using the methods you created in this problem set,
    decrypt the fable given by the function get_fable_string().
    Once you decrypt the message, be sure to include as a comment
    at the end of this problem set how the fable relates to your
    education at MIT.

    returns: string - fable in plain text
    """
    ### TODO.



#fable = get_fable_string()
#shifts = find_best_shifts(wordlist, fable)




    
#What is the moral of the story?
#
#
#
#
#

