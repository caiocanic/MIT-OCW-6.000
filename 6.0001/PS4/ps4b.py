#Caesar Cipher

import string

WORDLIST_FILENAME = 'words.txt'

def load_words(file_name):
    '''
    file_name (string): the name of the file containing the list of
    words to load    
    
    Returns: a list of valid words. Words are strings of lowercase
    letters.
    '''
    #print("Loading word list from file...")
    # inFile: file
    inFile = open(file_name, 'r')
    # wordlist: list of strings
    wordlist = []
    for line in inFile:
        wordlist.extend([word.lower() for word in line.split(' ')])
    #print("  ", len(wordlist), "words loaded.")
    return wordlist

def is_word(word_list, word):
    '''
    Determines if word is a valid word, ignoring capitalization and
    punctuation

    word_list (list): list of words in the dictionary.
    word (string): a possible word.
    
    Returns: True if word is in word_list, False otherwise
    '''
    word = word.lower()
    word = word.strip(" !@#$%^&*()-_+={}[]|\:;'<>?,./\"")
    return word in word_list

def get_story_string():
    """
    Returns: a story in encrypted text.
    """
    f = open("story.txt", "r")
    story = str(f.read())
    f.close()
    return story

class Message(object):
    def __init__(self, text):
        '''
        Initializes a Message object
                
        text (string): the message's text

        a Message object has two attributes:
            self.message_text (string, determined by input text)
            self.valid_words (list, determined using helper function
            load_words)
        '''
        self.message_text = text
        self.valid_words = load_words(WORDLIST_FILENAME)

    def get_message_text(self):
        '''
        Used to safely access self.message_text outside of the class
        
        Returns: self.message_text
        '''
        return self.message_text

    def get_valid_words(self):
        '''
        Used to safely access a copy of self.valid_words outside of the
        class. This helps you avoid accidentally mutating class
        attributes.
        
        Returns: a COPY of self.valid_words
        '''
        return self.valid_words[:]

    def build_shift_dict(self, shift):
        '''
        Creates a dictionary that can be used to apply a cipher to a 
        letter. The dictionary maps every uppercase and lowercase letter
        to a character shifted down the alphabet by the input shift. The
        dictionary should have 52 keys of all the uppercase letters and
        all the lowercase letters only.
        
        shift (integer): the amount by which to shift every letter of
        the alphabet. 0 <= shift < 26

        Returns: a dictionary mapping a letter (string) to another
        letter (string). 
        '''
        assert shift >= 0 and shift < 26, "Invalid shift value."
        dic = {}
        #Map lowercase letters
        for i, letter in enumerate(string.ascii_lowercase):
            dic[letter] = string.ascii_lowercase[(i+shift)%26]
        #Map uppercase letters
        for i, letter in enumerate(string.ascii_uppercase):
            dic[letter] = string.ascii_uppercase[(i+shift)%26]
        return dic
            
    def apply_shift(self, shift):
        '''
        Applies the Caesar Cipher to self.message_text with the input
        shift. Creates a new string that is self.message_text shifted
        down the alphabet by some number of characters determined by the
        input shift        
        
        shift (integer): the shift with which to encrypt the message.
        0 <= shift < 26

        Returns: the message text (string) in which every character is
        shifted down the alphabet by the input shift
        '''
        assert shift >= 0 and shift < 26, "Invalid shift value."
        dic = self.build_shift_dict(shift)
        shifted_message = ""
        for letter in self.get_message_text():
            if dic.get(letter,-1) == -1:
                shifted_message += letter
            else:
                shifted_message += dic[letter]
        return shifted_message

class PlaintextMessage(Message):
    def __init__(self, text, shift):
        '''
        Initializes a PlaintextMessage object        
        
        text (string): the message's text
        shift (integer): the shift associated with this message

        A PlaintextMessage object inherits from Message and has five
        attributes:
            self.message_text (string, determined by input text)
            self.valid_words (list, determined using helper function
            load_words)
            self.shift (integer, determined by input shift)
            self.encryption_dict (dictionary, built using shift)
            self.message_text_encrypted (string, created using shift)
        '''
        assert shift >= 0 and shift < 26, "Invalid shift value."
        Message.__init__(self,text)
        self.shift = shift
        self.encryption_dict = self.build_shift_dict(shift)
        self.message_text_encrypted = self.apply_shift(shift)

    def get_shift(self):
        '''
        Used to safely access self.shift outside of the class
        
        Returns: self.shift
        '''
        return self.shift

    def get_encryption_dict(self):
        '''
        Used to safely access a copy self.encryption_dict outside of the
        class
        
        Returns: a COPY of self.encryption_dict
        '''
        return self.encryption_dict.copy()

    def get_message_text_encrypted(self):
        '''
        Used to safely access self.message_text_encrypted outside of the
        class
        
        Returns: self.message_text_encrypted
        '''
        return self.message_text_encrypted

    def change_shift(self, shift):
        '''
        Changes self.shift of the PlaintextMessage and updates other
        attributes determined by shift.        
        
        shift (integer): the new shift that should be associated with
        this message. 0 <= shift < 26

        Returns: nothing
        '''
        assert shift >= 0 and shift < 26, "Invalid shift value."
        self.shift = shift
        self.encryption_dict = self.build_shift_dict(shift)
        self.message_text_encrypted = self.apply_shift(shift)


class CiphertextMessage(Message):
    def __init__(self, text):
        '''
        Initializes a CiphertextMessage object
                
        text (string): the message's text

        a CiphertextMessage object has two attributes:
            self.message_text (string, determined by input text)
            self.valid_words (list, determined using helper function
            load_words)
        '''
        Message.__init__(self,text)

    def decrypt_message(self):
        '''
        Decrypt self.message_text by trying every possible shift value
        and find the "best" one. We will define "best" as the shift that
        creates the maximum number of real words when we use
        apply_shift(shift) on the message text. If s is the original
        shift value used to encrypt the message, then we would expect
        26 - s to be the best shift value for decrypting it.

        Returns: a tuple of the best shift value used to decrypt the
        message and the decrypted message text using that shift value
        '''
        max_valid_words = -1
        for decrypt_shift in range(26):
            decrypted_message = self.apply_shift(decrypt_shift)
            decrypted_words = str.split(decrypted_message," ")
            n_valid_words = 0
            for word in decrypted_words:
                if is_word(self.get_valid_words(),word):
                    n_valid_words += 1        
            if n_valid_words >= max_valid_words:
                max_valid_words = n_valid_words
                best_shift_message = (decrypt_shift,decrypted_message)
        return best_shift_message

if __name__ == '__main__':    
    cp = CiphertextMessage(get_story_string())
    print(cp.decrypt_message())