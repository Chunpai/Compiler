#!/usr/bin/env python
#Author: Chunpai Wang
#email: cwang64@u.rochester.edu
#implementation of Lambda Calculus with python language

import numbers
import time
count = 0

# Expr class
# Expr can do binary operation, and it has three parameters
# first paramter op is the operators, which can be '+','-','*','/'
# E1 and E2 are expression, which can be number, parameter, and function Application (Apply instance)
# Example1: Expr('+',1,2)   
# Example2: Expr('+','x',1)  
class Expr:
    def __init__(self,op,E1,E2):
        self.op = op
        self.E1 = E1
        self.E2 = E2

# Apply class
# Apply is the function application
# M1 is the first function, and M2 is the second function
# Example: Apply(M1,M2)  will create an Apply instance with M1 and M2 as function applications
class Apply:
    def __init__(self,M1,M2):
        self.M1 = M1  
        self.M2 = M2


# Lambda class
# Lambda class has two parameters, p and M.
# p is the the parameter with string type and M is the function body, which can be number, string, Expr, Lambda, and Apply object
# Example: Lambda('x','x') 
class Lambda:
    def __init__(self,p,M):
        self.p = p    # p is parameter
        self.M = M    # M is function body


# evaluate the lambda calculus
# parameters: object and environment
# object : can be number, string, Expr instance, Lambda instance,and Apply instance
def eval(obj, env = {}):   #default env is empty
    env_1 = dict(env)      #clone the environment when eval each time
    if isinstance(obj, numbers.Number):
        return obj
    elif isinstance(obj, str):
        if obj in env_1:
            return env_1[obj]
        else:
            raise NameError(obj+' undefined')  # if parameter not defined in current environment, raise error
    elif isinstance(obj, Lambda):
        return (obj,env_1)  #return a tuple to represent closure in LC
    elif isinstance(obj, Apply):
        try:
            global count 
            count += 1
            print count
            v = eval(obj.M2, env_1)
            f = eval(obj.M1, env_1)
            def_env = f[1]
            M3 = f[0].M
            def_env[f[0].p] = v
            return eval(M3, def_env)
        except:
            global start_time
            print str(time.time() - start_time) + ' seconds'
            raise Exception('stack overflow')
    elif isinstance(obj, Expr):
        if obj.op in ['+','-','*','/']:
            if isinstance(obj.E1, numbers.Number) or isinstance(obj.E1,str) or isinstance(obj.E1,Apply):
                E1_value = eval(obj.E1, env_1)
            else:
                raise SyntaxError
            if isinstance(obj.E2, numbers.Number) or isinstance(obj.E2,str) or isinstance(obj.E2,Apply):
                E2_value = eval(obj.E2, env_1)
            else:
                raise SyntaxError
            return compute(obj.op, E1_value, E2_value) 
        else:
            raise SyntaxError('Not valid Operation !!!')
    else:
        raise SyntaxError('SyntaxError')


# binary operation
# parameter op is the operator
# parameters value1 and value2 are the values of first operand and second operand, which can be any type of number
# for unary operation -x, it needs syntax make_binary_op('-',0,x)
def make_binary_op(op, value1, value2):
    if op == '+':
        return value1 + value2
    elif op == '-':
        return value1 - value2
    elif op == '*':
        return value1 * value2
    elif op == '/':
        return value1 / value2



if __name__ == '__main__':
    # test cases
    #print eval(Apply(Lambda('x','x'),1))  
    #print eval(1)
    #print eval(Lambda('x','x'))
    #print eval(Expr('+',2,3))                                                 
    #print eval(Apply(Lambda('x',Expr('+','x',1)),2))                          # same to (lambda(x (x+1) 2))
    print eval(Apply(Lambda('x',Apply('x','x')),Lambda('x',Apply('x','x'))))   # infinite loop

