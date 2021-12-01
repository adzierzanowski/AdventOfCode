import json
import re
from itertools import product

from util.helpers import readlines, rpath, tpath


coord_rx = r'(se|sw|ne|nw|e|w)'

dc = {
  'se': (1, -1),
  'sw': (-1, -1),
  'ne': (1, 1),
  'nw': (-1, 1),
  'e': (2, 0),
  'w': (-2, 0)
}

def parse(line):
  xy = 0, 0
  coords = re.findall(coord_rx, line)

  for c in coords:
    x, y = xy
    dx, dy = dc[c]
    xy = x+dx, y+dy

  return xy

def get_tiles(data):
  tiles = {}
  for tile in data:
    if tile in tiles:
      if tiles[tile] == 'b':
        tiles[tile] = 'w'
      else:
        tiles[tile] = 'b'
    else:
      tiles[tile] = 'b'
  return tiles

def count_b(tiles):
  return list(tiles.values()).count('b')

def adjacent_b(tiles, x, y):
  b = 0

  for dxdy in dc.values():
    dx, dy = dxdy
    xy = x+dx, y+dy

    color = tiles.get(xy, 'w')
    if color == 'b':
      b += 1
  return b

def iterate(tiles):
  crds = tiles.keys()
  xcrds, ycrds = [c[0] for c in crds], [c[1] for c in crds]

  minx, miny = min(xcrds)-2, min(ycrds)-1
  maxx, maxy = max(xcrds)+2, max(ycrds)+1

  new_tiles = {}
  for x, y in product(range(minx, maxx+1), range(miny, maxy+1)):
    color = tiles.get((x,y), 'w')
    if color == 'w':
      if adjacent_b(tiles, x, y) == 2:
        new_tiles[(x,y)] = 'b'
      else:
        new_tiles[(x,y)] = 'w'
    else:
      adj_b = adjacent_b(tiles, x, y)
      if adj_b == 0 or adj_b > 2:
        new_tiles[(x,y)] = 'w'
      else:
        new_tiles[(x,y)] = 'b'
  return new_tiles

def part1(data):
  tiles = get_tiles(data)
  return count_b(tiles)

def part2(data):
  tiles = get_tiles(data)

  bt = []
  ts = tiles
  for i in range(100):
    ts = iterate(ts)
    bt.append([list(t) for t, c in ts.items() if c == 'b'])

  with open('vis/day24/tiles.js', 'w') as f:
    f.write('let tiles = ' + json.dumps(bt) + ';')

  return count_b(ts)


if __name__ == '__main__':
  data = readlines(rpath('day24.txt', 'aoc2020'), conv=parse)

  print(part1(data))
  print(part2(data))
