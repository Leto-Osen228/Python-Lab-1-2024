from Terminal import Terminal, BorderArea

from signal import signal, SIGWINCH

import os
import sys
import time
from math import sin, pi

# size:os.terminal_size = os.get_terminal_size()

# print(type(size), size.columns, size.lines)

# FLAG_COLORS = (BackgroundColors.YELLOW.value,
# 			   BackgroundColors.GREEN.value,
# 			   BackgroundColors.RED.value)

# for line in range(size.lines):
# 	# if size.lines % 3 == 0:
# 	color = FLAG_COLORS[int(3 * line / size.lines)]
# 	print(f'\n\r{color}{line:2}{" " * (size.columns-2)}{BackgroundColors.END.value}', end='')
# sys.stdin.read(1)

# sin_ = lambda x: sin(pi * x / 30)
# fun = lambda x: int(size.lines * max(sin_(x), -sin_(x)))
# arr = [fun(x) for x in range(-1, size.columns+1)]
# print(arr)
# for y in range(size.lines, 0, -1):
# 	for x in range(1, size.columns+1):
# 		l = min(arr[x-1], arr[x], arr[x+1])
# 		r = max(arr[x-1], arr[x], arr[x+1])
# 		sys.stdout.write((' ', '*')[l <= y <= r])
# sys.stdin.read(1)

'''
plot_list = [[0 for i in range(10)] for i in range(10)]
result = [0 for i in range(10)]

for i in range(10):
	result[i] = i ** 3

step = round(abs(result[0] - result[9]) / 9, 2)
print(step)

for i in range(10):
	for j in range(10):
		if j == 0:
			plot_list[i][j] = step * (8-i) + step

for i in range(9):
	for j in range(10):
		if abs(plot_list[i][0] - result[9 - j]) < step:
			for k in range(9):
				if 8 - k == j:
					plot_list[i][k+1] = 1

for i in range(9):
	line = ''
	for j in range(10):
		if j == 0:
			line += '\t' + str(int(plot_list[i][j])) + '\t'
		if plot_list[i][j] == 0:
			line += '--'
		if plot_list[i][j] == 1:
			line += '!!'
	print(line)
print('\t0\t1 2 3 4 5 6 7 8 9')

for i in range(10):
	#print(plot_list[i])
	pass

with open('sequence.txt', 'r') as file:
	list = list(map(float, file))
	print(list)
'''

class Main:
	def __init__(self, app):
		self.app = app
		self.last_handler = 0
		self.string = ''
		self.esc = -1

	def view(self):
		self.app.terminal.border()
		self.app.terminal.write(['Hello, wolf', 'А это уже на русском', 'Третья строка'], (2, 2), True)
		
		self.app.terminal.cursor.move(10, 10)
		

	def handler(self):
		if (time.time() - self.last_handler >= 0.1):
			self.last_handler = time.time()
			key = sys.stdin.read(1)
			if key == 'q':
				return -1
			elif key == 'c':
				self.string = ''
				self.app.view()
			elif key == '\x1b':
				self.esc = time.time()
			else:
				self.string += key
				self.app.terminal.write(self.string, (10, 5), True)

class App:
	def __init__(self) -> None:
		self.terminal = None
		self.tab = None
		self.last_update = 0

	def view(self):
		if not self.terminal:
			return
		
		if time.time() - self.last_update < 0.01:
			return
		self.last_update = time.time()

		self.terminal.clear()
		if self.tab:
			self.tab.view()
		self.terminal.update()

	def run(self):
		with Terminal() as temp:
			self.terminal = temp
			self.tab = Main(self)
			self.view()
			signal(SIGWINCH, lambda a, b: self.view())
			while True:
				if self.tab.handler() == -1:
					break
		print(self.tab.string)