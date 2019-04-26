# Hangman Game
# -----------------------------------
import random
import string

def load_words():
    """
    Returns a list of valid words. Words are strings of lowercase letters.
    
    Depending on the size of the word list, this function may
    take a while to finish.
    """
    print("Loading word list from file...")
    # inFile: file
    inFile = open(WORDLIST_FILENAME, 'r')
    # line: string
    line = inFile.readline()
    # wordlist: list of strings
    wordlist = line.split()
    print("  ", len(wordlist), "words loaded.")
    return wordlist

def choose_word(wordlist):
    """
    wordlist (list): list of words (strings)
    
    Returns a word from wordlist at random
    """
    return random.choice(wordlist)

def is_word_guessed(secret_word, letters_guessed):
    '''
    secret_word: string, the word the user is guessing; assumes all letters are
      lowercase
    letters_guessed: list (of letters), which letters have been guessed so far;
      assumes that all letters are lowercase
    returns: boolean, True if all the letters of secret_word are in 
      letters_guessed; False otherwise
    '''
    for char in secret_word:
        if char not in letters_guessed: 
            return False
    return True

def get_guessed_word(secret_word, letters_guessed):
    '''
    secret_word: string, the word the user is guessing
    letters_guessed: list (of letters), which letters have been guessed so far
    returns: string, comprised of letters, underscores (_), and spaces that 
      represents which letters in secret_word have been guessed so far.
    '''
    guessed_letters=""
    for char in secret_word:
        if char in letters_guessed:
            guessed_letters += char
        else:
            guessed_letters += "_ "
    return guessed_letters

def get_available_letters(letters_guessed):
    '''
    letters_guessed: list (of letters), which letters have been guessed so far
    returns: string (of letters), comprised of letters that represents which 
      letters have not yet been guessed.
    '''
    available_letters = list(string.ascii_lowercase)
    for char in letters_guessed:
       available_letters.remove(char)
    return ''.join(available_letters)

def hangman(secret_word):
    '''
    secret_word: string, the secret word to guess.
    
    Starts up an interactive game of Hangman.
    
    * At the start of the game, let the user know how many 
      letters the secret_word contains and how many guesses s/he starts with.
      
    * The user should start with 6 guesses

    * Before each round, you should display to the user how many guesses
      s/he has left and the letters that the user has not yet guessed.
    
    * Ask the user to supply one guess per round. Remember to make
      sure that the user puts in a letter!
    
    * The user should receive feedback immediately after each guess 
      about whether their guess appears in the computer's word.

    * After each guess, you should display to the user the 
      partially guessed word so far.
    
    Follows the other limitations detailed in the problem write-up.
    '''
    guesses_remaining = 6
    warnings_remaining = 3
    letters_guessed = []
    print("Welcome to the game Hangman!")
    print("I am thinking of a word that is", len(secret_word), "letters long.")
    print("You have", warnings_remaining, "warnings left.")
    while (not is_word_guessed(secret_word, letters_guessed) and 
           guesses_remaining > 0):
        print("-------------")
        print("You have", guesses_remaining, "guesses left.")
        print("Available letters:", get_available_letters(letters_guessed))
        letter = input("Please guess a letter:")
        #Check if is a invalid letter
        if not letter.isalpha():
            if warnings_remaining > 0:
                warnings_remaining -= 1
                print("Oops! That is not a valid letter. You have",
                      warnings_remaining, "warnings left:",
                      get_guessed_word(secret_word, letters_guessed))
            else:
                guesses_remaining -= 1
                print("Oops! That is not a valid letter. You have no warnings "
                      "left so you lose one guess:",
                      get_guessed_word(secret_word, letters_guessed))
        #Check if the letter has alreday beed guessed
        elif letter in letters_guessed:
            if warnings_remaining > 0:
                warnings_remaining -= 1
                print("Oops! You've already guessed that letter. You have",
                      warnings_remaining, "warnings left:",
                      get_guessed_word(secret_word, letters_guessed))
            else:
                guesses_remaining -= 1
                print("Oops! You've already guessed that letter. You have no "
                      "warnings left so you lose one guess:",
                      get_guessed_word(secret_word, letters_guessed))
        #If a valid letter, add it to the letters_guessed
        else:
            letters_guessed.append(letter.lower())   
            if letter in secret_word:
                print("Good guess:", get_guessed_word(secret_word,
                                                      letters_guessed))
            else:
                #Check if it's a vowel
                if letter in ["a", "e", "i", "o", "u"]:
                    guesses_remaining -= 2
                else:
                    guesses_remaining -= 1
                print("Oops! That letter is not in my word:",
                      get_guessed_word(secret_word, letters_guessed))
    print("-------------")
    #You win if the word was guessed
    if is_word_guessed(secret_word, letters_guessed):
        print("Congratulations, you won!")
        print("Your total score for this game is:",
              len(set(secret_word)) * guesses_remaining)
    #Else you loose
    else:
        print("Sorry, you ran out of guesses. The word was", secret_word)    

# -----------------------------------

def match_with_gaps(my_word, other_word):
    '''
    my_word: string with _ characters, current guess of secret word
    other_word: string, regular English word
    returns: boolean, True if all the actual letters of my_word match the 
      corresponding letters of other_word, or the letter is the special 
      symbol _ , and my_word and other_word are of the same length;
      False otherwise: 
    '''
    my_word = my_word.replace(" ","")
    if len(my_word) == len(other_word):
        for i in range(0,len(my_word)):
            if my_word[i] != "_" and my_word[i] != other_word[i]:
                return False
            elif my_word[i] == "_" and other_word[i] in my_word:
                return False
    else:
        return False
    return True

def show_possible_matches(my_word):
    '''
    my_word: string with _ characters, current guess of secret word
    returns: nothing, but should print out every word in wordlist that matches
      my_word
    Keep in mind that in hangman when a letter is guessed, all the positions at
      which that letter occurs in the secret word are revealed. Therefore, the
      hidden letter(_ ) cannot be one of the letters in the word that has
      already been revealed.
    '''
    possible_matches = []
    for other_word in wordlist:
        if match_with_gaps(my_word, other_word):
            possible_matches.append(other_word)
    if possible_matches == []:
        print("No matches found")
    else:
        print(" ".join(possible_matches))


def hangman_with_hints(secret_word):
    '''
    secret_word: string, the secret word to guess.
    
    Starts up an interactive game of Hangman.
    
    * At the start of the game, let the user know how many 
      letters the secret_word contains and how many guesses s/he starts with.
      
    * The user should start with 6 guesses
    
    * Before each round, you should display to the user how many guesses
      s/he has left and the letters that the user has not yet guessed.
    
    * Ask the user to supply one guess per round. Make sure to check that the
      user guesses a letter
      
    * The user should receive feedback immediately after each guess 
      about whether their guess appears in the computer's word.

    * After each guess, you should display to the user the 
      partially guessed word so far.
      
    * If the guess is the symbol *, print out all words in wordlist that
      matches the current guessed word. 
    
    Follows the other limitations detailed in the problem write-up.
    '''
    guesses_remaining = 6
    warnings_remaining = 3
    letters_guessed = []
    print("Welcome to the game Hangman!")
    print("I am thinking of a word that is", len(secret_word), "letters long.")
    print("You have", warnings_remaining, "warnings left.")
    while (not is_word_guessed(secret_word, letters_guessed) and 
           guesses_remaining > 0):
        print("-------------")
        print("You have", guesses_remaining, "guesses left.")
        print("Available letters:", get_available_letters(letters_guessed))
        letter = input("Please guess a letter:")
        #Check to print possible words
        if letter == "*":
            print("Possible word matches are:")
            show_possible_matches(get_guessed_word(secret_word,
                                                   letters_guessed))
        #Check if is a invalid letter
        elif not letter.isalpha():
            if warnings_remaining > 0:
                warnings_remaining -= 1
                print("Oops! That is not a valid letter. You have",
                      warnings_remaining, "warnings left:",
                      get_guessed_word(secret_word, letters_guessed))
            else:
                guesses_remaining -= 1
                print("Oops! That is not a valid letter. You have no warnings "
                      "left so you lose one guess:",
                      get_guessed_word(secret_word, letters_guessed))
        #Check if the letter has alreday beed guessed
        elif letter in letters_guessed:
            if warnings_remaining > 0:
                warnings_remaining -= 1
                print("Oops! You've already guessed that letter. You have",
                      warnings_remaining, "warnings left:",
                      get_guessed_word(secret_word, letters_guessed))
            else:
                guesses_remaining -= 1
                print("Oops! You've already guessed that letter. You have no "
                      "warnings left so you lose one guess:",
                      get_guessed_word(secret_word, letters_guessed))
        #If a valid letter, add it to the letters_guessed
        else:
            letters_guessed.append(letter.lower())   
            if letter in secret_word:
                print("Good guess:", get_guessed_word(secret_word,
                                                      letters_guessed))
            else:
                #Check if it's a vowel
                if letter in ["a", "e", "i", "o", "u"]:
                    guesses_remaining -= 2
                else:
                    guesses_remaining -= 1
                print("Oops! That letter is not in my word:",
                      get_guessed_word(secret_word, letters_guessed))
    print("-------------")
    #You win if the word was guessed
    if is_word_guessed(secret_word, letters_guessed):
        print("Congratulations, you won!")
        print("Your total score for this game is:",
              len(set(secret_word)) * guesses_remaining)
    #Else you loose
    else:
        print("Sorry, you ran out of guesses. The word was", secret_word)
    

WORDLIST_FILENAME = "words.txt"
wordlist = load_words()
secret_word = choose_word(wordlist)
#hangman(secret_word)
hangman_with_hints(secret_word)