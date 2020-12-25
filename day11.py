from functools import partial

from helpers import readlines, rpath, tpath


def adj_seats_occupied(data, x, y, w, h):
  seats = ''.join([data[j][i]
                   for j in range(max(y-1,0), min(y+2, h))
                   for i in range(max(x-1,0), min(x+2, w))
                   if (i, j) != (x, y)])
  return seats.count('#')

def occupiedf(data, x, y, w, h, rx=None, ry=None):
  if rx is None:
    rng = zip([x]*w, ry)
  elif ry is None:
    rng = zip(rx, [y]*h)
  else:
    rng = zip(rx, ry)

  for i, j in rng:
    if data[j][i] == 'L':
      return 0
    if data[j][i] == '#':
      return 1
  return 0

def queen_seats_occupied(data, x, y, w, h):
  return sum([occupied(data, x, y, w, h) for occupied in (
    partial(occupiedf, rx=range(x+1, w)),
    partial(occupiedf, rx=reversed(range(0, x))),
    partial(occupiedf, ry=range(y+1, h)),
    partial(occupiedf, ry=reversed(range(0, y))),
    partial(occupiedf, rx=range(x+1, w), ry=range(y+1, h)),
    partial(occupiedf, rx=reversed(range(0, x)), ry=range(y+1, h)),
    partial(occupiedf, rx=(reversed(range(0, x))), ry=reversed(range(0, y))),
    partial(occupiedf, rx=range(x+1, w), ry=reversed(range(0, y))),
  )])

def switch(data, v, x, y, w, h, func=None, unseat_limit=None):
  if v == 'L':
    return '#' if func(data, x, y, w, h) == 0 else v
  elif v == '#':
    return 'L' if func(data, x, y, w, h) >= unseat_limit else v
  return '.'

def iterate(data, w, h, switchf):
  return [''.join([switchf(data, v, x, y, w, h) for x, v in enumerate(line)])
          for y, line in enumerate(data)]

def task(data, w, h, switchf):
  c = data
  while True:
    i = iterate(c, w, h, switchf)
    if i == c:
      break
    c = i
  return ''.join(c).count('#')

def part1(data, w, h):
  swf = partial(switch, func=adj_seats_occupied, unseat_limit=4)
  return task(data, w, h, swf)

def part2(data, w, h):
  swf = partial(switch, func=queen_seats_occupied, unseat_limit=5)
  return task(data, w, h, swf)


if __name__ == '__main__':
  data = readlines(rpath('day11.txt'))
  w, h = len(data[0]), len(data)
  print(part1(data, w, h))
  print(part2(data, w, h))
