import os
import sys
import time
from signal import signal, SIGWINCH
import select

class Point:
	def __init__(self, x, y) -> None:
		self.x = x
		self.y = y

	x, y = 0, 0

class Style:
	def set(style:list):
		sys.stdout.write(f"\x1b[{';'.join(style)}m")

	def reset():
		sys.stdout.write("\x1b[0m")

class Cursor:
	def view(flag):
		sys.stdout.write(f"\x1b[?25{('l', 'h')[flag]}")


	def move(point:Point):
		sys.stdout.write(f"\x1b[{point.x};{point.y}H")
		sys.stdout.flush()


	def getPos():
		# Отправляем управляющую последовательность для запроса позиции курсора
		sys.stdout.write("\x1b[6n")
		# sys.stdout.flush()

		# Чтение ответа от терминала
		answer = ''
		while True:
			ch = sys.stdin.getchar()
			if ch == 'R':  # Конец ответа
				break
			answer += ch

		# Позиция формата: ESC [ row ; column R
		answer = answer.split(';')
		row = int(answer[0][2:])  # Получаем номер строки
		col = int(answer[1])	   # Получаем номер столбца

		return row, col


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
		pos = list(pos)

		# temp_cursor_pos = self.cursor.getPos()

		if border:
			max_len = len(max(lines, key=lambda line: len(line)))
			Cursor.move(pos[0], pos[1])
			sys.stdout.write(f"┌{'─' * (max_len + 2)}┐")
			pos[0] += 1

		for i in range(len(lines)):
			self.cursor.move(pos[0]+i, pos[1])
			if border:
				sys.stdout.write(f"│ {lines[i]}{' '*(max_len-len(lines[i]))} │")
			else:
				sys.stdout.write(lines[i])
		
		if border:
			self.cursor.move(pos[0]+len(lines), pos[1])
			sys.stdout.write(f"└{'─' * (max_len + 2)}┘")

		# self.cursor.move(*temp_cursor_pos)

	def border(self, style=["5", "32"]):
		size = os.get_terminal_size()
		Cursor.move(Point(1, 1))
		Style.set(style)
		sys.stdout.write(f"┌{'─' * (size.columns-2)}┐")
		sys.stdout.write(f"│{' ' * (size.columns-2)}│" * (size.lines-2))
		sys.stdout.write(f"└{'─' * (size.columns-2)}┘")
		Style.reset()
		self.update()


	def open(self):
		sys.stdout.write("\x1b[?1049h") # Поднять изолированный режим
		sys.stdout.write("\x1b[?1000h") # Поднять события мыши
		Cursor.move(Point(1, 1))
		# self.cursor.view(False)
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

class Widget:
	_deep = 1
	# area is Widget or Terminal
	def __init__(self, area) -> None:
		self.area = area
		self.widgets = set()

	def view(self):
		if not self.widgets is None:
			for w in self.widgets:
				w.view()
		

	def handler(self):
		if not self.widgets is None:
			for w in self.widgets:
				w.handler()

	def getSize(self) -> tuple[Point]:
		return self._area.getSize()
	
	def addWidget(self, widget):
		if self.widgets is None:
			raise
		self.widgets.add(widget)


class BorderArea (Widget):
	def __init__(self, area) -> None:
		super().__init__(area=area)
		area.addWidget(self)
		self._terminal = area.terminal

	def view(self):
		start, end = super().getSize()
		Cursor.move(start.x, start.y)
		for y in range(start.y, end.y-1):
			self.cursor.move(Point(start.x, y))
			sys.stdout.write(f"│{' '*(end.x - start.x)}│")
		super().view()

class MainArea:
	def getSize() -> tuple[Point]:
		return Point(40, 20)

if __name__ == "__main__":
	with Terminal() as temp:
		MainArea
		main = BorderArea(temp)
		signal(SIGWINCH, lambda a, b: main.view())
		while True:
			pass