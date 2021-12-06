from util.helpers import readlines, rpath, tpath


def adjgen(q, x, y):
  for pos in ((x, y-1), (x-1, y), (x+1, y), (x, y+1)):
    yield q.get(pos, '.')

def count_bugs(q, x, y):
  cnt = 0
  for cell in adjgen(q, x, y):
    if cell == '#':
      cnt += 1
    if cnt > 2:
      return 3
  return cnt

def pq(q):
  for y in range(5):
    for x in range(5):
      print(q[x, y], end='')
    print()
  print()

def part1(data):
  q = {(x, y): c for y, line in enumerate(data) for x, c in enumerate(line)}
  qs = [''.join(q.values())]

  while True:
    nq = {**q}
    for pos, cell in q.items():
      bugs = count_bugs(q, *pos)
      if cell == '#' and bugs != 1:
        nq[pos] = '.'
      elif cell == '.' and bugs in (1, 2):
        nq[pos] = '#'

    nqs = ''.join(nq.values())
    if nqs in qs:
      return sum(2**i if cell == '#' else 0 for i, cell in enumerate(nqs))
    qs.append(nqs)
    q = nq

def part2(data):
  pass


if __name__ == '__main__':
  data = readlines(rpath('day24.txt', 'aoc2019'))
  print(part1(data))
  print(part2(data))
