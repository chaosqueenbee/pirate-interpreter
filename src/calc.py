INTEGER, PLUS, MINUS, EOF = 'INTEGER', 'PLUS', 'MINUS', 'EOF'

class Token(object):
    def __init__(self, type, value):
    	self.type = type
    	self.value = value

    def __string__(self):
    	return 'Token({type}, {value})'.format(
            type = self.type,
            value = repr(self.value))

    def __repr__(self):
        return self.__str__()

class Interpreter(object):
	def __init__(self, text):
		self.text = text
		# position in self.text
		self.indexInText = 0
		# current token index
		self.currentToken = None

	def get_integer(self):
		result = ''
		curChar = self.text[self.indexInText]
		while curChar is not None and curChar.isdigit():
			result += curChar
			self.indexInText += 1
			if self.indexInText > len(self.text) - 1:
				curChar = None  # Indicates end of input
			else:
				curChar = self.text[self.indexInText]
		return int(result)

	def get_next_token(self):
		text = self.text

		if self.indexInText > len(text) - 1:
			return Token(EOF, None)

		currentChar = text[self.indexInText]

		if currentChar.isspace():
			self.indexInText += 1
			token = self.get_next_token()
			return token

		if currentChar.isdigit():
			token = Token(INTEGER, self.get_integer())
			return token

		if currentChar == '+':
			token = Token(PLUS, currentChar)
			self.indexInText += 1
			return token

		if currentChar == '-':
			token = Token(MINUS, currentChar)
			self.indexInText += 1
			return token

		raise Exception("Invalid input: {}".format(currentChar))

	def eatAndGetValue(self, tokenType):
		if self.currentToken.type == tokenType:
			token = self.currentToken
			self.currentToken = self.get_next_token()
			return token.value
		else:
			raise Exception("Invalid input. Current token is of type {}, but looking for type {}".format(
				self.currentToken.type,
				tokenType))

	def expr(self):
		self.currentToken = self.get_next_token()

		result = self.eatAndGetValue(INTEGER)

		while self.currentToken.type in (PLUS, MINUS):
			token = self.currentToken
			if token.type == PLUS:
				self.eatAndGetValue(PLUS)
				result += self.eatAndGetValue(INTEGER)
			elif token.type == MINUS:
				self.eatAndGetValue(MINUS)
				result -= self.eatAndGetValue(INTEGER)
		return result

def main():
	while True:
		try:
			text = raw_input('calc> ')
		except EOFError:
			break

		if not text:
			continue

		interpreter = Interpreter(text)
		result = interpreter.expr()
		print(result)

if __name__ == '__main__':
    main()