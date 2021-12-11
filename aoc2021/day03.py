from util.helpers import readlines, rpath, tpath


def part1(data):
  gamma = int(''.join([str(int(col.count('1') > col.count('0'))) for col in zip(*data)]), 2)
  return gamma * (gamma ^ int('1' * len(data[0]), 2))

def part2(data):
  def binfilter(ls, predicate):
    bitpos = 0
    while len(ls) > 1:
      bits = [n[bitpos] for n in ls]
      nils, ones = (bits.count(x) for x in '01')
      common = '1' if predicate(nils, ones) else '0'
      ls = [n for n in ls if n[bitpos] == common]
      bitpos += 1
    return int(ls[0], 2)

  oxy = binfilter(data, lambda z, o: z <= o)
  co2 = binfilter(data, lambda z, o: z > o)
  return oxy * co2

def get_data():
  return readlines(rpath('day03.txt', 'aoc2021'))


if __name__ == '__main__':
  data = get_data()
  print(part1(data))
  print(part2(data))
