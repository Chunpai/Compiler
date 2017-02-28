#!/usr/bin/env ruby
# Author: Jin Chul Ann
# Class: CSC 254 Fall 2014 MW 2-3PM
# Professor: Chen Ding
# TA: Jake Brock, Kevin Hu
# Homework 7(?): Singularity Assignment
# file name: interpreter.rb 

require 'readline'

# uses hashtable to create environment (env)
class Env < Hash
	# sets cur_env to denote current environment
	attr_accessor :cur_env

	# initializes using two array and hashtable
	#
	# @param [Array, Array, Hash] initialize parameter and arugment and stores them under the env
	def initialize(x =[], clos = [], cur_env=nil)
		if cur_env == nil
			cur_env = Hash.new
		end
		@cur_env = cur_env
		x.zip(clos).each{|p| store(*p)}
	end

	# accesses the env to find the arugment that the parameter has
	#
	# @param [Symbol] [] a symbol
	# @return [String] the argument that parameter have
	def [](name)
		return super(name) if super(name) != nil
		return @cur_env[name] if @cur_env[name] != nil
		puts name.to_s + " is not defined."
		return nil
	end
end

# brings out interpret which interprets each line
class Interpret

	attr_accessor :count
	# calls other functions to interpret
	#
	# @param [nil] interpreting does not take any param
	# @return [nil] only outputs with no return
	def interpreting
		
		puts "Scheme interpreter in Ruby"
		env = Env.new
		env.cur_env.update({ :+ => lambda{|*p| eval p.join('+')}, :* => lambda{|*p| eval p.join('*')}, :- => lambda{|*p| eval p.join('-')}, :/ => lambda{|*p| eval p.join('/')}})
		while line = Readline.readline(" >> ", true)
			begin
				@count = 0
				t1 = Time.now
				_val = parse(line)
				p _val
				x = _eval(_val, env)
				t2 = Time.now
				msec = (t2- t1)*100.0
				puts "Took #{msec.round(5)} milliseconds to evaluate."
				puts to_output(x) if x
			rescue SystemStackError => e
				t2 = Time.now
				msec = (t2- t1)*100.0
				puts "Took #{msec.round(5)} to return error."
				puts "STACK LEVEL: #{@count}"
				puts "Error: #{e}"
			end

		end
	end

	# parses the string and returns array
	# 
	# @param [String] parse parses the line taken in
	# @return [Array]
	def parse (input)
		return parse_tail(input.gsub('(', ' ( ').gsub(')', ' ) ').split)
	end

	# helper method for parse
	#
	# @param [String] parse_tail takes the line/string
	# @return [Array]
	def parse_tail(tok)
		if tok.size == 0
			raise SyntaxError, 'EOF unexpected'
		end
		first_tok = tok.delete_at(0)
		if '(' == first_tok
			x = []
			while tok[0] != ')'
				x << parse_tail(tok)
			end
			tok.delete_at(0)
			return x
		elsif ')' == first_tok
			raise SyntaxError, '\')\' unexpected'
		else
		  	return convert_tok(first_tok)
		end
	end

	# helper method for parse_tail
	# converts each token to either Integer, Float or Symbol (symbol is any non-number)
	# 
	# @param [String] convert_tok takes in the String
	# @return [Symbol]
	def convert_tok(token)
		if token.to_i.to_s == token
			return Integer(token)
		elsif token.to_f.to_s == token
			return Float(token)
		else
			token.to_sym
		end
	end

	# eval function for the evaluator
	#
	# @param [Array, Hash] _eval takes parsed expression and env
	# @return [Number] the evaluated result
	def _eval(m, env)
		@count+=1
		if m.is_a? Symbol
			return env[m]
 		elsif !m.is_a? Array
 			return m
 		end
		case m[0]
		when :lambda
			__, x, m1 = m[0], [m[1]], [m[2]]
			Proc.new{|*clos| _eval(m1, Env.new(x, clos, env))}
		else
			exprs = m.map { |expr| _eval(expr, env)}
			return exprs[0] if !exprs[0].is_a? Proc
			exprs[0].call(*exprs[1..-1])
		end
	end

	# converts the evaluated expression into an output
	#
	# @param [Array] to_output takes in the expression that is already evaluated
	# @return [String] the user friendly readable output
	def to_output(expr)
		if expr.kind_of? Array
			expr.map { |x| to_output(x) + " "}.join[0..-2]
		else
			expr.to_s
		end
	end
end

interpreter = Interpret.new
interpreter.interpreting
