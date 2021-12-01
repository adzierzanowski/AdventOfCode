from itertools import islice
from collections import deque

from util.helpers import readlines, rpath, tpath


def parse(line):
  return deque([int(x) for x in line.split('\n')[1:]])

def game(d1, d2):
  previous = set()

  while d1 and d2:
    if (tuple(d1), tuple(d2)) in previous:
      return d1, 1

    previous.add((tuple(d1), tuple(d2)))

    c1, c2 = d1.popleft(), d2.popleft()

    if c1 <= len(d1) and c2 <= len(d2):
      d, w = game(deque(tuple(d1)[:c1]), deque(tuple(d2)[:c2]))
      if w == 1:
        d1 += c1, c2
      else:
        d2 += c2, c1
      continue

    if c1 > c2:
      d1 += c1, c2
    else:
      d2 += c2, c1

  d = d1 if d1 else d2
  w = 1 if d1 else 2
  return d, w

def part1(d1, d2):
  while d1 and d2:
    c1, c2 = d1.popleft(), d2.popleft()

    if c1 > c2:
      d1 += c1, c2
    else:
      d2 += c2, c1

  d = d1 if d1 else d2
  return sum([c*(i+1) for i, c in enumerate(reversed(d))])

def part2(d1, d2):
  d, w = game(d1, d2)
  return sum([c*(i+1) for i, c in enumerate(reversed(d))])


if __name__ == '__main__':
  data = readlines(rpath('day22.txt', 'aoc2020'), sep='\n\n', conv=parse)
  deck1, deck2 = data

  print(part1(deck1.copy(), deck2.copy()))
  print(part2(deck1.copy(), deck2.copy()))
