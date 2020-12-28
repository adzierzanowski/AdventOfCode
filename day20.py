import re
import sys
import math
import json
from functools import partial, reduce
from operator import mul

from helpers import readlines, rpath, tpath


edgematchv = ((0, 2), (2, 0))
edgematchh = ((1, 3), (3, 1))
edgematch = edgematchh + edgematchv

def parse(data):
  data = data.split('\n')
  label = data[0][:-1].replace('Tile ', '')
  tile_data = data[1:]
  return (label, tile_data)

def flipped(tile):
  return list(reversed(tile))

def rotated(tile, n=1):
  for i in range(n):
    new = []
    for i, _ in enumerate(tile[0]):
      new.append([])
      for line in tile:
        new[i].append(line[i])
      new[i] = ''.join(new[i])
    new.reverse()
    tile = new

  return tile

# Shortcuts (:
r1 = rotated
r2 = partial(rotated, n=2)
r3 = partial(rotated, n=3)
f = flipped

def edge(tile, n=0):
  '''Gets an edge'''

  # ----0--->
  # |       |
  # 3   N   1
  # |       |
  # v---2-->v

  if n == 0:
    return tile[0]
  elif n == 1:
    return ''.join([l[-1] for l in tile])
  elif n == 2:
    return tile[-1]
  elif n == 3:
    return ''.join([l[0] for l in tile])

def printt(*tiles):
  '''Prints horizontally connected tiles'''
  for i in range(len(tiles[0])):
    print(' '.join([t[i] for t in tiles]))

def connections(tile, tiles):
  '''
  Calculates matching edges for the tile against all other tiles
  and gets flips and rotations needed for the match

  N = normal, F = flipped
  0,1,2,3 = rotated n times counterclockwise
  F2 = flipped and rotated 2 times CCW

  Returns a list of tuples:
      (tile_label, tile_edge, other_label, other_edge, other_flip_rotation)
  '''
  tlabel, ttile = tile
  conns = []
  for label, tile in tiles:
    if label != tlabel:
      for i in range(4):
        for j in range(4):
          if (i, j) in edgematch:
            if edge(ttile, i) == edge(tile, j):
              conns.append((tlabel, i, label, j, 'N0'))
            if edge(ttile, i) == edge(r1(tile), j):
              conns.append((tlabel, i, label, j, 'N1'))
            if edge(ttile, i) == edge(r2(tile), j):
              conns.append((tlabel, i, label, j, 'N2'))
            if edge(ttile, i) == edge(r3(tile), j):
              conns.append((tlabel, i, label, j, 'N3'))
            if edge(ttile, i) == edge(f(tile), j):
              conns.append((tlabel, i, label, j, 'F0'))
            if edge(ttile, i) == edge(r1(f(tile)), j):
              conns.append((tlabel, i, label, j, 'F1'))
            if edge(ttile, i) == edge(r2(f(tile)), j):
              conns.append((tlabel, i, label, j, 'F2'))
            if edge(ttile, i) == edge(r3(f(tile)), j):
              conns.append((tlabel, i, label, j, 'F3'))
  return conns

def all_conns(data):
  '''Returns a dict of all sensible connections for each tile in data'''
  return {t[0]: connections(t, data) for t in data}

def get_corners(conns):
  return [lbl for lbl, con in conns.items() if len(con) == 2]

def cvtfr(tile, datad):
  '''
  Convert tile data based on its flip & rotation

  tile = (tile_label, flip_rot)
  datad = dict(tile_lbl: tile_data)
  '''
  lbl, fr = tile
  tiledata = datad[lbl]
  if fr[0] == 'F':
    tiledata = flipped(tiledata)
  tiledata = rotated(tiledata, n=int(fr[1]))
  return tiledata

def stripedges(tiledata):
  '''Returns tile's data with all edges stripped by 1 elem'''
  tiledata = tiledata[1:-1]
  newtile = []
  for line in tiledata:
    newtile.append(line[1:-1])
  return newtile

def get_img(data):
  img = []
  for line in data:
    l = []
    img.append(l)

    for lbl, fr in line:
      data = cvtfr((lbl, fr), datad)
      l.append(stripedges(data))
  return img

def join_img(img):
  newimg = []
  for line in img:
    l = []
    for i in range(len(line[0])):
      l.append(''.join([t[i] for t in line]))
    newimg.append(l)
  return sum(newimg, [])

def find_monsters(img):
  monster = (
    r'(?=(..................#.))',
    r'(?=(#....##....##....###))',
    r'(?=(.#..#..#..#..#..#...))'
  )
  monster_width = len(monster[0])
  monster_height = len(monster)
  monster_hashes = ''.join(monster).count('#')
  monster_count = 0

  for i, line in enumerate(img):
    try:
      m1 = re.finditer(monster[0], line)
      m2 = re.finditer(monster[1], img[i+1])
      m3 = re.finditer(monster[2], img[i+2])
      m1 = set([m.span() for m in m1])
      m2 = set([m.span() for m in m2])
      m3 = set([m.span() for m in m3])

      isect = m1 & m2 & m3

      if isect:
        monster_count += len(isect)

    except IndexError:
      pass
  return ''.join(img).count('#') - monster_count * monster_hashes, monster_count


def part1(corners):
  return reduce(mul, [int(x) for x in corners])

def part2(data, datad, conns, corners):
  n = int(math.sqrt(len(data)))

  firstlbl = corners[0]
  firstdata = datad[firstlbl]
  firstfr = 'N0'

  for i in range(4):
    fcons = connections((firstlbl, firstdata), data)
    f1, f2 = fcons
    e1, e2 = f1[1], f2[1]
    if (e1, e2) == (1, 2):
      break
    firstdata = rotated(firstdata)
    firstfr = 'N' + str(i+1)

  if firstfr == 'N4':
    # This step is not necessary
    # We could accept finding (2, 1) as well in the previous loop
    # and it would suffice; it would just be rotated
    # in a different way
    firstdata = flipped(firstdata)
    firstfr = 'F0'
    for i in range(4):
      fcons = connections((firstlbl, firstdata), data)
      f1, f2 = fcons
      e1, e2 = f1[1], f2[1]
      if (e1, e2) == (1, 2):
        break
      firstdata = rotated(firstdata)
      firstfr = 'F' + str(i+1)

  first = (firstlbl, firstfr)

  lines = []
  while len(lines) != n:
    line = []
    lines.append(line)
    line.append(first)
    current = line[0]

    while len(line) != n:
      clbl, cfr = current
      cdata = cvtfr((clbl, cfr), datad)

      for con in connections((clbl, cdata), data):
        t1, e1, t2, e2, fr = con
        if (e1, e2) in edgematchh and (t2, fr) not in line:
          line.append((t2, fr))
          current = line[-1]
          break

    firstdata = cvtfr(first, datad)

    for con in connections((firstlbl, firstdata), data):
      t1, e1, t2, e2, fr = con
      if (e1, e2) == (2, 0):
        first = t2, fr
        firstdata = datad[t2]
        firstlbl = t2
        break

  img = get_img(lines)
  img = join_img(img)

  imgc = img
  for i in range(4):
    hashcnt, monstercnt = find_monsters(imgc)
    if monstercnt:
      return hashcnt
    imgc = rotated(imgc)

  imgc = f(imgc)
  for i in range(4):
    hashcnt, monstercnt = find_monsters(imgc)
    if monstercnt:
      return hashcnt
    imgc = rotated(imgc)


if __name__ == '__main__':
  data = readlines(rpath('day20.txt'), sep='\n\n', conv=parse)
  datad = dict(data)
  conns = all_conns(data)
  corners = get_corners(conns)

  print(part1(corners))
  print(part2(data, datad, conns, corners))
