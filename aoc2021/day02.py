from util.helpers import readlines, rpath, tpath


def part1(data):
  pos, depth = 0, 0
  for line in data:
    dir_, dist = line.split(' ')
    dist = int(dist)
    match dir_:
      case 'up':
        depth -= dist
      case 'down':
        depth += dist
      case 'forward':
        pos += dist
  return pos * depth

def part2(data):
  aim, pos, depth = 0, 0, 0

  for line in data:
    dir_, dist = line.split(' ')
    dist = int(dist)
    match dir_:
      case 'up':
        aim -= dist
      case 'down':
        aim += dist
      case 'forward':
        pos += dist
        depth += aim * dist
  return pos * depth

if __name__ == '__main__':
  data = readlines(rpath('day02.txt', 'aoc2021'))
  print(part1(data))
  print(part2(data))
