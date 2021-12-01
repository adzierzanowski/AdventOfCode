import signal

from util.helpers import readlines, rpath, tpath


def task(data, lim):
  numbers = {n: [i+1] for i, n in enumerate(data)}
  last = data[-1]
  i = len(numbers) + 1

  signal.signal(signal.SIGINFO, lambda *_: print('i =', i))

  while i <= lim:
    ls = numbers.get(last, [])

    if len(ls) < 2:
      l0 = numbers.get(0, [])
      l0.append(i)
      numbers[0] = l0
      last = 0

    else:
      new = ls[-1] - ls[-2]
      newl = numbers.get(new, [])
      newl.append(i)
      numbers[new] = newl
      last = new

    i += 1
  return last

def part1(data):
  return task(data, 2020)

def part2(data):
  # It gets done in about half a minute
  return task(data, 30_000_000)


if __name__ == '__main__':
  data = readlines(rpath('day15.txt', 'aoc2020'),
                   conv=lambda l: [int(x) for x in l.split(',')])[0]
  print(part1(data))
  print(part2(data))
