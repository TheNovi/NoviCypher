from random import shuffle
from shutil import make_archive, unpack_archive, rmtree, move
from os import remove, path, makedirs


class FileCypher:
	def __init__(self, folder, rows=199, chunk=2**15):
		print('start')
		if len(folder) == 0:
			return
		self.folder = folder
		make_archive(folder, 'zip', folder)
		print('Loading file')
		a = self.__first__(chunk)
		print('Ziping for cypher')
		self.check = a
		print(f'Cypher is {len(a)}')
		a = [x for x in zip(range(len(a)), a)]
		shuffle(a)
		print('Second')
		self.ncy = self.__second__(a)
		print('Adding rows')
		if rows > 0:
			self.ncy.add_lines(rows)

		print('Saving')
		self.save_and_zip()
		print('Done\n')

	def save_and_zip(self):
		cy = self.ncy.get_cypher()
		# print(len(cy.split('\n')))
		with open(f'{self.folder}-copy/cy', 'w') as f:
			f.write(cy)
		make_archive(f'{self.folder}', 'zip', f'{self.folder}-copy')
		try:
			rmtree(f'{self.folder}-copy')
		except:
			print(f"Can't delete {self.folder}-copy folder")
		move(f'{self.folder}.zip', f'{self.folder}.ncy')

	def decrypt_file(self, folder):
		print('Unpacking')
		unpack_archive(f'{folder}.ncy', folder+'-copy', 'zip')
		a = []
		self.folder = folder
		print('Reading cy')
		with open(f'{folder}-copy/cy', 'r') as f:
			l = [x.replace('\n', '') for x in f.readlines()]
		for x in l:
			a.append([int(y) for y in x.split(' ')])
		print('Deciphering cy')
		a = Cypher.decrypt_file(a, False, True)
		print('Reading e')
		a = [[int(x) for x in a], self.read_file()]
		print('Deciphering e')
		# When i tried to give this to Cypher class to decipher. For some reason it just cant successfully copy one
		# (also fuck this line length limit) variable. I just copied whole decipher method here. FUCK THIS SHIT
		cypher = a
		out = cypher
		for i in range(len(cypher) - 1):
			out = list(zip(cypher[i], cypher[i + 1]))
			out.sort()
			cypher[i + 1] = [x[1] for x in out]
		a = [bytes.fromhex(x[1]) for x in out]
		print('Crating deciphered zip')
		self.get_file(b''.join(a))
		print('Removing temp files and unpacking')
		try:
			rmtree(f'{self.folder}-copy')
		except:
			print(f"Can't delete {self.folder}-copy folder")
		unpack_archive(f'{folder}-copy.zip', folder + '-decrypted', 'zip')
		remove(f'{folder}-copy.zip')
		print("Done (Don't forget to clear your trash bin after deleting deciphered folder)")

	def __first__(self, chunk):
		l = []
		print('Reading files')
		with open(f'{self.folder}.zip', 'rb') as f:
			while True:
				a = f.read(chunk)
				if not a:
					break
				l.append(str(a.hex())+'\n')
				# l.append(int.from_bytes(a, byteorder='little'))
		return l

	def __second__(self, a):
		l = [list(t) for t in zip(*a)]
		remove(f'{self.folder}.zip')
		if not path.exists(f'{self.folder}-copy'):
			makedirs(f'{self.folder}-copy')
		print('Parsing e')
		# o = ''
		# for ii in range(len(l[1])):
		# 	x = l[1][ii]
		# 	# if ii % 10:
		# 	print(f'{ii}/{len(l[1])}')

		# print(len(l[1][0]))
		# sleep(10)

		# o = ''.join([str(x) + '\n' for x in l[1]])
		print('Writing e')
		with open(f'{self.folder}-copy/e', 'w') as f:
			f.writelines(l[1])
		cc = Cypher('')
		cc.encrypted = [l[0]]
		return cc

	def read_file(self):
		with open(f'{self.folder}-copy/e', 'r') as f:
			l = [x.replace('\n', '') for x in f.readlines()]
		return l

	def get_file(self, a):
		with open(f'{self.folder}-copy.zip', 'wb') as f:
			# for y in [x.to_bytes((max(a).bit_length() + 7) // 8, byteorder='little') for x in a]:
			f.write(a)


class Cypher:
	original_text = ''
	# text = ''
	encrypted = []
	decrypted = ''
	chunk_size = 1

	def __init__(self, text, rows=0):
		if not str(text).isdigit():
			text = [ord(x) for x in text]
		self.encrypted = [[int(x) for x in text]]
		self.original_text = text
		if rows > 0:
			self.add_lines(rows)

	def add_lines(self, rows=1):
		out = [[x for x in self.encrypted.pop(0)]]
		for _ in range(rows):
			cypher = self.__add_line__(out[-1])
			out[-1] = cypher[1]
			out.append(cypher[0])
		self.encrypted = list(reversed(out)) + self.encrypted

	def get_cypher(self):
		out = ''
		for row in self.encrypted:
			for item in row:
				out += str(item) + ' '
			out = out[:-1] + '\n'
		return out[:-1]

	def print_table(self):
		s = "{:" + str(len(str(max(self.encrypted[0] + self.encrypted[-1])))) + "}"
		for row in self.encrypted:
			for item in row:
				print(s.format(item), end=" ")
			print("")

	@staticmethod
	def decrypt_file(l, ascii_char=True, lists=False):
		cypher = l
		out = cypher
		for i in range(len(cypher) - 1):
			out = list(zip(cypher[i], cypher[i + 1]))
			out.sort()
			cypher[i + 1] = [x[1] for x in out]
		if ascii_char:
			l = [chr(x[1]) for x in out]
		else:
			l = [str(x[1]) for x in out]
		if not lists:
			l = ''.join(l)
		return l

	def decrypt(self, ascii_char=True, lists=False):
		cypher = self.encrypted[:]
		out = cypher
		for i in range(len(cypher) - 1):
			out = list(zip(cypher[i], cypher[i + 1]))
			out.sort()
			cypher[i + 1] = [x[1] for x in out]
		if ascii_char:
			self.decrypted = [chr(x[1]) for x in out]
		else:
			# print(out)
			self.decrypted = [str(x[1]) for x in out]
		if not lists:
			self.decrypted = ''.join(self.decrypted)
		return self.decrypted

	@staticmethod
	def __add_line__(t):
		o = list(zip([x for x in range(len(t))], t))
		shuffle(o)
		out = [list(x) for x in zip(*o)]
		return out
