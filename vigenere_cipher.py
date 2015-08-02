class PHPGoAway(object):

    def __init__(self, characters=None):
        self.key = ""
        self.cached_vigenere_table = None
        if characters is None:
            lowercase = "abcdefghijklmnopqrstuvwxyz"
            uppercase = lowercase.upper()
            punctuation = ".,?;:'`~!@#$%^&*()-+_=[]{}/\| "
            self.characters = lowercase + uppercase + punctuation
        else:
            self.characters = characters

    @property
    def __vigenere_table(self):
        if self.cached_vigenere_table is None:
            letters_as_numbers = list(range(len(self.characters)))
            table = dict()
            for i in range(len(letters_as_numbers)):
                table[i] = letters_as_numbers[i:]
                table[i].extend(letters_as_numbers[:i])
            self.cached_vigenere_table = table
        return self.cached_vigenere_table

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
        msg_int = self.characters.find(msg_char)
        key_int = self.characters.find(key_char)
        encrypt_int = self.__vigenere_table[key_int][msg_int]
        return self.characters[encrypt_int]

    def __decrypt_char(self, encrypt_char, key_char):
        encrypt_int = self.characters.find(encrypt_char)
        key_int = self.characters.find(key_char)
        row = self.__vigenere_table[key_int]
        return self.characters[row.index(encrypt_int)]
