#a calculator can do scanning, LL(1) parsing and evaluation with action routine.
import sys
import tokenizer


class Node():
    def __init__(self,name,st,ptr):
        self.name  = name
        #self.child = []
        self.st  = st
        self.ptr = ptr
    def get_st(self):
        return self.st
    def get_ptr(self):
        return self.ptr


class Calculator:
    def __init__(self, scanner):
        self.scanner = scanner
        self.input_token = scanner.next_token()
   
    #if match the token, consume current token, and get next token
    def match(self,expected_token):
        if self.input_token.get_name() == expected_token:
            self.input_token = self.scanner.next_token()
        else:
            print 'ERROR1!!!'
    
    # the parameter node, is the node for expression
    def expression(self,node):
        #node_E = Node('E',0,0)
        node_T = Node('T',0,0)
        node_TT = Node('TT',0,0)
        if self.input_token.get_name() in ['left_p','number']:
            #node.child.append(node_T)
            #node.child.append(node_TT)
            self.term(node_T)
            node_TT.st =  node_T.ptr
            self.term_tail(node_TT)
            node.ptr = node_TT.ptr
        elif self.input_token.get_name() == 'minus':
            self.match('minus')
            #node.child.append(node_T)
            #node.child.append(Node_TT)
            self.term(node_T)
            node_T.ptr = self.make_un_op('-',node_T.ptr)
            node_TT.st =  node_T.ptr
            self.term_tail(node_TT)
            node.ptr = node_TT.ptr
        else:
            print 'ERROR2!!!'
        
    def term(self,node):
        #node_T = Node('T',0,0)  
        node_F = Node('F',0,0)
        node_FT = Node('FT',0,0)
        if self.input_token.get_name() in ['left_p','number']:
            #node.child.append(node_F)
            #node.child.append(node_FT)
            self.factor(node_F)
            #print 'haha',node_F.ptr 
            node_FT.st = node_F.ptr
            self.factor_tail(node_FT)
            #print 'haha',node_FT.ptr
            #print 'node_FT.st',node_FT.st
            node.ptr = node_FT.ptr
            #print 'node.ptr',node.ptr
        else:
            print 'ERROR3!!!'

    def term_tail(self,node):
        #node_TT = Node('TT',0,0)
        node_T2 = Node('T',0,0)
        node_TT2 = Node('TT',0,0)
        if self.input_token.get_name() ==  'add':
            self.match(self.input_token.get_name())
            #node.child.append(node_T2)
            #node.child.append(node_TT2)
            self.term(node_T2)
            node_TT2.st = self.make_bin_op('+',node.st,node_T2.ptr)
            self.term_tail(node_TT2)
            #print node_T2.st
            #print node_TT2.ptr
            node.ptr = node_TT2.ptr
        elif self.input_token.get_name() == 'minus':
            self.match(self.input_token.get_name())
            #node.child.append(node_T2)
            #node.child.append(node_TT2)
            self.term(node_T2)
            node_TT2.st = self.make_bin_op('-',node.st,node_T2.ptr)
            self.term_tail(node_TT2)
            node.ptr = node_TT2.ptr
        elif self.input_token.get_name() in ['right_p','eps']:
            node.ptr = node.st
        else:
            print 'ERROR4!!!'

    def factor(self,node):
        if self.input_token.get_name() == 'left_p':
            node_E2 = Node('E',0,0)
            self.match('left_p')
           # node.child.append(node_E2)
            self.expression(node_E2)
            self.match('right_p')
            node.ptr = node_E2.ptr
        elif self.input_token.get_name() == 'number':
            const = self.input_token.get_value()
            self.match('number')
            node.ptr = const
            #print node.ptr
        #elif self.input_token.get_name() == 'minus':
        #    node_F2 = Node('F2',0,0)
        #    self.match('minus')
        #    self.factor(node_F2)
        #    node.ptr = self.make_un_op('-',node_F2.ptr)
        else:
            print 'ERROR5!!!'

    def factor_tail(self,node):
        if self.input_token.get_name() == 'multi':
            self.match(self.input_token.get_name())
            node_F2 = Node('F2',0,0)
            node_FT2 = Node('FT2',0,0)
            self.factor(node_F2)
            node_FT2.st = self.make_bin_op('*',node.st, node_F2.ptr)
            self.factor_tail(node_FT2)
            node.ptr = node_FT2.ptr
        elif self.input_token.get_name() == 'div':
            self.match(self.input_token.get_name())
            node_F2 = Node('F2',0,0)
            node_FT2 = Node('FT2',0,0)
            self.factor(node_F2)
            node_FT2.st =  self.make_bin_op('/', node.st , node_F2.ptr)
            self.factor_tail(node_FT2)
            #print node.st
            #print node_F2.ptr
            node.ptr = node_FT2.ptr
        elif self.input_token.get_name() in ['add','minus','right_p','eps']:
            node.ptr = node.st
            #print 'factor_tail',node.ptr
            pass 
        else:
            print 'ERROR6!!!'
            #print self.input_token.get_value()
        
            
    def make_bin_op(self, op, value1, value2):
        if op == '+':
            return int(value1)+int(value2)
        elif op == '-':
            return int(value1)-int(value2)
        elif op == '*':
            return int(value1)*int(value2)
        elif op == '/':
            return int(value1) / int(value2)
        else:
            print 'ERROR7!!!'


    def make_un_op(self, op, value):
        if op == '-':
            return 0-int(value)
        else:
            print 'ERROR8!!!'
        


if __name__ == '__main__':
    scanner = tokenizer.Scanner(sys.argv[1])
    calculator = Calculator(scanner)
    node = Node('E',0,0)
    calculator.expression(node)
    print node.ptr
