# Substitution Cipher

from ps4a import get_permutations

WORDLIST_FILENAME = 'words.txt'

# you may find these constants helpful
VOWELS_LOWER = 'aeiou'
VOWELS_UPPER = 'AEIOU'
CONSONANTS_LOWER = 'bcdfghjklmnpqrstvwxyz'
CONSONANTS_UPPER = 'BCDFGHJKLMNPQRSTVWXYZ'

def load_words(file_name):
    '''
    file_name (string): the name of the file containing the list of
    words to load.  
    
    Returns: a list of valid words. Words are strings of lowercase
    letters.
    
    Depending on the size of the word list, this function may take a
    while to finish.
    '''
    
    print("Loading word list from file...")
    # inFile: file
    inFile = open(file_name, 'r')
    # wordlist: list of strings
    wordlist = []
    for line in inFile:
        wordlist.extend([word.lower() for word in line.split(' ')])
    print("  ", len(wordlist), "words loaded.")
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

def get_story_string(file_path):
    """
    Returns: a story in encrypted text.
    """
    f = open(file_path, "r")
    story = str(f.read())
    f.close()
    return story

class SubMessage(object):
    def __init__(self, text):
        '''
        Initializes a SubMessage object
                
        text (string): the message's text

        A SubMessage object has two attributes:
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
        class.
        
        Returns: a COPY of self.valid_words
        '''
        return self.valid_words.copy()
                
    def build_transpose_dict(self, vowels_permutation):
        '''
        vowels_permutation (string): a string containing a permutation
        of vowels (a, e, i, o, u)
        
        Creates a dictionary that can be used to apply a cipher to a
        letter. The dictionary maps every uppercase and lowercase letter
        to an uppercase and lowercase letter, respectively. Vowels are
        shuffled according to vowels_permutation. The first letter in
        vowels_permutation corresponds to a, the second to e, and so on
        in the order a, e, i, o, u. The consonants remain the same. The
        dictionary should have 52 keys of all the uppercase letters and
        all the lowercase letters.

        Returns: a dictionary mapping a letter (string) to 
                 another letter (string). 
        '''
        dic = {}
        #Map vowels
        for i, letter in enumerate(vowels_permutation):
            dic[VOWELS_LOWER[i]] = letter.lower()
            dic[VOWELS_UPPER[i]] = letter.upper()
        #Map consonants
        for i in range(len(CONSONANTS_LOWER)):
            dic[CONSONANTS_LOWER[i]] = CONSONANTS_LOWER[i]
            dic[CONSONANTS_UPPER[i]] = CONSONANTS_UPPER[i]
        return dic
    
    def apply_transpose(self, transpose_dict):
        '''
        transpose_dict (dict): a transpose dictionary
        
        Returns: an encrypted version of the message text, based on the
        dictionary
        '''
        encrypted_message = ""
        for letter in self.get_message_text():
            if transpose_dict.get(letter,-1) == -1:
                encrypted_message += letter
            else:
                encrypted_message += transpose_dict[letter]    
        return encrypted_message
        
        
class EncryptedSubMessage(SubMessage):
    def __init__(self, text):
        '''
        Initializes an EncryptedSubMessage object

        text (string): the encrypted message text

        An EncryptedSubMessage object inherits from SubMessage and has
        two attributes:
            self.message_text (string, determined by input text)
            self.valid_words (list, determined using helper function
            load_words)
        '''
        SubMessage.__init__(self,text)

    def decrypt_message(self):
        '''
        Attempt to decrypt the encrypted message
        
        Idea is to go through each permutation of the vowels and test it
        on the encrypted message. For each permutation, check how many
        words in the decrypted text are valid English words, and return
        the decrypted message with the most English words. If no good
        permutations are found (i.e. no permutations result in at least
        one valid word), return the original string. If there are
        multiple permutations that yield the maximum number of words,
        return any one of them.

        Returns: the best decrypted message
        '''
        possibly_permutation = get_permutations(VOWELS_LOWER)
        max_valid_words = -1
        best_decrypted_message = decrypted_message = self.get_message_text()
        for vowels_permutation in possibly_permutation:
            dic = self.build_transpose_dict(vowels_permutation)
            decrypted_message = self.apply_transpose(dic)
            decrypted_words = str.split(decrypted_message," ")
            n_valid_words = 0
            for word in decrypted_words:
                if is_word(self.get_valid_words(), word):
                    n_valid_words += 1
            if n_valid_words > max_valid_words:
                max_valid_words = n_valid_words
                best_decrypted_message = decrypted_message
        return best_decrypted_message


def test_substitution_cipher(original_message, permutation,
                             expected_encryption):
    message = SubMessage(original_message)
    enc_dict = message.build_transpose_dict(permutation)
    print("Original message:", message.get_message_text(), "Permutation:",
          permutation)
    print("Expected encryption:", expected_encryption)
    print("Actual encryption:", message.apply_transpose(enc_dict))
    enc_message = EncryptedSubMessage(message.apply_transpose(enc_dict))
    print("Decrypted message:", enc_message.decrypt_message())

if __name__ == '__main__':
    original_message = ["Hello World!",
                        get_story_string("story2_original.txt")]
    expected_encryption = ["Hallu Wurld!",
                           get_story_string("story2_encrypted.txt")]
    permutation = "eaiuo"
    
    for i in range(len(original_message)):
        test_substitution_cipher(original_message[i], permutation,
                                 expected_encryption[i])
    