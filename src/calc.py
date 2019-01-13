INTEGER, PLUS, EOF = 'INTEGER', 'PLUS', 'EOF'

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

	def get_next_token(self):
		text = self.text

		if self.indexInText > len(text) - 1:
			return Token(EOF, None)

		currentChar = text[self.indexInText]

		if currentChar.isdigit():
			token = Token(INTEGER, int(currentChar))
			self.indexInText += 1
			return token

		if currentChar == '+':
			token = Token(PLUS, currentChar)
			self.indexInText += 1
			return token

		raise Exception("Invalid input: {}".format(currentChar))

	def eat(self, tokenType):
		if self.currentToken.type == tokenType:
			self.currentToken = self.get_next_token()
		else:
			raise Exception("Invalid input. Current token is of type {}, but looking for type {}".format(
				self.currentToken.type,
				tokenType))

	def expr(self):
		self.currentToken = self.get_next_token()

		left = self.currentToken
		self.eat(INTEGER)

		operation = self.currentToken
		self.eat(PLUS)

		right = self.currentToken
		self.eat(INTEGER)

		result = left.value + right.value
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