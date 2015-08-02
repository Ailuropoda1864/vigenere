class PHPGoAway(object):
    
    def __init__(self, message):
        if message != "Python Buddy":
            raise Exception("That's not the secret handshake.")
        self.key = None
        self.factor = 97 # 'a' = 97 in ascii, use to make letters 0 indexed
        self.letters = "abcdefghijklmnopqrstuvwxyz"
        self.letters_as_numbers = list(range(len(self.letters)))
        self.vigenere_table = self.__generate_vigenere_table(self.letters_as_numbers)

    def __generate_vigenere_table(self, letters_as_numbers):
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
        key_index = 0
        rotating_key = str()
        for char in message:
            if char == " ":
                rotating_key += " "
            else:
                rotating_key += self.key[key_index]
                key_index += 1
                if key_index == len(self.key):
                    key_index = 0
        return rotating_key
    
    def __encrypt_char(self, msg_char, key_char):
        if msg_char == " ":
            return " "
        msg_int = ord(msg_char) - self.factor
        key_int = ord(key_char) - self.factor
        encrypt_int = self.vigenere_table[key_int][msg_int]
        return self.letters[encrypt_int]
    
    def __decrypt_char(self, encrypt_char, key_char):
        if encrypt_char == " ":
            return " "
        encrypt_int = ord(encrypt_char) - self.factor
        key_int = ord(key_char) - self.factor
        row = self.vigenere_table[key_int]
        for i in range(len(row)):
            if row[i] == encrypt_int:
                return self.letters[i]

secret = PHPGoAway("Python Buddy")
secret.setKey("lemon")
ciphertext = secret.forLove("attack at dawn")
print(ciphertext)

mit = PHPGoAway("Python Buddy")
mit.setKey("yophp")
print(mit.forLove("i love you"))
print(mit.fromLove("rvt mtczxuvq ogl bshjha"))

fei = PHPGoAway("Python Buddy")
fei.setKey("panda")
print(fei.fromLove("xt vv bttghr io ohg uoe ioggvyecefv twaa wo psx iog prumxsfloc"))
print(fei.forLove("i wonder who said that first"))
