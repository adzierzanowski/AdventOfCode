from util.helpers import readlines, rpath, tpath


def part1(data):
  return [(p - q) > 0 for p, q in zip(data[1:], data[:-1])].count(True)

def part2(data):
  d = [m + data[i+1] + data[i+2] for i, m in enumerate(data[:-2])]
  return part1(d)

def get_data():
  return readlines(rpath('day01.txt', 'aoc2021'), conv=int)

if __name__ == '__main__':
  data = get_data()
  print(part1(data))
  print(part2(data))
