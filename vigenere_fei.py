class PHPGoAway(object):
    def __init__(self):
        
        self.alphabet = 'abcdefghijklmnopqrstuvwxyz'
        self.ALPHABET = self.alphabet.upper()
        self.combinedAlphabet = self.alphabet + self.ALPHABET
        
        # create a dictionary of letter:index(integer) pairs
        # e.g. 'a':0, 'b':1, 'A':0
        self.dict={}
        for n in range(26):
            self.dict[self.alphabet[n]]=n
            self.dict[self.ALPHABET[n]]=n
        
        # create tabula recta as a list of strings (lowercase) 
        row = self.alphabet
        self.Vsquare=[row]
        for n in range(25):
            row=row[1:]+row[0]
            self.Vsquare+=[row]

    
    def setKey(self, key):
        '''alphabetical letters only; NOT case-sensitive'''
        for char in key:
            if char not in self.combinedAlphabet:
                raise Exception('The key must consist of alphabetical letters only.')
        self.key=key
                
    
    def actualKey(self, text):
        key=''
        n=0 # index for the self.key string
        
        for i in range(len(text)):
            
            # key rotation bypasses any non-alphabetical characters
            if text[i] not in self.combinedAlphabet:
                key+=text[i]
                
            else:
                if n>=len(self.key):
                    n%=len(self.key)
                key+=self.key[n].lower() # output string is all lowercase
                n+=1
        
        return key    

                        
    def forLove(self, msg):
        '''any non-alphabetical character remains as is
        case of alphabetical letter will be preserved'''
        
        key=self.actualKey(msg)
   
        encrypt=''
        for i in range(len(msg)):
            if msg[i] not in self.combinedAlphabet:
                encrypt += msg[i]
            else:
                row_index = self.dict[key[i]]
                column_index = self.dict[msg[i]]
                if msg[i] in self.ALPHABET:
                    encrypt += self.Vsquare[row_index][column_index].upper()
                else:
                    encrypt += self.Vsquare[row_index][column_index]
        
        return encrypt
 
               
    def fromLove(self, en_msg):
        '''any non-alphabetical character remains as is
        case of alphabetical letter will be preserved'''
        
        key=self.actualKey(en_msg)
        
        decrypt=''
        for i in range(len(en_msg)):
            if en_msg[i] not in self.combinedAlphabet:
                decrypt += en_msg[i]
            else:
                index = self.dict[en_msg[i]] - self.dict[key[i]]
                if index < 0:
                    index += 26
                if en_msg[i] in self.ALPHABET:
                    decrypt += self.Vsquare[0][index].upper()
                else:
                    decrypt += self.Vsquare[0][index]
        
        return decrypt
   