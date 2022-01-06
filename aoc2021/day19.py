import re
from util.helpers import readlines, rpath, tpath
from itertools import product
from math import sin, cos, pi


def intsin(a):
  return round(sin(a))

def intcos(a):
  return round(cos(a))

def Rx(a):
  return ((1,0,0), (0,intcos(a),-intsin(a)), (0,intsin(a),intcos(a)))

def Ry(a):
  return ((intcos(a),0,intsin(a)), (0,1,0), (-intsin(a),0,intcos(a)))

def Rz(a):
  return ((intcos(a),-intsin(a),0), (intsin(a),intcos(a),0), (0,0,1))

def matmul(m, n):
  m0, m1, m2 = m
  n0, n1, n2 = zip(*n)
  return (
    (sum(a*b for a, b in zip(m0, n0)),
     sum(a*b for a, b in zip(m0, n1)),
     sum(a*b for a, b in zip(m0, n2))),
    (sum(a*b for a, b in zip(m1, n0)),
     sum(a*b for a, b in zip(m1, n1)),
     sum(a*b for a, b in zip(m1, n2))),
    (sum(a*b for a, b in zip(m2, n0)),
     sum(a*b for a, b in zip(m2, n1)),
     sum(a*b for a, b in zip(m2, n2))))

ROT = []
angles = (0, pi/2, pi, 3*pi/2)
for a, b, c in product(angles, repeat=3):
  rot = matmul(Rx(a), matmul(Ry(b), Rz(c)))
  if rot not in ROT:
    ROT.append(rot)

class Vector:
  def __init__(self, x, y, z):
    self.x = x
    self.y = y
    self.z = z

  def __hash__(self):
    return hash(self.v)

  def __eq__(self, other):
    return self.v == other.v

#  def __lt__(self, other):
#    return self.v < other.v

  def __neg__(self):
    return Vector(*[-q for q in self.v])

  def __add__(self, other):
    return self.add(other)

  def __sub__(self, other):
    return self.sub(other)

  @property
  def v(self):
    return (self.x, self.y, self.z)

  @v.setter
  def v(self, val):
    self.x, self.y, self.z = val

  def rotate(self, rot):
    r0, r1, r2 = rot
    x = sum(a*b for a, b in zip(r0, self.v))
    y = sum(a*b for a, b in zip(r1, self.v))
    z = sum(a*b for a, b in zip(r2, self.v))
    self.v = x, y, z
    return self

  def rotated(self, rot):
    v = Vector(*self.v)
    return v.rotate(rot)

  def add(self, other):
    if isinstance(other, Vector):
      return Vector(*[p+q for p, q in zip(self.v, other.v)])
    else:
      return Vector(*[p+q for p, q in zip(self.v, other)])

  def sub(self, other):
    if isinstance(other, Vector):
      return Vector(*[p-q for p, q in zip(self.v, other.v)])
    else:
      return Vector(*[p-q for p, q in zip(self.v, other)])

  def dist(self, other):
    return sum([abs(q) for q in (self - other).v])

class Scanner:
  def __init__(self, name, vectors):
    self.name = name
    self.vectors = vectors

  def relation(self, other):
    for rotation in ROT:
      diffs = {}
      for v0, v1 in product(self.vectors, other.vectors):
        diff = v0 - (v1.rotated(rotation))
        if diff in diffs:
          diffs[diff] += 1
          if diffs[diff] >= 12:
            return diff, rotation
        else:
          diffs[diff] = 1
    return None

def part1(data, relations):
  added = []
  def traverse(start, trans=Vector(0,0,0), rots=None):
    if not rots:
      rots = [ROT[0]]

    vecs = set()
    if start not in added:
      for v in start.vectors:
        for rot in reversed(rots):
          v.rotate(rot)
        v += trans
        vecs.add(v)
      added.append(start)

    for rel in [r for r in relations if r[0] == start and r[1] not in added]:
      _, s1 = rel
      t, r = relations[rel]

      for rot in reversed(rots):
        t = t.rotated(rot)
      t = trans + t
      r = rots + [r]

      vecs = vecs.union(traverse(s1, trans=t, rots=r))

    return vecs

  vecs = traverse(data[0])
  return len(vecs)

def part2(data, relations):
  positions = {}
  def traverse(start, trans=Vector(0,0,0), rots=None):
    if not rots:
      rots = [ROT[0]]

    if start not in positions:
      positions[start] = trans

    for rel in [r for r in relations if r[0] == start and r[1] not in positions]:
      _, s1 = rel
      t, r = relations[rel]

      for rot in reversed(rots):
        t = t.rotated(rot)
      t = trans + t
      r = rots + [r]
      traverse(s1, trans=t, rots=r)
  traverse(data[0])
  return max([positions[s0].dist(positions[s1]) for s0, s1 in product(data, data)])

def get_relations(data):
  relations = {}
  found = [data[0]]
  def find_rels(start):
    for s1 in data:
      if s1 not in found:
        if rel := start.relation(s1):
          found.append(s1)
          relations[start, s1] = rel
          find_rels(s1)
  find_rels(data[0])
  return relations

def get_data():
  data = readlines(rpath('day19.txt', 'aoc2021'), sep='\n\n')
  scanners = []
  for sc in data:
    lines = sc.split('\n')
    name, vecs = lines[0], lines[1:]
    name = name.replace('--- scanner ', 'Scn').replace(' ---', '')
    vecs = [Vector(*[int(q) for q in l.split(',')]) for l in vecs]
    scanners.append(Scanner(name, vecs))
  relations = get_relations(scanners)
  return scanners, relations

if __name__ == '__main__':
  data = get_data()
  print(part1(*data))
  print(part2(*data))
