import re

from util.helpers import readlines, rpath, tpath


def part1(x, y):
  '''Upward steps from 0,0 are of lengths: (y_velocity), (yv-1), ..., 5, 4, 3, 2,
  1, 0; the function is basically an x-axis-squished parabola so
  the y-axis values are symmetrical, given that, the upper half has length of
  two times the sum of consecutive integers, i.e. n*(n+1), n being the initial y
  velocity

  Ok, so the next point after the second zero of the parabola must have y value
  of ymin, thus the initial y velocity has to be ymin-1

  The maximum y value is the sum: 1 + 2 + ... + ymin-1

  I didn't bother to check if that's the case for other quadrants'''
  ymin, _ = y
  return ymin*(ymin+1)//2 # Simplified because ymin is negative in my input

def part2(x, y):
  xrange = range(x[0], x[1]+1)
  yrange = range(y[0], y[1]+1)

  minx = 0
  minxsum = 0
  while minxsum < x[0]:
    minx += 1
    minxsum = minx * (minx+1) // 2

  _, maxx = x
  miny, _ = y

  maxysum = miny*(miny+1)//2
  maxy = 0
  while maxy*(maxy+1)//2 < maxysum:
    maxy += 1

  def in_target(vx, vy):
    p = [0, 0]
    for _ in range(abs(miny)*2):
      px, py = p
      p = [px+vx, py+vy]
      if p[0] in xrange and p[1] in yrange:
        return True
      if vx > 0:
        vx -= 1
      elif vx < 0:
        vx += 1
      vy -= 1
    return False

  cnt = 0
  for x in range(minx, maxx+1):
    for y in range(miny, maxy+1):
      if in_target(x, y):
        cnt += 1
  return cnt

def get_data():
  data = readlines(rpath('day17.txt', 'aoc2021'))[0]
  data = re.findall(r'(x|y)=(-?\d+\.\.-?\d+)', data)
  x, y = [(int(x), int(y)) for x, y in [d[1].split('..') for d in data]]
  return x, y

if __name__ == '__main__':
  data = get_data()
  print(part1(*data))
  print(part2(*data))
