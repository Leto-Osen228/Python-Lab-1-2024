from Terminal import Terminal, Point, Style

from signal import signal, SIGWINCH

import os
import sys
import time
from math import sin, pi

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
for i in range(10):
	#print(plot_list[i])
	pass

with open('sequence.txt', 'r') as file:
	list = list(map(float, file))
	print(list)
'''

def constrain(x, low, high):
	if x < low:
		return low
	if x > high:
		return high
	return x


class Main:
	def __init__(self, app):
		self.app = app
		self.last_handler = 0
		self.string = ''
		self.esc = -1

	def view(self):
		self.app.terminal.border()
		self.app.terminal.write(['Hello, wolf', 'А это уже на русском', 'Третья строка'], (2, 2), True)

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

class Flag:
	def __init__(self, app):
		self.app = app
		self.last_read_handler = 0

		self.draw_period = 15.0
		self.start_draw_time = time.time()
		self.completed = 0.0

		self.last_update_time = self.start_draw_time
		self.draw_sigment_period = 0


	def view(self):

		size = os.get_terminal_size()
		if self.draw_period != 0 and self.completed < 1.0:
			self.draw_sigment_period = self.draw_period / (size.columns - 2)			# freq of draw one sigment
			self.completed = (time.time() - self.start_draw_time) / self.draw_period 	# complited draw valume
			self.last_draw_time = time.time()											# time of last draw one sigment
			self.draw_sigment_period = max(self.draw_sigment_period, 0.9)
		else:
			self.completed = 1.0

		self.app.terminal.border(buttom_ofset = 1)
		
		self.app.terminal.write(f"completed: {self.completed:0.2f}", (size.lines, 2))

		
		for line in range(2, size.lines-1):
			if 3*line < size.lines:
				Style.set(['43'])
			elif 3*line < 2*size.lines:
				Style.set(['41'])
			else:
				Style.set(['42'])
			self.app.terminal.cursor.move(Point(line, 2))
			sys.stdout.write(' ' * round((size.columns - 2) * min(self.completed, 1)))
		Style.reset()
		
	
	def handler(self):
		# if time.time() - self.last_read_handler >= 0.1:
		# 	self.last_handler = time.time()
		# 	key = sys.stdin.read(1)
		# 	if key == 'q':
		# 		return -1

		if self.completed < 1.0:
			if time.time() - self.last_update_time >= self.draw_sigment_period:
				self.app.view()



class Plot:
	def __init__(self, app):
		self.app = app
		self.last_read_handler = 0

	def view(self):
		size = os.get_terminal_size()
		half_width = (size.columns - 2) // 2

		fun = lambda x: abs(x)
		plot_x = list(range(-half_width, half_width))
		plot_y = []
		for x in plot_x:
			plot_y.append(constrain(fun(x), 0, size.lines-4))


		self.app.terminal.border(buttom_ofset = 1)

		for dot in zip(plot_x, plot_y):
			pos = Point(-dot[1], dot[0]) + Point(size.lines-2, half_width+2)
			self.app.terminal.cursor.move(pos)
			sys.stdout.write('*')

		self.app.terminal.write(f"fun: y = |x|", (size.lines, 2))

	def handler(self):
		if time.time() - self.last_read_handler >= 0.1:
			self.last_read_handler = time.time()
			key = sys.stdin.read(1)
			if key == 'q':
				return -1


class App:
	def __init__(self) -> None:
		self.terminal = None
		self.tab = None
		self.last_update = 0
		self.view_enter = False

	def view(self):
		if not self.terminal:
			return
		
		if time.time() - self.last_update < 0.01 or self.view_enter:
			return
		self.view_enter = True
		self.last_update = time.time()

		self.terminal.clear()
		if self.tab:
			self.tab.view()
		self.terminal.update()
		self.view_enter = False

	def run(self):
		with Terminal() as temp:
			self.terminal = temp
			self.tab = Flag(self)
			self.view()
			signal(SIGWINCH, lambda a, b: self.view())
			while True:
				if self.tab.handler() == -1:
					break

if __name__ == "__main__":
	app = App()
	app.run()
