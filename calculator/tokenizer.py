#Author: Chunpai Wang
#Email: cwang64@u.rochester.edu
#CSC254 HWK03 : Tokenizer

#build a tokenizer for arithmatic expression
import sys
import os

class Token:
    # constructor, token has two parameters (name and value)
    def __init__(self,token_name, token_value):
        self.token_name  = token_name
        self.token_value = token_value
    # return the name of token
    def get_name(self):
        return self.token_name
    # return the value of token
    def get_value(self):
        return self.token_value

class Scanner:
    # constructor can read file as a string,
    # remove all comments, 
    # and return a list of tokens.
    def __init__(self, file_name):
        self.infile = open(file_name,'r')
        #print self.infile.tell()
        #print self.infile.read(1)
        #print self.infile.tell()
        #self.infile.seek(0)
        #print self.infile.tell()
        self.cursor = 0
        if os.path.getsize(file_name) == 0:
            print 'Empty File!'
    
    """
    #peek next character, but not effect the infile position
    def peek_next(self, size):
        last_pos   = self.infile.tell()
        chars = self.infile.read(size)
        self.infile.seek(last_pos)
        return chars
    """
    
    # return the next token (as a Token object) or EOF
    # this function will remove the whitespace before see valid characters
    # and read the char by char to match the patterns
    def next_token(self):
        letter = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z','_']
        digit = ['0','1','2','3','4','5','6','7','8','9']
        ch = self.infile.read(1)
        while(ch == ' ' or ch == '\t' or ch == '\n' or ch =='\r'):
            ch = self.infile.read(1)
        if(ch == ' ' or ch == '\t' or ch == '\n' or ch == '\r'):
            self.infile.close()
        else:
            #detect numbers
            if ch in digit:
                value = ch
                next_ch = self.infile.read(1)
                while(next_ch in digit):
                    value += next_ch
                    next_ch = self.infile.read(1)
                if next_ch.lower() in letter:
                    print 'ERROR: illegal token \"'+ value + next_ch +'\"'
                else:
                    new_pos = self.infile.tell() -1
                    self.infile.seek(new_pos)
                    token = Token('number',value)
                    return token
            #detect symbols
            elif ch == '+':
                token = Token('add',ch)
                return token
            elif ch == '-':
                token = Token('minus',ch)
                return token
            elif ch == '*':
                token = Token('multi',ch)
                return token
            elif ch == '/':
                token = Token('div',ch)
                return token
            elif ch == '(':
                token = Token('left_p',ch)
                return token
            elif ch == ')':
                token = Token('right_p',ch)
                return token
            elif not ch:
                #print('Tokenization Finished !')
                token = Token('eps','$$')
                return token
            else:
                print 'ERROR: illegal token \"'+value+'\"'


if __name__ == "__main__":
    output_file = open('output_file.c','w')
    scanner = Scanner(sys.argv[1])
    token = scanner.next_token()
    while token.get_name() != 'eps': # while not END of FILE
        print (token.get_name(),token.get_value())
        if token.get_name() == 'identifier':
            output_file.write(token.get_value()+'_cs254'+' ')
        else:
            output_file.write(token.get_value()+' ')
        token = scanner.next_token()
    output_file.close()
     


    """
    letter = '[a-zA-Z|_]'
    digit  = '[0-9]'
    identifier = letter+'('+letter+'|'+digit +')*'
    number = '(' + digit+ ')+'
    reserverd_word = 'int|void|if|while|return|continue|break|scanf|printf'
    symbol = '\(|\)|\[|\]|\{|\}|,|;|\+|-|\*|/|==|!=|>|<|>=|<=|=|&&|(\|\|)|&'
    string = '(\'.*\')|(\".*\")'
    meta_stmt = '(#|//).*\n'
    """
