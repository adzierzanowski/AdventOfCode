from util.helpers import readlines, rpath, tpath


def parse(data):
  return {child: parent for parent, child in data}

def path_to_com(rel, from_):
  p = []
  o = from_
  while o in rel:
    p.append(o)
    o = rel[o]
  return p

def part1(data):
  rel = parse(data)
  objs = set(sum(data, []))

  total = 0
  for obj in objs:
    total += len(path_to_com(rel, obj))

  return total

def part2(data):
  rel = parse(data)
  pyou, psan = ['YOU'], ['SAN']
  pyou = path_to_com(rel, 'YOU')
  psan = path_to_com(rel, 'SAN')

  for i, o in enumerate(pyou):
    if o in psan:
      return i + psan.index(o) - 2


if __name__ == '__main__':
  data = readlines(rpath('day06.txt', 'aoc2019'), conv=lambda m: m.split(')'))
  print(part1(data))
  print(part2(data))
