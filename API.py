from NoviCypher import FileCypher
from os import path
import sys


def encode(p, r, k, c):
	print(f"encoding {p}\nrows={r}\nkey={k}\nchunk={c}")
	FileCypher(p, rows=r, chunk=c, key=k)


def decode(p, k):
	print(f"Decoding {p}\nkey={k}")
	FileCypher.decrypt_file(p, k)


arg = sys.argv
len_argv = len(arg)
if len_argv > 1:
	if arg[1] in ['-h', '--help']:
		print(f"folder/File rows chunk")
		quit()
	a = arg[1]
else:
	a = input('File/Folder >')
if not path.exists(a):
	print(f"Path doesn't exist: {a}")
	quit()
key = input('Key >')
if path.isfile(a):
	a, b = path.splitext(a)
	if b != '.ncy':
		print(f'File must be .ncy but it is {b}')
	decode(a, key)
elif path.isdir(a):
	if len_argv > 2:
		row = arg[2]
	else:
		row = input('Number of rows >')
	if len_argv > 3:
		chunk = arg[3]
	else:
		chunk = input('chunk >')
	encode(a, int(row), key, int(chunk))
else:
	print("Unknown path")
input()