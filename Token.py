def key_exist(dic,mb):
	for i in dic.keys():
		if i == mb:
			return True
	return False

def reduce_inquire(lst):
	ans = []
	for i in lst:
		ans.append(i.reduce)

	return ans

class Error:
	def typeerror(ex="0"):
		return "TypeError:"+ex
	def unnameerror(ex='0'):
		return "UnknownNameError:"+ex

class Token:
	reduce = None
	inif = False
	def __init__(self,typ,name):
		self.name = name
		self.typ = typ

	def __bool__(self):
		return bool(self.name) and bool(self.typ)

	def __add__(self):
		if type(self.name)!=type(123):
			v = Error()
			return Error.typerror("Cannot use '+' between two strings.")

	def __sub__(self):
		if type(self.name)!=type(123):
			v = Error()
			return Error.typerror("Cannot use '-' between two strings.")

	def __mul__(self):
		if type(self.name)!=type(123):
			v = Error()
			return Error.typerror("Cannot use '*' between two strings.")

	def __floordiv__(self):
		if type(self.name)!=type(123):
			v = Error()
			return Error.typerror("Cannot use '/' between two strings.")

	def __truediv__(self):
		if type(self.name)!=type(123):
			v = Error()
			return Error.typerror("Cannot use '/' between two strings.")

	def __int__(self):
		if type(self.name) != type(123):
			return ascii(self.name)
		else:
			return self.name

	def reduce(self,red):
		self.reduce	= red

	def inif(self,red):
		self.inif = red