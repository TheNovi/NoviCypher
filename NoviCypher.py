from random import shuffle, sample


class Cypher:
	original_text = ''
	# text = ''
	encrypted = []
	decrypted = ''

	def __init__(self, text):
		self.encrypted = [text]
		self.original_text = text

	def add_lines(self, rows=1):
		out = [[str(x) for x in self.encrypted.pop(-1)]]
		for _ in range(rows):
			cypher = self.__add_line__(out[-1])
			out[-1] = cypher[1]
			out.append(cypher[0])
		self.encrypted = self.encrypted + list(reversed(out))

	def print_table(self):
		for row in self.encrypted:
			for item in row:
				print(item, end=" ")
			print("")

	def decrypt(self):
		cypher = self.encrypted[:]
		out = cypher
		for i in range(len(cypher) - 1):
			out = list(zip(cypher[i], cypher[i + 1]))
			out.sort()
			cypher[i + 1] = [x[1] for x in out]
		self.decrypted = ''.join([str(x[1]) for x in out])
		return self.decrypted

	@staticmethod
	def __add_line__(t):
		o = list(zip([chr(x) for x in sorted(sample(range(33, 127), len(t)))], t))
		shuffle(o)
		out = [list(x) for x in zip(*o)]
		return out
