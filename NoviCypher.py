from random import shuffle
from shutil import make_archive, unpack_archive, rmtree, move
from os import remove, path, makedirs


class FileCypher:  # todo automatic chunk size
	def __init__(self, folder, rows=2, output_name='o', chunk=15, key=None):
		print('Starting encoding')
		chunk = 2 ** chunk
		if chunk < 1:
			print("Minimum chunk is 1 (Actual chunk is '2**chunk')")
			return
		rows -= 1
		if rows < 1:
			print("Minimum rows is 2")
			return
		if not path.exists(folder):
			print("Folder doesn't exist")
			return
		self.folder = folder
		print('Ziping for cypher')
		make_archive('Copy', 'zip', folder)
		print('Loading file')
		a = self.__first__(chunk)
		print(f'Cypher is {len(a)}')
		a = [x for x in zip(range(len(a)), a)]
		shuffle(a)
		print('Creating cypher')
		self.ncy = Cypher(self.__second__(a), rows=rows, key=key)
		# if rows > 0:
		# 	self.ncy.add_lines(rows)
		print('Saving')
		self.save_and_zip(output_name)
		print('Done\n')

	def save_and_zip(self, o):
		with open(f'Temp/cy', 'w') as f:
			f.write(self.ncy.get_cypher())
		make_archive(f'Copy', 'zip', f'Temp')
		try:
			rmtree(f'Temp')
		except:
			print(f"Can't delete Temp folder")
		if self.folder[-1] not in ['/', '\\']:
			self.folder += '/'
		move(f'Copy.zip', f'{self.folder}../{o}.ncy')
		print('Saved to ' + path.abspath(f'{self.folder}../{o}.ncy'))

	@staticmethod
	def decrypt_file(folder, key=None):
		print('Starting decoding')
		if not path.exists(f'{folder}.ncy'):
			print("Cant find .ncy file")
			return
		print('Unpacking')
		unpack_archive(f'{folder}.ncy', 'Temp', 'zip')
		a = []
		print('Reading cy')
		with open('Temp/cy', 'r') as f:
			l = [x.replace('\n', '').split(' ') for x in f.readlines()]
		for x in l:
			a.append([int(y) for y in x])
		print('Deciphering cy')
		a = [int(x) for x in Cypher(a, key=key, decode=True).decrypt(True)]
		print('Reading e')
		with open('Temp/e', 'r') as f:
			l = [x.replace('\n', '') for x in f.readlines()]
		a = [a, l]
		print('Deciphering e')
		a = [bytes.fromhex(x) for x in Cypher(a, decode=True).decrypt(True)]
		print('Creating deciphered zip')
		with open('Copy.zip', 'wb') as f:
			f.write(b''.join(a))
		print('Removing temp files and unpacking')
		try:
			rmtree('Temp')
		except:
			print("Can't delete Temp folder")
		try:
			unpack_archive('Copy.zip', folder + '-dec', 'zip')
		except:
			print("!!!! Can't decipher file. Maybe wrong key. !!!!")
			remove('Copy.zip')
			return False
		remove('Copy.zip')
		print("Done (Don't forget to clear your trash bin after deleting deciphered folder)")
		return True

	@staticmethod
	def __first__(chunk):
		l = []
		print('Reading files')
		with open('Copy.zip', 'rb') as f:
			while True:
				a = f.read(chunk)
				if not a:
					break
				l.append(str(a.hex())+'\n')
		return l

	@staticmethod
	def __second__(a):
		print('Parsing e')
		l = [list(t) for t in zip(*a)]
		remove('Copy.zip')
		if not path.exists('Temp'):
			makedirs('Temp')
		print('Writing e')
		with open(f'Temp/e', 'w') as f:
			f.writelines(l[1])
		return l[0]


class Cypher:
	encrypted = []
	to_ascii = False
	key = False

	def __init__(self, cypher_list=None, rows=0, is_it_chars=False, key=None, decode=False):
		if cypher_list in [False, None] or len(cypher_list) == 0:
			self.encrypted = []
			return
		mode = 0
		if type(cypher_list) is list:
			mode = 1
			if type(cypher_list[0]) is list:
				mode = 2
		if mode == 0:
			self.encrypted = [x for x in cypher_list]
		else:
			self.encrypted = cypher_list
		if is_it_chars:
			self.encrypted = [ord(y) - 32 for y in self.encrypted]
			self.to_ascii = True
		if mode < 2:
			self.encrypted = [self.encrypted]
		if rows > 0:
			self.add_lines(rows)
		if key not in [None, False] and len(key) > 0:  # todo better handling
			self.key = [int(x) for x in key]
			if not decode:
				self.__enc_key__()

	def __enc_key__(self):
		yek = self.key[:]
		yek.reverse()
		for k_i in yek:
			tmp = list(zip(range(len(self.encrypted)), [x.copy() for x in self.encrypted]))  # zip[1]
			tmp_sorted = list(sorted([x[:] for x in tmp], key=lambda x: x[1][k_i]))
			for i in range(len(tmp_sorted)):
				tmp[tmp.index([x for x in tmp if x[0] == tmp_sorted[i][0]][0])][1][k_i + 1:] = self.encrypted[i][k_i + 1:]
			self.encrypted = [x[1] for x in tmp]  # tmp

	def __dec_key__(self):
		tmp = [x.copy() for x in self.encrypted]
		for k_i in self.key:
			tmp_sorted = list(sorted([x.copy() for x in tmp], key=lambda x: x[k_i]))
			for i in range(len(tmp_sorted)):
				tmp[i][k_i + 1:] = tmp_sorted[i][k_i + 1:]
		return tmp

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
		if self.to_ascii:
			for row in self.encrypted[:-1]:
				for item in row:
					print(s.format(item), end=" ")
				print('')
			for item in self.encrypted[-1]:
				print(s.format(f' {chr(item + 32)}'), end=' ')
			print("")
		else:
			for row in self.encrypted:
				for item in row:
					print(s.format(item), end=" ")
				print("")

	def decrypt(self, return_list=False):
		if self.key not in [None, False] and len(self.key) > 0:
			cypher = self.__dec_key__()
		else:
			cypher = [x.copy() for x in self.encrypted]
		out = cypher
		for i in range(len(cypher) - 1):
			out = list(zip(cypher[i], cypher[i + 1]))
			out = list(sorted(out, key=lambda x: x[0]))
			cypher[i + 1] = [x[1] for x in out]
		if self.to_ascii:
			out = [chr(x[1] + 32) for x in out]
		else:
			out = [str(x[1]) for x in out]
		if not return_list:
			out = ''.join(out)
		return out

	@staticmethod
	def __add_line__(t):  # todo optimalization
		t = list(zip([x for x in range(len(t))], t))
		shuffle(t)
		last = 0
		index = 0
		l = []
		out = t[:]
		# print('1')
		for i in range(len(t)):
			xx = [x for x in t if x[0] == i]
			for x in xx:
				i = t.index(x)
				if last > i:
					l.append([i, last])
					index += 1
				last = i
				out[i] = (index, x[1])
		# print('2')
		return [list(x) for x in zip(*out)]
