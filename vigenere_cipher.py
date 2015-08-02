class PHPGoAway(object):
    
    def __init__(self, alphabet=None):
        self.key = ""
        if alphabet is None:
            lowercase = "abcdefghijklmnopqrstuvwxyz"
            uppercase = lowercase.upper()
            punctuation = ".,?;:'`~!@#$%^&*()-+_=[]{}/\| "
            self.alphabet = lowercase + uppercase + punctuation
        else:
            self.alphabet = alphabet
        self.vigenere_table = self.__generate_vigenere_table(self.alphabet)

    def __generate_vigenere_table(self, alphabet):
        letters_as_numbers = list(range(len(alphabet)))
        table = dict()
        for i in range(len(letters_as_numbers)):
            table[i] = letters_as_numbers[i:]
            table[i].extend(letters_as_numbers[:i])
        return table
    
    def setKey(self, key):
        self.key = key
    
    def forLove(self, message):
        rotating_key = self.__get_rotating_key(message)
        encrypted = str()
        for i in range(len(message)):
            encrypted += self.__encrypt_char(message[i], rotating_key[i])
        return encrypted
    
    def fromLove(self, encrypted):
        rotating_key = self.__get_rotating_key(encrypted)
        message = str()
        for i in range(len(encrypted)):
            message += self.__decrypt_char(encrypted[i], rotating_key[i])
        return message
    
    def __get_rotating_key(self, message):
        if not self.key:
            raise Exception("Set the key first, dummy!  Do you want everyone to read this?")
        rotating_key = str()
        for i in range(len(message)):
            rotating_key += self.key[i % len(self.key)]
        return rotating_key
    
    def __encrypt_char(self, msg_char, key_char):
        msg_int = self.alphabet.find(msg_char)
        key_int = self.alphabet.find(key_char)
        encrypt_int = self.vigenere_table[key_int][msg_int]
        return self.alphabet[encrypt_int]
    
    def __decrypt_char(self, encrypt_char, key_char):
        encrypt_int = self.alphabet.find(encrypt_char)
        key_int = self.alphabet.find(key_char)
        row = self.vigenere_table[key_int]
        for i in range(len(row)):
            if row[i] == encrypt_int:
                return self.alphabet[i]
