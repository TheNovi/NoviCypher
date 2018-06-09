from random import shuffle, sample

supported_characters = ''.join(chr(x) for x in range(33, 127))
max_length = len(supported_characters)  # !!!!! MAX 94 CHAR !!!!!


def print_table(arr):
	s = "{:" + str(len(str(max(arr[0]+arr[-1])))) + "}"
	for row in arr:
		for item in row:
			print(s.format(item), end=" ")
		print("")


def decrypt(cypher, force_ascii=False):
	cypher = cypher[:]
	out = cypher
	for i in range(len(cypher)-1):
		out = list(zip(cypher[i], cypher[i+1]))
		out.sort()
		cypher[i+1] = [x[1] for x in out]
	if force_ascii or len(out) > max_length:
		return ''.join([chr(x[1]) for x in out])
	return ''.join([str(x[1]) for x in out])


def __encrypt_ascii__(text):
	o = list(zip([chr(x) for x in sorted(sample(range(33, 127), len(text)))], text))
	shuffle(o)
	out = [list(x) for x in zip(*o)]
	return out


def __encrypt_numbers__(text):
	o = list(zip([x for x in range(len(text))], text))
	shuffle(o)
	out = [list(x) for x in zip(*o)]
	return out


def smart_encrypt(text, rows=1, force_numbers=False):
	out = [[str(x) for x in text]]
	en = __encrypt_ascii__
	if force_numbers or len(text) > 94:
		en = __encrypt_numbers__
		out[0] = [ord(x) for x in out[0]]
	for _ in range(rows):
		cypher = en(out[-1])
		out[-1] = cypher[1]
		out.append(cypher[0])
	return list(reversed(out))
