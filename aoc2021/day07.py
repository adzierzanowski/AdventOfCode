from util.helpers import readlines, rpath, tpath


def part1(data):
  return min([sum([abs(x-i) for x in data]) for i in range(max(data))])

def part2(data):
  return min([sum([abs(x-i)*(abs(x-i)+1)//2 for x in data])
    for i in range(max(data))])

def get_data():
  return readlines(rpath('day07.txt', 'aoc2021'), conv=int, sep=',')


if __name__ == '__main__':
  data = get_data()
  print(part1(data))
  print(part2(data))
