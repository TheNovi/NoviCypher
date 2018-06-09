from random import shuffle, sample

supported_characters = ''.join(chr(x) for x in range(33, 127))
max_length = len(supported_characters)  # !!!!! MAX 94 CHAR !!!!!


def print_table(cypher2d):
	for row in cypher2d:
		for char in row:
			print(f"{char} ", sep=' ', end='', flush=True)
		print("")


def decrypt(cypher):
	out = cypher
	for i in range(len(cypher)-1):
		out = list(zip(cypher[i], cypher[i+1]))
		out.sort()
		cypher[i+1] = [x[1] for x in out]
	return ''.join([x[1] for x in out])


def __encrypt__(text):
	o = list(zip([chr(x) for x in sorted(sample(range(33, 127), len(text)))], text))
	shuffle(o)
	out = [list(x) for x in zip(*o)]
	return out


def smart_encrypt(text, rows=1):
	out = [[x for x in text]]
	for _ in range(rows):
		cypher = __encrypt__(out[-1])
		out[-1] = cypher[1]
		out.append(cypher[0])
	return list(reversed(out))
