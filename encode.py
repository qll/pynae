#!/usr/bin/env python
#coding: utf8
import sys, re, math


# nonalpha way of creating True and False
TRUE  = "''==''"
FALSE = "''<''"
SET   = "{%s}" % FALSE

# chars which can be created without the use of %c
CHARS = "FTaelrstu0123456789"

# chars which are considered alphanumeric
ALPHANUM = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ012345679"


py3 = sys.hexversion > 0x03000000


class Encoder:
	def __init__(self, use_vars = False, var_name = ''):
		"""
		The Encoder contains all methods to generate nonalpha Python strings from a
		normal string. Parameters:
		use_vars - Determines if the Encoder should use variables for True, False and stuff like that
		var_name - Name of the variable which will hold the built string at the end. If empty
		           this script ist just going to build the string.
		"""
		self.use_vars = use_vars
		self.var_name = var_name

	def _factor(self, number):
		""" Gets the prime factorization of a number. Stolen from stackoverflow :-). """
		if number < 2: return [number]
		def recurse(factors, x, n):
			if x < 2: return factors
			if n > 1 + x ** 0.5: # reached the upper limit
				factors.append(x) # the only prime left is x itself
				return factors
			if x % n == 0: # x is a factor
				factors.append(n)
				return recurse(factors, x / n, n)
			else:
				return recurse(factors, x, n + 1)
		return recurse([], number, 2)
	
	def _count_to_num(self, number):
		i = 0
		prefix = ""
		base = FALSE
		while i != number:
			if i == 1:
				prefix = ""
				base = TRUE
			if prefix.startswith('~'):
				prefix = "-" + prefix
				i = -i
			else:
				prefix = "~" + prefix
				i = ~i
		if prefix == "":
			return "(%s)*(%s)" % (base, TRUE)
		return "%s(%s)" % (prefix, base)

	def _make_num(self, number):
		madeEven = False
		numbers = self._factor(number)
		if number > 10 and len(numbers) == 1:
			numbers = self._factor(number - 1) # create an even number
			madeEven = True
		numbers = "*".join([self._count_to_num(n) for n in numbers])
		if madeEven:
			numbers += "+%s" % self._count_to_num(1)
		return numbers
	
	def _make_fmtstr(self, count):
		""" Generates %c * count. """
		return "('%%'+`'¬'`[%s])*%s" % (self._make_num(-2), self._make_num(count))
	
	def _make_from_chars(self, char):
		base = TRUE
		if char in "False":
			base = FALSE
		elif char in "set":
			base = SET
		elif char in "012345679":
			return "`%s`" % self._make_num(int(char)) 
		return "`%s`[%s]" % (base, self._make_num(str(eval(base)).find(char)))
	
	def _make_from_c(self, string):
		# create %c
		result = self._make_fmtstr(len(string))
		# format string
		result += "%%(%s)" % (",".join([self._make_num(ord(c)) for c in string]))
		return result
	
	def _flush_c_str(self, result, c_str):
		if len(c_str) != 0:
			result.append(self._make_from_c(c_str))
		return ""
	
	def _check_result(self, result):
		""" Apply some ugly hacks before pushing the string out :). """
		if self.var_name:
			result = self.var_name + '=' + result
		if self.use_vars:
			inserted_true  = False
			inserted_false = False
			prefix = ''
			if result.count(TRUE) > 1:
				prefix += '_=%s;' % TRUE
				inserted_true = True
				result = re.sub(r"\(?%s\)?" % TRUE, "_", result)
			if result.count(FALSE) > 1:
				if inserted_true:
					prefix += '__=_^_;'
				else:
					prefix += '__=%s;' % FALSE
				inserted_false = True
				result = re.sub(r"\(?%s\)?" % FALSE, "__", result)
			result = prefix + result
		return result.replace("'+'", "")
	
	def dumb_encode(self, string):
		""" Encodes the string with the %c-method only. Results in very large strings. """
		result = self._make_from_c(string)
		if not py3 and string != eval(result):
			# check result
			raise Exception("Could not create non-alphanumeric Python code.")
		return result
	
	def encode(self, string):
		""" Encodes the string with a mix of some techniques to get a short string. """
		result = []
		c_str  = ""
		for c in string:
			if c not in ALPHANUM:
				c_str = self._flush_c_str(result, c_str)
				result.append("'%s'" % c)
			elif c not in CHARS:
				c_str += c
			else:
				c_str = self._flush_c_str(result, c_str)
				result.append(self._make_from_chars(c))
		self._flush_c_str(result, c_str)
		return self._check_result("+".join(result))
	

if __name__ == "__main__":
	if py3:
		print("Warning: To execute the non-alphanumeric code, you need to use Python 2.x.")
	if len(sys.argv) < 2:
		print('Usage: %s STRING' % sys.argv[0])
		sys.exit(1)
	enc = Encoder().encode(sys.argv[1])
	print('Length: %d chars' % len(enc))
	print('')
	print(enc)

