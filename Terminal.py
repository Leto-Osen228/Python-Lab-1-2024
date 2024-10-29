import os
import sys
import time
from signal import signal, SIGWINCH
import select


class Style:
	def set(style:list):
		sys.stdout.write(f"\x1b[{';'.join(style)}m")

	def reset():
		sys.stdout.write("\x1b[0m")

class Cursor:
	def view(flag):
		sys.stdout.write(f"\x1b[?25{('l', 'h')[flag]}")


	def move(row, col):
		sys.stdout.write(f"\x1b[{row};{col}H")
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
		Cursor.move(1, 1)
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
		Cursor.move(1, 1)
		Style.set(style)
		sys.stdout.write(f"┌{'─' * (size.columns-2)}┐")
		sys.stdout.write(f"│{' ' * (size.columns-2)}│" * (size.lines-2))
		sys.stdout.write(f"└{'─' * (size.columns-2)}┘")
		Style.reset()
		self.update()


	def open(self):
		sys.stdout.write("\x1b[?1049h") # Поднять изолированный режим
		sys.stdout.write("\x1b[?1000h") # Поднять события мыши
		Cursor.move(1, 1)
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
