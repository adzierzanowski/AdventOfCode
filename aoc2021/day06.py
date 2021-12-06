from util.helpers import readlines, rpath, tpath

def nextday(d):
  newd = {**d}
  for i in range(9):
    newd[i] = d.get(i+1, 0)
  newd[6] += d[0]
  newd[8] = d[0]
  return newd

def part1(data):
  days = {i: data.count(i) for i in range(9)}
  for i in range(80):
    days = nextday(days)
  return sum(days.values())

def part2(data):
  days = {i: data.count(i) for i in range(9)}
  for i in range(256):
    days = nextday(days)
  return sum(days.values())


if __name__ == '__main__':
  data = readlines(rpath('day06.txt', 'aoc2021'), sep=',', conv=int)
  print(part1(data))
  print(part2(data))
