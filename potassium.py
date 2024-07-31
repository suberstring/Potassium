import re,Token,sys,os,io

def main_program(rfile):
	sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='gb18030')
	fg = 1
	DEBUG = 0
	with open(rfile,"r+",encoding="gb18030") as ji:
		codes = ji.read()
	del fg
	flexed = []
	n = ""
	p = 0
	flag = 1
	if flag:
		for i in codes:
			n+=i
			if n[0] == "'" and n[-1] == "'" and len(n) >=2:
				flexed.append(Token.Token("string",n[1:-1]))
				n = ""
			elif re.match("[0-9]+",n) and (codes[p+1] not in "1234567890" or codes[p+1] == ";"):
				flexed.append(Token.Token("int",int(n)))
				n = ""
			elif re.match("^[$][A-Za-z0-9_~^]+",n) and codes[p+1] in "!@#$%&*()<>,.?';\"[]{ }\t\n":
				flexed.append(Token.Token("var",n))
				n = ""
			elif n[0] == "`" and n[-1] == "`":
				#注释
				#静默锤子雨伞
				n = ""
			elif n == "=":
				n = ""
				flexed.append(Token.Token("symbol","="))
			elif n == "|":
				n = ""
				flexed.append(Token.Token("symbol","|"))
			elif n == "#":
				n = ""
				flexed.append(Token.Token("symbol","#"))
			elif n == ":":
				n = ""
				flexed.append(Token.Token("symbol",":"))
			elif n == "!":
				n = ""
				flexed.append(Token.Token("symbol","!"))
			elif n == "<" or n == ">":
				flexed.append(Token.Token("symbol",n))
				n = ""
			elif n in ["print","if"]:
				flexed.append(Token.Token("sent",n))
				n = ""
			elif n == "var":
				n = ""
				flexed.append(Token.Token("keyword","var"))
			elif n == "printwn":
				n = ""
				flexed.append(Token.Token("sent","printen"))
			elif n == "if":
				n = ""
				flexed.append(Token.Token("oif","if"))
			elif n == ";":
				if n == ";":
					n = ""
					flexed.append(Token.Token("symbol",";"))
				else:
					print("Error(Main):Lexcial Error:"+n+"?-0x02")
					return -1
			elif n in "+-*/":
				flexed.append(Token.Token("symbol",n))
				n = ""
			elif n == "\n" or n == " " or n == "\t":
				n = ""
				#静默处理
				#锤子雨伞
			p+=1
	if DEBUG:
		for i in flexed:
			print("#DEBUGGER:",i.name,i.typ)

	if DEBUG:
		print("-------------")
	del p,n,codes
	if DEBUG:
		print("Clearing...")
		print("-------------")

	p = 0
	var_dict = {"$__lang__":"Potassium_Test_0.0.3","$__system__":"Windows-x64","$__path__":os.getcwd(),"$__updateinfo__":"Error/Warning,<,>"}
	this,_next=[],flexed[p]
	no_go = False
	while p < len(flexed):
		if var_dict["$__lang__"]!="Potassium_Test_0.0.3" and var_dict["$__system__"]!="Windows-x64" and var_dict["$__path__"]!=os.getcwd() and var_dict["$__updateinfo__"]!="Error/Warning,<,>":
			print("Error(Main):Change the system variable.You are so crazy:(!-(0x02)")
			return -1
		p+=1
		if DEBUG:
			print(Token.reduce_inquire(this),no_go)
		this.append(_next)
		if p != len(flexed):
			_next = flexed[p]
		else:
			_next = Token.Token("","")
		if no_go and this[-1].name != "|":
			continue
		else:
			no_go = False
		#用 if:*** if:***而不是if:*** elif:*** ----多次归约
		if this[-1].name == "var":
			this[-1].reduce("keywd")
		if this[-1].name == "if":
			this[-1].reduce("if")
		if this[-1].name == "print":
			this[-1].reduce("output")
		if this[-1].typ == "string":
			this[-1].reduce("strs")
		if this[-1].name == ";":
			this[-1].reduce("sentend")
		if this[-1].typ == "var":
			this[-1].reduce("unit")
		if this[-1].name == "=":
			this[-1].reduce("assieq")
		if this[-1].name == "#":
			this[-1].reduce("strapp")
		if this[-1].name == "|":
			this[-1].reduce("ifstru")
		if this[-1].name == ">":
			this[-1].reduce("leftbig")
		if this[-1].name == "<":
			this[-1].reduce("rightbig")	
		if this[-1].name == "!":
			this[-1].reduce("noeq")
		if this[-1].name == ":":
			this[-1].reduce("trueq")
		if this[-1].typ == "int":
			this[-1].reduce("int")
		if str(this[-1].name) in "+-*/":
			this[-1].reduce(this[-1].name)
		if Token.reduce_inquire(this[-3:]) == ["int","*","int"]:
			temp = this[-3].name * this[-1].name
			del this[-3:]
			temp = Token.Token(typ="int",name=temp)
			temp.reduce("int")
			this.append(temp)
			del temp
		if Token.reduce_inquire(this[-3:]) == ["int","/","int"]:
			temp = this[-3].name / this[-1].name
			del this[-3:]
			temp = Token.Token(typ="int",name=temp)
			temp.reduce("int")
			this.append(temp)
			del temp
		if Token.reduce_inquire(this[-3:]) == ["int","+","int"]:
			if _next.name not in ["*","/"]:
				temp = this[-3].name + this[-1].name
				del this[-3:]
				temp = Token.Token(typ="int",name=temp)
				temp.reduce("int")
				this.append(temp)
				del temp
		if Token.reduce_inquire(this[-3:]) == ["int","-","int"]:
			if _next.name not in ["*","/"]:
				temp = this[-3].name - this[-1].name
				del this[-3:]
				temp = Token.Token(typ="int",name=temp)
				temp.reduce("int")
				this.append(temp)
				del temp
		if Token.reduce_inquire(this[-3:]) == ["strs","strapp","strs"]:
			temp = this[-3].name + this[-1].name
			del this[-3:]
			temp = Token.Token(typ="string",name=temp)
			temp.reduce("strs")
			this.append(temp)
			del temp
		if Token.reduce_inquire(this[-5:]) == ["if","unit","trueq","int","ifstru"] or Token.reduce_inquire(this[-5:]) == ["if","unit","trueq","strs","ifstru"]:
			if type(var_dict[this[-4].name]) != type(this[-2].name):
				print('Error(Main):Cannot Equal Two Diffrent Values!-0x03')
				return -1
			if var_dict[this[-4].name] != this[-2].name:
				no_go = True
			del this[-5:]
		if Token.reduce_inquire(this[-5:]) == ["if","unit","noeq","int","ifstru"] or Token.reduce_inquire(this[-5:]) == ["if","unit","noeq","strs","ifstru"]:
			if type(var_dict[this[-4].name]) != type(this[-2].name):
				print('Error(Main):Cannot Equal Two Diffrent Values!-0x03')
				return -1
			if var_dict[this[-4].name] == this[-2].name:
				no_go = True
			del this[-5:]
		if Token.reduce_inquire(this[-5:]) == ["if","unit","leftbig","int","ifstru"] or Token.reduce_inquire(this[-5:]) == ["if","unit","leftbig","strs","ifstru"]:
			if type(var_dict[this[-4].name]) != type(this[-2].name):
				print('Error(Main):Cannot Equal Two Diffrent Values!-0x03')
				return -1
			if var_dict[this[-4].name] <= this[-2].name:
				no_go = True
			del this[-5:]
		if Token.reduce_inquire(this[-5:]) == ["if","unit","rightbig","int","ifstru"] or Token.reduce_inquire(this[-5:]) == ["if","unit","rightbig","strs","ifstru"]:
			if type(var_dict[this[-4].name]) != type(this[-2].name):
				print('Error(Main):Cannot Equal Two Diffrent Values!-0x03')
				return -1
			if var_dict[this[-4].name] >= this[-2].name:
				no_go = True
			del this[-5:]
		if Token.reduce_inquire(this[:5]) == ["keywd","unit","assieq","int","sentend"]:
			var_dict[this[-4].name] = this[-2].name
			del this[:5]
		if Token.reduce_inquire(this[:5]) == ["keywd","unit","assieq","strs","sentend"]:
			var_dict[this[-4].name] = this[-2].name
			del this[:5]
		if Token.reduce_inquire(this[-3:]) == ["output","strs","sentend"]:
			print(this[-2].name)
			del this[-2:]
		if Token.reduce_inquire(this[-3:]) == ["output","int","sentend"]:
			print(this[-2].name)
			del this[-2:]
		if Token.reduce_inquire(this[-3:]) == ["output","unit","sentend"]:
			print(var_dict[this[-2].name])
			del this[-2:]

try:
	main_program(sys.argv[1])
except IndexError:
	print("Error(Root):Need File!-0x01")