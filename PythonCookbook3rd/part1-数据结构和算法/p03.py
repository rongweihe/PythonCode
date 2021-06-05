# *-* coding=utf-8 *-*
from collections import deque

def search(lines, pattern, history=5):
    previous_lines = deque(maxlen=history)
    for line in lines:
        if pattern in line:
            yield line, previous_lines
        previous_lines.append(line)

# example use on a file
if __name__ == '__main__':
    with open(r'somefile.txt') as f:
        for line, previous in search(f, 'python',5):
            for pl in previous:
                print("pl=",pl)
            print(line,end='')
            print('-'* 20)
