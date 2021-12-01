from util.helpers import readlines, rpath, tpath
from intcode import Intcode
from itertools import product
from statistics import mean
import math
from PIL import Image

def get_beam(cpu, x, y):
  cpu.reset()
  cpu.inputs = [x, y]
  cpu.run()
  return cpu.read_output()[0]


'''
def get_beam(data, dx, dy):
  cpu = intcode()
  cpu.load_program(data)

  out = {}
  for x, y in product(range(dx), range(dy)):
    cpu.reset()
    cpu.inputs = [x, y]
    cpu.run()
    out[x, y] = cpu.read_output()[0]
  return out
'''

def part1(data):
  out = get_beam(data, 50, 50)
  return tuple(out.values()).count(1)

def part2(data):
  cpu = Intcode()
  cpu.load_program(data)
  out = {}
  x, y = 0, 0
  xmin, xmax = None, 0
  rng = 100

  while True:
    if y < 5:
      xmin = None
      for x in range(4):
        val = get_beam(cpu, x, y)
        if val == 1:
          if xmin is None:
            xmin = x
          if x > xmax:
            xmax = x
          out[x, y] = val

    elif y > rng:
      break

    else:
      x0, x1 = xmin, xmax
      xmin, xmax = None, 0
      for x in range(x0-1, x1+2):
        if val := get_beam(cpu, x, y):
          if xmin is None:
            xmin = x
          if x > xmax:
            xmax = x
          out[x, y] = val

    y += 1

  img = Image.new('RGB', (2000, 2000), 'black')
  pix = img.load()
  for y in range(rng+1):
    print(f'{y:<4}', end='')
    for x in range(rng):
      val = out.get((x, y), 0)
      print('.' if val == 0 else '#', end='')
      try:
        pix[x, 2000-y] = (128, 128, 128) if val == 0 else (0, 0, 0)
      except IndexError:
        pass
    print()


  # find approximate slopes of the beam edges
  a0, a1 = [], []
  for y in range(10, rng):
    ys = {k: v for k, v in out.items() if k[1] == y}
    dx0, dy0 = min(ys, key=lambda m: m[0])
    dx1, dy1 = max(ys, key=lambda m: m[0])
    a0.append(dy0/dx0)
    a1.append(dy1/dx1)

  a0 = mean(a0)
  a1 = mean(a1)
  print('a0', a0)
  print('a1', a1)
  xa, ya, xb, yb = xaya(a0, a1)
  print('xa, ya', xa, ya)
  print('xb, yb', xb, yb)

  '''
  beam1 = [(x, int(x * a0)) for x in range(1000)]
  beam2 = [(x, int(x * a1)) for x in range(1000)]
  sqline = [(x, int(x * -1) - int(100 * math.sqrt(2))) for x in range(1000)]
  for x, y in beam1:
    try:
      pix[x, 2000-y] = (0, 255, 0)
      pix[x-1, 2000-y] = (0, 255, 0)
      pix[x, 2000-(y+1)] = (0, 255, 0)
      pix[x-1, 2000-(y+1)] = (0, 255, 0)
    except IndexError:
      pass

  for x, y in beam2:
    try:
      pix[x, 2000-y] = (0, 255, 255)
      pix[x-1, 2000-y] = (0, 255, 255)
      pix[x, 2000-(y+1)] = (0, 255, 255)
      pix[x-1, 2000-(y+1)] = (0, 255, 255)
    except IndexError:
      pass

  for y in range(-2, 3):
    for x in range(-y, y+1):
      pix[xa+x, ya+y] = (255, 0, 0)

  farout = {}
  for y in range(min(ya, yb), max(ya, yb)):
    for x in range(min(xa, xb), max(xa, xb)):
      farout[x, y] = get_beam(cpu, x, y)

  for x, y in farout:
    pix[x, 2000-y] = (32, 32, 32)

  img.show()

  '''
  return min(xa, xb) * 10000 + min(ya, yb)

def xaya(a0, a1):
  alpha = (a0+1)/(a1+1)
  top = 100 * math.sqrt(2)
  bot1 = (alpha - 1)**2
  bot2 = (a1 * alpha - a0)**2
  bot = math.sqrt(bot1+bot2)
  xa = top / bot
  ya = a0*xa
  xb = xa*alpha
  yb = a1*xb
  return (int(xa), int(ya), int(xb), int(yb))

if __name__ == '__main__':
  data = readlines(rpath('day19.txt', 'aoc2019'), conv=int, sep=',')
  #print(part1(data))
  print(part2(data))
