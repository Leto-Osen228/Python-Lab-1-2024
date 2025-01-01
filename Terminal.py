import os
import sys
import time
from signal import signal, SIGWINCH
import select

class Point:
	def __init__(self, x, y) -> None:
		self.x = x
		self.y = y

	def __add__(self, point):
		return Point(self.x + point.x, self.y + point.y)

	def __iconcat__(self, point):
		self = self + point
		return self
	
	x, y = 0, 0

class Style:
	def set(style:list):
		if style != None:
			sys.stdout.write(f"\x1b[{';'.join(style)}m")

	def reset():
		sys.stdout.write("\x1b[0m")

class Cursor:
	def view(flag):
		sys.stdout.write(f"\x1b[?25{('l', 'h')[flag]}")


	def move(point:Point):
		sys.stdout.write(f"\x1b[{point.x};{point.y}H")
		sys.stdout.flush()



class Terminal:
	cursor = Cursor
	style = Style

	def __init__(self):
		pass


	def update(self):
		sys.stdout.flush()


	def clear(self):
		Cursor.move(Point(1, 1))
		Style.reset()
		sys.stdout.write("\x1b[2J")   # Очищаем область

	def write(self, info, pos = [1, 1], border=False):
		lines:list[str] = []
		max_len = None

		if type(info) is str:
			lines = info.split('\n')
		else:
			lines = list(info)
		
		pos = Point(pos[0], pos[1])

		# temp_cursor_pos = self.cursor.getPos()

		if border:
			max_len = len(max(lines, key=lambda line: len(line)))
			self.cursor.move(pos)
			sys.stdout.write(f"┌{'─' * (max_len + 2)}┐")
			pos += Point(1, 0)

		for i in range(len(lines)):
			self.cursor.move(pos + Point(i, 0))
			if border:
				sys.stdout.write(f"│ {lines[i]}{' '*(max_len-len(lines[i]))} │")
			else:
				sys.stdout.write(lines[i])
		
		if border:
			self.cursor.move(pos + Point(len(lines), 0))
			sys.stdout.write(f"└{'─' * (max_len + 2)}┘")

		# self.cursor.move(*temp_cursor_pos)

	def border(self, style=None, buttom_ofset=0):
		size = os.get_terminal_size()
		Cursor.move(Point(1, 1))
		Style.set(style)
		sys.stdout.write(f"┌{'─' * (size.columns-2)}┐")
		sys.stdout.write(f"│{' ' * (size.columns-2)}│" * (size.lines-2-buttom_ofset))
		sys.stdout.write(f"└{'─' * (size.columns-2)}┘")
		Style.reset()
		self.update()


	def open(self):
		sys.stdout.write("\x1b[?1049h") # Поднять изолированный режим
		sys.stdout.write("\x1b[?1000h") # Поднять события мыши
		Cursor.move(Point(1, 1))
		self.cursor.view(False)
		os.system('stty -echo')          # Скрыть ввод
		os.system("stty -icanon")
		self.update()


	def close(self):
		self.clear()
		sys.stdout.write("\x1b[?1000l") # Опустить события мыши
		Cursor.view(True)
		os.system('stty echo')         	# Вернуть ввод
		os.system("stty icanon")
		sys.stdout.write("\x1b[?1049l") # Опустить изолированный режим
		self.update()


	def __enter__(self):
		self.open()
		return self


	def __exit__(self, exc_type, exc_value, traceback):
		self.close()
		if exc_type is not None:
			print(f"Error: {exc_type}, {exc_value}")
		return False