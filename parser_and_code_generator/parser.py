#!/usr/bin/env python
#Author: Chunpai Wang
#Email: cwang64@u.rochester.edu
#Description: do static checking and intermedia code generation along with LL parsing.
import tokenizer
import sys
from subprocess import call

# node for expression
class Node:
    def __init__(self,name,addr,code):
        self.name = name
        self.addr = addr
        self.code = code

#control flow node
class CFNode:
    def __init__(self,name,code,true,false):
        self.name = name
        self.code = code
        self.true = true
        self.false = false

class Parser:
    def __init__(self,scanner):
        self.scanner = scanner
        self.input_token = scanner.next_token()  # get next_token from tokenizer
        self.variables  = 0                      # used for counting the number of variables
        self.functions  = 0
        self.statements = 0
        self.symbol_tables = {'global':{}}       # use dictionray data structure to build symbol tables.
        self.current = 'global'  # name for current symbol table
        self.current_symbol_table = self.symbol_tables[self.current]
        self.output = []                         #save generated code into a output list, and write in a text file once finishing parsing 
        self.temp_size = -1                      # used for generating offset in the symbol table
        self.label_size = 0                      # used for generating labels
        self.reserved_index = 0                  
   
    def new_temp(self):
        self.temp_size += 1
        #return self.current+'_var['+str(self.temp_size)+']'
        return self.current+'_var'

    def new_label(self):
        self.label_size +=1
        return 'L'+str(self.label_size) 

    def gen(self,code):
        return code + ';\n'

    #match by token_value or token_name(token type) and append the token into output_list
    def match(self,attribute,expected_token):
        if attribute == 'name':
            if self.input_token.get_name() == expected_token:
                #print self.input_token.get_value()
                self.output.append(self.input_token.get_value()+' ')
                self.input_token = self.scanner.next_token()
            else:
                raise SyntaxError('Not Match !')
        elif attribute == 'value':
            if self.input_token.get_value() == expected_token:
                #print self.input_token.get_value()
                self.output.append(self.input_token.get_value()+' ')
                self.input_token = self.scanner.next_token()
            else:
                raise SyntaxError('Not Match !')
    
    # match but not append token into output list
    def match2(self,attribute,expected_token):
        if attribute == 'name':
            if self.input_token.get_name() == expected_token:
                #print self.input_token.get_value()
                #self.output.write(self.input_token.get_value()+' ')
                self.input_token = self.scanner.next_token()
            else:
                raise SyntaxError('Not Match !')
        elif attribute == 'value':
            if self.input_token.get_value() == expected_token:
                #print self.input_token.get_value()
                #self.output.write(self.input_token.get_value()+' ')
                self.input_token = self.scanner.next_token()
            else:
                raise SyntaxError('Not Match !')


    def program(self):
        if self.input_token.get_value() in ['int','void']:
            self.data_decls()
            self.output.append('int '+self.current+'_var[' + str(self.temp_size + 1) + '];\n') # generate an array for global variables
            self.func_list()
        elif self.input_token.get_value() == '$$':
            print 'pass'
        else:
            raise SyntaxError('ERROR1!!!')

    def func_list(self):
        if self.input_token.get_value() in ['int','void']:
            self.func()
            self.func_list()
        elif self.input_token.get_value() == '$$':
            pass
        else:
            raise SyntaxError('ERROR2!!!')


    def func(self):
        #symbol_table = {}
        if self.input_token.get_value() in ['int','void']:
            code = self.func_decl()       # the return code is the code for function parameters, and specify them in the  function
            self.func_tail(code)
        else:
            raise SyntaxError('ERROR2!!!')

    # pass the code from function's parameter into function tail
    def func_tail(self,code):
        #print self.input_token.get_value() +'hahahah'
        if self.input_token.get_value() == ';':
            self.match('value',';')
        elif self.input_token.get_value() == '{':
            self.match('value','{')
            self.functions += 1
            #print self.input_token.get_name() +'88888ah'
            self.output.append(' ')
            self.reserved_index = len(self.output) -1 
            self.output.append(code)
            self.data_decls()
            self.stmts()
            self.match('value','}')
            self.output[self.reserved_index] = 'int '+self.current+'_var[' + str(self.temp_size + 1) + '];\n'
        else:
            raise SyntaxError('ERROR3!!!')

    def func_decl(self):
        if self.input_token.get_value() in ['int','void']:
            self.type_name()
            func_name = self.input_token.get_value()
            if func_name not in self.symbol_tables:
                self.symbol_tables[func_name] = {}
            #else:
            #    raise SyntaxError('ERROR: current function name has been used, choose another one')
            self.current = func_name
            self.current_symbol_table = self.symbol_tables[self.current]
            self.temp_size = -1
            self.match('name','identifier')
            self.match('value','(')
            code = self.parameter_list()
            self.match('value',')')
            return code
        else:
            raise SyntaxError('ERROR4!!!')

    def type_name(self):
        if self.input_token.get_value() in ['int','void']:
            self.match('value',self.input_token.get_value())
        else:
            raise SyntaxError('ERROR5!!!')

    def parameter_list(self):
        if self.input_token.get_value() == 'void':
            self.match('value','void')
            code = ' '
            return code
        elif self.input_token.get_value() == 'int':
            code = self.non_empty_list()
            return code
        elif self.input_token.get_value() == ')':
            code = ' '
            return code
            #pass
        else:
            raise SyntaxError('ERROR6!!!')

    def non_empty_list(self):
        if self.input_token.get_value() == 'int':
            self.variables += 1
            self.match('value','int')
            idf = self.input_token.get_value()
            new_temp = self.new_temp() 
            offset = self.temp_size
            self.current_symbol_table[idf] = (new_temp,self.temp_size)
            self.match('name','identifier')
            code = self.gen(new_temp+'[' +str(offset)+']'+ '=' + idf)
            if self.input_token.get_value() == ',':
                code = self.non_empty_list_prime(code)
            else:
                self.non_empty_list_prime(code)
            return code
        else:
            raise SyntaxError('ERROR7!!!')

    def non_empty_list_prime(self,code):
        if self.input_token.get_value() == ',':
            self.variables += 1
            self.match('value',',')
            self.match('value','int')
            idf = self.input_token.get_value()
            new_temp = self.new_temp()
            offset = self.temp_size
            self.current_symbol_table[idf] = (new_temp,self.temp_size)
            self.match('name','identifier')
            code = code + self.gen(new_temp +'[' +str(offset)+']'+ '=' + idf)
            if self.input_token.get_value() == ',':
                code = self.non_empty_list_prime(code)
            else:
                self.non_empty_list_prime(code)
            return code
        elif self.input_token.get_value() == ')':
            pass
        else:
            raise SyntaxError('ERROR8!!!')

    # since data_decls can be empty and func_lists can be empty too.
    # And both start with type_name ID, we need to peek 3 tokens to check 
    # which production rule to use.
    def data_decls(self):
        #print self.input_token.get_value()
        last_pos = self.scanner.infile.tell()
        last_token = self.input_token
        #print last_pos
        if self.input_token.get_value() in ['int']:
            next_token = self.scanner.next_token()
            #print next_token.get_value()
            if next_token.get_name() == 'identifier':
                next_token = self.scanner.next_token()
                if next_token.get_value() in ['[',',',';']:
                    self.scanner.infile.seek(last_pos)
                    self.input_token = last_token
                    self.type_name()
                    self.output.pop()
                    self.id_list()
                    self.match2('value',';')
                    self.data_decls()
                elif next_token.get_value() == '(':
                    self.scanner.infile.seek(last_pos)
                    self.input_token =  last_token
                    pass
                else:
                    raise SyntaxError('ERROR9!!!')
            else:
                self.scanner.infile.seek(last_pos)
                self.input_token = last_token
                raise SyntaxError('ERROR10!!!')
        elif self.input_token.get_name() in ['identifier','reserved_words','eof','type_name']:
            pass
        else:
            raise SyntaxError('ERROR11!!!')


    def id_list(self):
        if self.input_token.get_name() == 'identifier':
            idf = self.input_token.get_value()
            array_flag, node_expr = self.id_()  # return boolean if this id is an array, and the expression(or size) of the array
            self.variables += 1
            if idf not in self.current_symbol_table:
                if array_flag == False:
                    #offset = 1
                    new_temp = self.new_temp()
                    self.current_symbol_table[idf] = (new_temp, self.temp_size)
                else:
                    if node_expr.addr.isdigit():
                        #self.output.append(idf+'['+node_expr.addr+']')
                        size = int(node_expr.addr)
                        new_temp = self.new_temp()
                        self.current_symbol_table[idf] = (new_temp, self.temp_size)
                        self.temp_size = self.temp_size + size - 1
                    else:
                        raise SyntaxError('ERROR: definition of variable with array type needs an explicit size or an initializer')
            else:
                raise SyntaxError('ERROR: Already declare a variable with same identifier, choose another name.')
            self.id_list_prime()
        else:
            raise SyntaxError('ERROR12!!!')


    def id_list_prime(self):
        if self.input_token.get_value() == ',':
            self.match2('value',',')
            idf = self.input_token.get_value()
            array_flag, node_expr = self.id_()  # return if this id is an array, and the expression(size) of the array
            self.variables += 1
            if idf not in self.current_symbol_table:
                if array_flag == False:
                    new_temp = self.new_temp()
                    self.current_symbol_table[idf] = (new_temp, self.temp_size)
                else:
                    if node_expr.addr.isdigit():
                        #self.output.append(idf+'['+node_expr.addr+']')
                        size = int(node_expr.addr)
                        new_temp = self.new_temp()
                        self.current_symbol_table[idf] = (new_temp, self.temp_size)
                        self.temp_size = self.temp_size + size -1
                    else:
                        raise SyntaxError('ERROR: definition of variable with array type needs an explicit size or an initializer')
            else:
                raise SyntaxError('ERROR: Already declare a variable with same identifier, choose another name.')
            self.id_list_prime()
        elif self.input_token.get_value() == ';':
            pass
        else:
            raise SyntaxError('ERROR13!!!')

    def id_(self):
        if self.input_token.get_name() == 'identifier':
            idf = self.input_token.get_value()
            self.match2('name','identifier')
            if self.input_token.get_value() == '[':
                array_flag = True
                node_expr = self.id_tail() 
                return array_flag, node_expr       # return if current identifier is an array or not.
            else:
                array_flag = False
                node_expr = Node('None','','')
                self.id_tail()
                return array_flag, node_expr
        else:
            raise SyntaxError('ERROR14!!!')

    def id_tail(self):
        if self.input_token.get_value() == '[':
            self.match2('value','[')
            node_expr = self.expression()
            #if node_expr.addr.isdigit():
            #    self.output.append(node_expr.addr)
            #else:
            #    raise SyntaxError('ERROR: definition of variable with array type needs an explicit size or an initializer')
            self.match2('value',']')
            return node_expr
        elif self.input_token.get_value() in [',','==',';']:
            pass
        else:
            raise SyntaxError('ERROR15!!!')

    # parameter label is the label right out of block statement 
    def block_stmts(self, label = None):
        if self.input_token.get_value() == '{':
            self.match2('value','{')
            #if label != None:
            #    print label
            self.stmts(label)
            self.match2('value','}')
        elif self.input_token.get_name() == 'identifier':
            self.statement()
        elif self.input_token.get_value() in ['printf','scanf','if','while','return','break','continue','for']: 
            self.statement(label)
        else:
            raise SyntaxError('ERROR16!!!')
    
    def stmts(self, label = None):
        if self.input_token.get_name() in ['identifier','reserved_words','type_name']:
            self.statement(label)
            self.stmts(label)
        elif self.input_token.get_value() == '}':
            pass
        else:
            raise SyntaxError('ERROR17!!!')

    # since assignment and general function both start with ID
    def statement(self, label = None):
        #if label != None:
        #    print label
        self.statements += 1
        if self.input_token.get_name() == 'identifier':
            idf = self.input_token.get_value()
            self.match('name','identifier')
            if self.input_token.get_value() in ['[','=','++','--']:
                self.assignment(idf)
            elif self.input_token.get_value() == '(':
                node_general_function_call = self.general_func_call(idf)
                self.output.append(node_general_function_call.code)
            else:
                #print self.input_token.get_value()
                raise SyntaxError('ERROR18!!!')
        elif self.input_token.get_value() == 'printf':
            self.printf_func_call()
        elif self.input_token.get_value() == 'scanf':
            self.scanf_func_call()
        elif self.input_token.get_value() == 'if':
            self.if_else_stmt(label)
        elif self.input_token.get_value() == 'while':
            self.while_stmt(label)
        elif self.input_token.get_value() == 'return':
            self.return_stmt()
        elif self.input_token.get_value() == 'break':
            print 'hahahahah'
            if label != None:
                print label + 'break'
            self.break_stmt(label)
        elif self.input_token.get_value() == 'continue':
            self.continue_stmt()
        elif self.input_token.get_value() == 'for':
            raise SyntaxError('Not Support for-loop')
            #self.for_stmt()
        else:
            raise SyntaxError('ERROR19!!!')
    
    def assignment(self, idf):
        if self.input_token.get_value() == '[':
            node_expr1 = self.id_tail()
            self.match2('value','=')
            node_expr2 = self.expression()
            self.match2('value',';')
            #self.gen()
            if idf in self.current_symbol_table:
                if node_expr1.addr.isdigit():
                    offset = self.current_symbol_table[idf][1]
                    assignment_code = self.gen(node_expr2.code + self.current_symbol_table[idf][0]+'['+ str(offset+int(node_expr1.addr))+'] =' + node_expr2.addr)
                else:
                    assignment_code = self.gen(node_expr1.code + node_expr2.code + self.current_symbol_table[idf][0]+'['+ node_expr1.addr +'] =' + node_expr2.addr)
            elif idf in self.symbol_tables['global']:
                if node_expr1.addr.isdigit():
                    offset = self.current_symbol_table[idf][1]
                    assignment_code = self.gen(node_expr2.code + self.symbol_tables['global'][idf][0]+'['+str(offset+int(node_expr1.addr))+ '] =' + node_expr2.addr)
                else:
                    assignment_code = self.gen(node_expr1.code + node_expr2.code + self.symbol_tables['global'][idf][0]+'['+ node_expr1.addr +'] =' + node_expr2.addr)
            else:
                raise SyntaxError('identifier has not been declared')
            self.output.pop()
            self.output.append(assignment_code)
        elif self.input_token.get_value() == '=':
            self.match('value','=')
            node_expr = self.expression()
            self.match('value',';')
            if idf in self.current_symbol_table:
                offset = self.current_symbol_table[idf][1]
                assignment_code = self.gen(node_expr.code + self.current_symbol_table[idf][0]+'['+str(offset)+']' + '=' + node_expr.addr)
            elif idf in self.symbol_tables['global']:
                offset = self.symbol_tables['global'][idf][1]
                assignment_code = self.gen(node_expr.code + self.symbol_tables['global'][idf][0] + '['+str(offset)+']' +'=' + node_expr.addr)
            else:
                raise SyntaxError('identifier has not been declared')
            #assignment_code = node_expr.code
            self.output.pop()
            self.output.pop() # pop last three element from output list
            self.output.pop()
            self.output.append(assignment_code)
            #self.output[self.reserved_index] = 'int '+self.current+'[' + str(self.temp_size + 1) + '];\n'
        elif self.input_token.get_value() in ['++','--']:
            self.double_plus_or_minus()
            self.match('value',';')
        else:
            raise SyntaxError('ERROR20!!!')

    def general_func_call(self,idf):
        node_general_function_call = Node('general_func_call',' ',' ')
        if self.input_token.get_value() == '(':
            self.match2('value','(')
            if self.input_token.get_name() in ['identifier','number','string'] or self.input_token.get_value() in ['-','(']:
                self.output.pop() #pop the identifier
                node_expr_list = self.expr_list()
                #self.output.append(node_expr_list.code)
                #self.output.append(idf+'('+node_expr_list.addr)
                node_general_function_call.code = self.gen(node_expr_list.code + idf +'(' + node_expr_list.addr + ')')
            else:
                self.output.pop()
                node_general_function_call.code = self.gen(idf +'( )')

            self.match2('value',')')
            self.match2('value',';')
            return node_general_function_call
        else:
            raise SyntaxError('ERROR21!!!')


    def printf_func_call(self):
        if self.input_token.get_value() == 'printf':
            self.match('value','printf')
            self.match('value','(')
            print_string = self.input_token.get_value()
            self.match('name','string')
            self.printf_func_call_tail(print_string)
        else:
            raise SyntaxError('ERROR22!!!')

    def printf_func_call_tail(self,print_string):
        if self.input_token.get_value() == ')':
            self.match('value',')')
            self.match('value',';')
        elif self.input_token.get_value() == ',':
            self.match('value',',')
            node_expr = self.expression()
            #print node_expr.code
            self.output.pop()    
            self.output.pop()
            self.output.pop()
            self.output.pop()
            self.output.append(node_expr.code)
            self.output.append('printf(' + print_string + ',' + node_expr.addr)
            self.match('value',')')
            self.match('value',';')
        else:
            raise SyntaxError('ERROR23!!!')

    def scanf_func_call(self):
        if self.input_token.get_value() == 'scanf':
            self.match('value','scanf')
            self.match('value','(')
            scan_string = self.input_token.get_value()
            self.match('name','string')
            self.match('value',',')
            self.match('value','&')
            node_expr = self.expression()
            self.output.pop()
            self.output.pop()
            self.output.pop()
            self.output.pop()
            self.output.pop()
            self.output.append(node_expr.code)
            self.output.append('scanf('+ scan_string + ', &'+ node_expr.addr )
            self.match('value',')')
            self.match('value',';')
        else:
            raise SyntaxError('ERROR24!!!')

    def expr_list(self):
        node_expr_list = Node('expr_list',' ',' ')
        if self.input_token.get_name() in ['identifier','number','string'] or self.input_token.get_value() in ['-','(']: # add 'string' as parameter for function call
            node_non_empty_expr_list = self.non_empty_expr_list()
            node_expr_list.code = node_non_empty_expr_list.code
            node_expr_list.addr = node_non_empty_expr_list.addr
            return node_expr_list
        elif self.input_token.get_value() == ')':
            #pass
            return node_expr_list
        else:
            raise SyntaxError('ERROR25!!!')

    def non_empty_expr_list(self):
        node_non_empty_expr_list = Node('non_empty_expr_list',' ',' ')
        if self.input_token.get_name() in ['identifier','number','string'] or self.input_token.get_value() in ['-','(']:  #add 'string'
            node_expr = self.expression()
            node_non_empty_expr_list.code = node_expr.code
            node_non_empty_expr_list.addr = node_expr.addr
            #print node_non_empty_expr_list.addr +'hahahhaahhahhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhh'
            if self.input_token.get_value() == ',':
                node_non_empty_expr_list_prime = self.non_empty_expr_list_prime(node_non_empty_expr_list)
                return node_non_empty_expr_list_prime
            else:
                self.non_empty_expr_list_prime(node_non_empty_expr_list)
                return node_non_empty_expr_list
        elif self.input_token.get_value() == ')':
            #return node_non_empty_expr_list
            pass
        else:
            raise SyntaxError('ERROR26!!!')

    def non_empty_expr_list_prime(self,node_non_empty_expr_list):
        node_non_empty_expr_list_prime = Node('non_empty_expr_list_prime',' ',' ')
        if self.input_token.get_value() == ',':
            #node_non_empty_expr_list_prime = Node('non_empty_expr_list_prime','','')
            self.match2('value',',')
            node_expr2 = self.expression()
            node_non_empty_expr_list_prime.addr = node_non_empty_expr_list.addr + ',' + node_expr2.addr
            node_non_empty_expr_list_prime.code = node_non_empty_expr_list.code + node_expr2.code
            if self.input_token.get_value() == ',':
                node_non_empty_expr_list_prime = self.non_empty_expr_list_prime(node_non_empty_expr_list_prime)
            else:
                self.non_empty_expr_list_prime(node_non_empty_expr_list_prime)
            return node_non_empty_expr_list_prime
        elif self.input_token.get_value() == ')':
            pass
            #return node_non_empty_expr_list_prime 
        else:
            raise SyntaxError('ERROR27!!!')
    
    def if_else_stmt(self, label= None):
        if self.input_token.get_value() == 'if':
            cfnode_if_else_stmt = CFNode('if_else_stmt','','','')
            true_label = self.new_label()
            false_label = self.new_label()
            cfnode_if_stmt,last_pos, last_token, last_index = self.if_stmt(true_label, false_label)
            #cfnode_if_else_stmt.code = cfnode_if_stmt.code
            self.scanner.infile.seek(last_pos)
            self.input_token = last_token
            self.output = self.output[0:last_index]
            self.output.append(cfnode_if_stmt.code)
            self.block_stmts(label)                          # this will simply match and output the code
            if self.input_token.get_value() == 'else':
                #cfnode_if_stmt.false = self.new_label()
                cfnode_else_stmt,last_pos2, last_token2, last_index2, next_label = self.else_stmt(cfnode_if_stmt)
                #cfnode_if_else_stmt.code = cfnode_if_else_stmt.code + cfnode_else_stmt.code
                self.scanner.infile.seek(last_pos2)   # because we need to check the next_label after else_stmt
                self.input_token = last_token2
                self.output = self.output[0:last_index2]
                self.output.append(cfnode_else_stmt.code)
                self.block_stmts(label)
                self.output.append(next_label + ': ')
                #return cfnode_if_else_stmt
            else:
                #cfnode_if_stmt.false = self.new_label()
                self.else_stmt(cfnode_if_stmt)
                self.output.append('\n'+ false_label+': ;')
                #cfnode_if_else_stmt.code =  cfnode_if_stmt.code
            #self.output.append(cfnode_if_else_stmt.code)
        else:
            raise SyntaxError('ERROR28!!!')


    # for convinencely generate code for block stmts, we need to return these 3 values
    def if_stmt(self, true_label, false_label):
        if self.input_token.get_value() == 'if':
            cfnode_if_stmt = CFNode('if_stmt','',true_label,false_label)
            #cfnode_if_stmt.true = self.new_label()
            self.match2('value','if')
            self.match2('value','(')
            cfnode_condition_expr = self.condition_expr(true_label,false_label)  #boolean expression
            #self.output.append(node_condition_expr.code)
            #self.output.append('if('+node_condition_expr.addr)
            self.match2('value',')')
            #node_block_stmt = self.block_stmts()
            cfnode_if_stmt.code = cfnode_condition_expr.code + cfnode_if_stmt.true + ': '

            last_pos = self.scanner.infile.tell()
            last_token = self.input_token
            last_index = len(self.output)

            #self.block_stmts() # append the code in block_stmts into output list.
            return cfnode_if_stmt, last_pos, last_token, last_index
        else:
            raise SyntaxError('ERROR28!!!')
    

    # for convinencely generate code for block stmts, we need to return these 4 values 
    def else_stmt(self, cfnode_if_stmt):
        if self.input_token.get_value() == 'else':
            cfnode_else_stmt = CFNode('else_stmt','','','')
            self.match('value','else')
            self.output.pop()
            #node_block_stmts = self.block_stmts()
            next_label = self.new_label()
            cfnode_else_stmt.code =  self.gen('goto ' + next_label + ';') + '\n' + cfnode_if_stmt.false + ':'

            last_pos = self.scanner.infile.tell()
            last_token = self.input_token
            last_index = len(self.output)

            return cfnode_else_stmt, last_pos, last_token, last_index, next_label
        elif self.input_token.get_value() in ['}','printf','scanf','if','while','return','break','continue','for']:
            pass
        elif self.input_token.get_name() == 'identifier':
            pass
        else:
            #print self.input_token.get_value()+'**********************'
            raise SyntaxError('ERROR28!!!')

    def for_stmt(self):
        if self.input_token.get_value() == 'for':
            self.match('value','for')
            self.match('value','(')
            self.for_block_1()
            self.for_block_2()
            self.for_block_3()
            self.match('value',')')
            self.block_stmts()
        else:
            raise SyntaxError('ERROR28!!!')

    def for_block_1(self):
        if self.input_token.get_name() == 'identifier':
            idf = self.input_token.get_value()
            self.match('name','identifier')
            self.assignment(idf)
        else:
            raise SyntaxError('ERROR28!!!')

    def for_block_2(self):
        if self.input_token.get_name() in ['identifier','number'] or self.input_token.get_value() in ['-','(']:
            self.condition_expr()
            self.match('value',';')
        else:
            raise SyntaxError('ERROR28!!!')

    def for_block_3(self):
        if self.input_token.get_name() == 'identifier':
            self.match('name','identifier')
            self.double_plus_or_minus()
        else:
            raise SyntaxError('ERROR28!!!')

    def double_plus_or_minus(self):
        if self.input_token.get_value() in ['++','--']:
            self.match('value',self.input_token.get_value())
        else:
            raise SyntaxError('ERROR28!!!')

    def condition_expr(self,true_label, false_label):
        if self.input_token.get_name() in ['identifier','number'] or self.input_token.get_value() in ['-','(']:
            cfnode_condition_expr = CFNode('condition_expr','',true_label,false_label)
            #node_condition_expr.true = self.new_label()
            #node_condition_expr.false = self.new_label()
            last_pos = self.scanner.infile.tell()
            last_token = self.input_token
            cfnode_condition = self.condition('','')
            if self.input_token.get_value() == '&&':
                self.scanner.infile.seek(last_pos)
                self.input_token = last_token
                new_true_label = self.new_label()
                cfnode_condition = self.condition(new_true_label, false_label)
                cfnode_condition_tail = self.condition_tail(true_label,false_label)
                cfnode_condition_expr.code = cfnode_condition.code + cfnode_condition.true +': '+ cfnode_condition_tail.code
                #cfnode_condition_expr.addr = cfnode_condition_expr.addr
            elif self.input_token.get_value() == '||':
                self.scanner.infile.seek(last_pos)
                self.input_token = last_token
                new_false_label = self.new_label()
                cfnode_condition = self.condition(true_label, new_false_label)
                cfnode_condition_tail = self.condition_tail(true_label,false_label)
                cfnode_condition_expr.code = cfnode_condition.code + cfnode_condition.false + ': ' + cfnode_condition_tail.code
            else:
                self.scanner.infile.seek(last_pos)
                self.input_token = last_token
                cfnode_condition = self.condition(true_label, false_label)
                self.condition_tail('','')
                cfnode_condition_expr.code = cfnode_condition.code
                #cfnode_condition_expr.addr = cfnode_condition.addr
            return cfnode_condition_expr
        else:
            raise SyntaxError('ERROR29!!!')

    def condition_tail(self, true_label, false_label):
        if self.input_token.get_value() in ['&&','||']:
            cfnode_condition_tail = CFNode('condition_tail','','','')
            cond_op = self.input_token.get_value()
            self.condition_op()
            cfnode_condition2 = self.condition(true_label, false_label)
            cfnode_condition_tail.code =  cfnode_condition2.code
            #cfnode_condition_tail.addr = cfnode_condition1.addr + cond_op + cfnode_condition2.addr
            return cfnode_condition_tail
        elif self.input_token.get_value() in [')',';']:
            pass
        else:
            raise SyntaxError('ERROR30!!!')

    def condition_op(self):
        if self.input_token.get_value() in ['&&','||']:
            self.match('value',self.input_token.get_value())
            self.output.pop()
        else:
            raise SyntaxError('ERROR31!!!')

    def condition(self, true_label, false_label):
        if self.input_token.get_name() in ['identifier','number'] or self.input_token.get_value() in ['-','(']:
            cfnode_condition = CFNode('condition','',true_label,false_label)
            node_expr1 = self.expression()
            comp_op = self.input_token.get_value()
            self.comparison_op()
            node_expr2 = self.expression()
            #print node_expr1.addr+'-------------------------------------------------------------------'
            cfnode_condition.code = node_expr1.code + node_expr2.code + self.gen('if (' + node_expr1.addr + comp_op + node_expr2.addr + ') goto ' + cfnode_condition.true) + self.gen('   goto ' + cfnode_condition.false)
            #node_condition.addr = node_expr.addr + comp_op + node_expr2.addr
            return cfnode_condition
        else:
            raise SyntaxError('ERROR32!!!')

    def comparison_op(self):
        if self.input_token.get_value() in ['==','!=','>','>=','<','<=']:
            self.match('value',self.input_token.get_value())
            self.output.pop()
        else:
            raise SyntaxError('ERROR33!!!')

    def while_stmt(self, label = None):
        if self.input_token.get_value() == 'while':
            begin_label = self.new_label()
            true_label = self.new_label()
            false_label = self.new_label()
            self.match2('value','while')
            self.match2('value','(')
            cfnode_condition_expr = self.condition_expr(true_label, false_label)
            self.match2('value',')')
            self.output.append('\n'+ begin_label+': ' + cfnode_condition_expr.code + cfnode_condition_expr.true +': ')
            self.block_stmts(false_label)
            self.output.append(self.gen('\n  goto ' + begin_label ))
            self.output.append(false_label + ': ;')
        else:
            raise SyntaxError('ERROR34!!!')

    def return_stmt(self):
        if self.input_token.get_value() == 'return':
            self.match('value','return')
            self.return_stmt_tail()
        else:
            raise SyntaxError('ERROR35!!!')

    def return_stmt_tail(self):
        if self.input_token.get_name() in ['identifier','number'] or self.input_token.get_value() in ['-','(']:
            node_expr = self.expression()
            self.output.pop()
            self.output.append(node_expr.code)
            self.output.append('return '+ node_expr.addr)
            self.match('value',';')
        elif self.input_token.get_value() == ';':
            self.match('value',';')
        else:
            raise SyntaxError('ERROR36!!!')

    def break_stmt(self, label = None):
        if self.input_token.get_value() == 'break':
            self.match2('value','break')       # skip the break, if we generate code for break, it will not followed 'switch' or if stmt, will raise error
            if label != None:
               self.output.append('goto ' + label)
            self.match('value',';')
        else:
            raise SyntaxError('ERROR37!!!')

    def continue_stmt(self):
        if self.input_token.get_value() == 'continue':
            self.match('value','continue')
            self.match('value',';')
        else:
            raise SyntaxError('ERROR38!!!')

    # based on precedence and associativity to figure out the attribute grammar
    # just simply pass the attribute from node to node
    def expression(self):
        node_expr = Node('expr','','')
        if self.input_token.get_name() in ['identifier','number'] or self.input_token.get_value() in ['-','(']:
            node_term = self.term()
            if self.input_token.get_value() in ['+','-']:
                #node_expr.addr = self.new_temp()
                #node_expr_prime, add_op = self.expression_prime(node_term)
                #self.gen(node_expr.addr + '=' + node_term.addr + add_op + node_expr_prime.addr + ';\n')
                node_expr_prime = self.expression_prime(node_term)
                node_expr.addr = node_expr_prime.addr
                node_expr.code = node_expr_prime.code
            else:
                node_expr.addr = node_term.addr
                node_expr.code = node_term.code
                self.expression_prime(node_term)
            return node_expr
        elif self.input_token.get_name() == 'string':  #addition support
            self.match('name','string')
        else:
            raise SyntaxError('ERROR39!!!')

    def expression_prime(self,node_term):
        if self.input_token.get_value() in ['+','-']:
            node_expr_prime = Node('expr_prime','','')
            value = self.new_temp()
            node_expr_prime.addr = value +'[' + str(self.temp_size) + ']'
            add_op = self.input_token.get_value()
            self.addop()
            node_term2 = self.term()
            #print node_term2.code   # since mul_op have higher precendence , use node_term2.code instead node_term.code
            if node_term.addr.isdigit()  and node_term2.addr.isdigit():
                value = str(self.make_bin_op(add_op,node_term.addr,node_term2.addr))
                node_expr_prime.addr = value
                node_expr_prime.code = self.gen(node_term.code + node_term2.code + node_expr_prime.addr + '=' + value)
            else:
                node_expr_prime.code = self.gen(node_term.code + node_term2.code + node_expr_prime.addr + '=' + node_term.addr + add_op + node_term2.addr)
            if self.input_token.get_value() in ['+','-']:
                #node_expr_prime.addr = value
                node_expr_prime = self.expression_prime(node_expr_prime)
                return node_expr_prime
            else:
                self.expression_prime(node_term)
                return node_expr_prime
        elif self.input_token.get_value() in [';','==','!=','>','>=','<','<=',',',')',']','&&','||']:
            pass
        else:
            raise SyntaxError('ERROR40!!!')

    def addop(self):
        if self.input_token.get_value() in ['+','-']:
            self.match2('value',self.input_token.get_value())
        else:
            raise SyntaxError('ERROR41!!!')

    def term(self):
        node_term = Node('term','','')
        if self.input_token.get_name() in ['identifier','number'] or self.input_token.get_value() in ['-','(']:
            #print self.input_token.get_value() + '***********'
            node_factor = self.factor()
            if self.input_token.get_value() in ['*','/']:
                #node_term.addr = self.new_temp()
                #node_term_prime = self.term_prime(node_factor)
                #self.gen(node_term.addr + '=' + node_term_prime.addr + ';\n')
                node_term_prime = self.term_prime(node_factor)
                node_term.addr = node_term_prime.addr
                node_term.code = node_term_prime.code
                print node_term.code
            else:
                node_term.addr = node_factor.addr
                node_term.code = node_factor.code
                self.term_prime(node_factor)
            return node_term
        else:
            raise SyntaxError('ERROR42!!!')


    def term_prime(self, node_factor):
        if self.input_token.get_value() in ['*','/']:
            node_term_prime = Node('term_prime','','')
            value = self.new_temp()
            offset = self.temp_size
            node_term_prime.addr = value+'['+str(offset)+']'
            mul_op = self.input_token.get_value()  
            self.mulop()
            node_factor2 = self.factor()
            if node_factor.addr.isdigit() and node_factor2.addr.isdigit():
                value = str(self.make_bin_op(mul_op,node_factor.addr,node_factor2.addr))
                node_term_prime.addr = value
                #node_term_prime.code = self.gen(node_factor.code + node_factor2.code + node_term_prime.addr + '=' + value)
            else:
                node_term_prime.code = self.gen(node_factor.code + node_factor2.code + node_term_prime.addr + '=' + node_factor.addr + mul_op + node_factor2.addr)
            #print node_term_prime.code
            if self.input_token.get_value() in ['*','/']:
                #node_term_prime.addr = value
                node_term_prime = self.term_prime(node_term_prime)
                return node_term_prime
            else:
                self.term_prime(node_factor)   # check if exist syntax error
                #print node_term_prime.code
                return node_term_prime
        elif self.input_token.get_value() in ['+','-',';','==','!=','>','>=','<','<=',',',')',']','&&','||']:
            pass
        else:
            raise SyntaxError('ERROR43!!!')


    def mulop(self):
        if self.input_token.get_value() in ['*','/']:
            self.match2('value',self.input_token.get_value())
        else:
            raise SyntaxError('ERROR44!!!')


    # when we see an operator, we need to generate code, 
    #otherwise just simply assign the address.
    def factor(self):
        node_factor = Node('factor','','')
        if self.input_token.get_name() == 'identifier':
            idf = self.input_token.get_value()
            self.match2('name','identifier')
            if self.input_token.get_value() == '[':
                node_factor_tail = self.factor_tail(idf)
                node_factor.addr = self.new_temp() + '[' + str(self.temp_size) + ']'
                node_factor.code = self.gen(node_factor_tail.code + node_factor.addr  + '=' + node_factor_tail.addr)        # attention
            elif self.input_token.get_value() == '(':
                node_factor_tail = self.factor_tail(idf)
                node_factor.addr = self.new_temp() + '[' + str(self.temp_size) + ']'
                node_factor.code = self.gen(node_factor_tail.code + node_factor.addr +'=' + idf+'(' + node_factor_tail.addr + ')')
            else:
                self.factor_tail(idf)
                if idf in self.current_symbol_table:
                    offset = self.current_symbol_table[idf][1]
                    node_factor.addr = self.current_symbol_table[idf][0] + '[' + str(offset) + ']'
                elif idf in self.symbol_tables['global']:
                    offset = self.symbol_tables['global'][idf][1]
                    node_factor.addr =  self.symbol_tables['global'][idf][0]+'[' + str(offset) + ']'
                    #node_facot.code = self.gen( node_factor.addr + '=' + idf)
                else:
                    node_factor.addr = self.new_temp() + '[' + str(self.temp_size) + ']'
                    node_factor.code = self.gen( node_factor.addr + '=' + idf)
                    #node_factor.addr =  self.current_symbol_table[idf][0]

        elif self.input_token.get_name() == 'number':
            const = self.input_token.get_value()
            self.match2('name','number')
            node_factor.addr = const
            #if const not in self.current_symbol_table:
            #    new_temp = self.new_temp()
            #    self.current_symbol_table[const] = (new_temp,1)
            #    node_factor.addr = new_temp
            #    node_factor.code = self.gen(new_temp + '=' + const)
        elif self.input_token.get_value() == '-':
            self.match2('value','-')
            const = self.input_token.get_value()
            self.match2('name','number')
            node_factor.addr = self.new_temp() + '[' + str(self.temp_size) + ']'
            node_factor.code = self.gen(node_factor.addr + '=' + '-' + const)
            #if const not in self.current_symbol_table:
            #    node_factor.code = self.gen(node_factor.addr + '=' + '-' + const)
            #else:
            #    node_factor.code = self.gen(node_factor.addr + '=' + '-' + self.current_symbol_table[const][0])
        elif self.input_token.get_value() == '(':
            self.match2('value','(')
            node_expression = self.expression()
            node_factor.addr = node_expression.addr
            node_factor.code = node_expression.code
            self.match2('value',')')
        else:
            raise SyntaxError('ERROR45!!!')
        return node_factor

    
    # for array acess or function call
    def factor_tail(self, idf):
        node_factor_tail = Node('factor_tail','','')
        if self.input_token.get_value() == '[':
            self.match2('value','[')
            node_expr = self.expression()
            self.match2('value',']')
            if idf in self.current_symbol_table:
                if node_expr.addr.isdigit():
                    offset = self.current_symbol_table[idf][1] 
                    node_factor_tail.addr = self.current_symbol_table[idf][0]+'['+str(offset+int(node_expr.addr))+']'
                    #node_factor_tail.addr = 'idf['+node_expr.addr+']'
                    node_factor_tail.code = node_expr.code
                    return node_factor_tail
                else:
                    node_factor_tail.addr = self.current_symbol_table[idf][0]+'['+node_expr.addr+']'
                    node_factor_tail.code = node_expr.code
                    return node_factor_tail
            elif idf in self.symbol_tables['global']:
                if node_expr.addr.isdigit():
                    offset  = self.symbol_tables['global'][idf][1]
                    node_factor_tail.addr = self.symbol_tables['global'][idf][0]+'['+str(offset+int(node_expr.addr))+']'
                    node_factor_tail.code = node_expr.code
                    return node_factor_tail
                else:
                    node_factor_tail.addr = self.symbol_tables['global'][idf][0]+'['+node_expr.addr+']'
                    node_factor_tail.code = node_expr.code
                    return node_factor_tail
            else:
                raise SyntaxError('Error: array has not been declared!!')
        elif self.input_token.get_value() == '(':
            self.match2('value','(')
            node_expr_list = self.expr_list()
            self.match2('value',')')
            node_factor_tail.code = node_expr_list.code
            #print node_factor_tail.code +'7777777777777777777777777777777777777777777777'
            node_factor_tail.addr = node_expr_list.addr
            #print node_factor_tail.addr +'8888888888888888888888888888888888888888888888'
            return node_factor_tail
        elif self.input_token.get_value() in ['+','-','*','/',';','==','!=','>','>=','<','<=',',',')',']','&&','||']:
            pass
        else:
            #print self.input_token.get_value() +'********************'
            raise SyntaxError('ERROR46!!!')


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
            print 'ERROR!!!'


    def make_un_op(self, op, value):
        if op == '-':
            return 0-int(value)
        else:
            print 'ERROR!!!'
 

if __name__ == '__main__':
    outfile  = open('output.c','w')
    scanner = tokenizer.Scanner(sys.argv[1],outfile)
    parser  = Parser(scanner)
    parser.program()
    for code in parser.output:
        #print code
        outfile.write(code)
    outfile.close()
    print 'pass'
    print parser.variables
    print parser.functions
    print parser.statements
    print 'symbol_tables:' + str(parser.symbol_tables)
    call(["gcc","output.c","-o","a.out"])
