from random import shuffle, sample


#  !!!!! MAX 94 CHAR !!!!!

'''
for x in range(126 - 33):
	print(f"{x}: '{chr(x+32)}'")
ord("a")
'''

def print_table(cypher2d):
	for row in cypher2d:
		for char in row:
			print(f"{char} ", sep=' ', end='', flush=True)
		print("")


def decrypt(cypher2d):  # todo more rows
	out = list(zip(cypher2d[0], cypher2d[1]))
	out.sort()
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
		out[-1] = cypher[0]
		out.append(cypher[1])
	return out
