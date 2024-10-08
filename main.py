from AnsiColors import BackgroundColors

import os
import sys

size:os.terminal_size = os.get_terminal_size()
print(type(size), size.columns, size.lines)
FLAG_COLORS = (BackgroundColors.YELLOW.value,
               BackgroundColors.GREEN.value,
               BackgroundColors.RED.value)

for line in range(size.lines):
    # if size.lines % 3 == 0:
    color = FLAG_COLORS[int(3 * line / size.lines)]
    print(f'\n\r{color}{line:2}{" " * (size.columns-2)}{BackgroundColors.END.value}', end='')
sys.stdin.read(1)
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