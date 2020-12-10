from helpers import readlines, rpath, tpath


def available(data, current):
  return [d for d in data if 1 <= d - current <= 3]

def part1(data):
  path = [0] + sorted(data) + [max(data)+3]
  diffs = [path[i+1] - path[i] for i in range(len(path)-1)]
  return diffs.count(1) * diffs.count(3)

def part2(data):
  pass

if __name__ == "__main__":
  data = readlines(rpath('day10.txt'), conv=int)
  print(part1(data))
  print(part2(data))
