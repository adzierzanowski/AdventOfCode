import re
from util.helpers import readlines, rpath, tpath
from itertools import permutations
from functools import reduce
from math import gcd


MOON_RX = re.compile(r'<x=(?P<x>-?\d+), y=(?P<y>-?\d+), z=(?P<z>-?\d+)>')

def lcm(a, b):
  return abs(a*b) / gcd(int(a), int(b))

class Moon:
  def __init__(self, data, id):
    self.id = id
    match = re.search(MOON_RX, data)
    self.pos = [int(x) for x in match.groupdict().values()]
    self.velocity = [0] * 3

  def __repr__(self):
    return f'Moon#{self.id}<POS={self.pos} VEL={self.velocity}>'

  def __eq__(self, other):
    return self.pos == other.pos and self.velocity == other.velocity

  def gravity(self, other):
    grav = [0 if q1 == q2 else (1 if q1 < q2 else -1) for q1, q2 in zip(self.pos, other.pos)]
    return grav

  def apply_velocity(self):
    self.pos = [p + v for p, v in zip(self.pos, self.velocity)]

  def potential_energy(self):
    return sum([abs(x) for x in self.pos])

  def kinetic_energy(self):
    return sum([abs(x) for x in self.velocity])

  def total_energy(self):
    return self.potential_energy() * self.kinetic_energy()

def apply_gravity(moons):
  for perm in permutations(moons, r=2):
    m1, m2 = perm
    m1.velocity = [q + g for q, g in zip(m1.velocity, m1.gravity(m2))]

def simulate_step(moons, times=1):
  for _ in range(times):
    apply_gravity(moons)
    for moon in moons:
      moon.apply_velocity()

def part1(data):
  moons = [Moon(line, i) for i, line in enumerate(data)]
  for _ in range(1000):
    simulate_step(moons)
  return sum([m.total_energy() for m in moons])

def part2(data):
  moons = [Moon(line, i) for i, line in enumerate(data)]
  inix, iniy, iniz = zip(*[m.pos for m in moons])
  periods = [None, None, None]

  step = 1
  while True:
    step += 1
    simulate_step(moons)

    xs, ys, zs = zip(*[m.pos for m in moons])

    if not periods[0] and inix == xs:
      periods[0] = step
    if not periods[1] and iniy == ys:
      periods[1] = step
    if not periods[2] and iniz == zs:
      periods[2] = step
    if all(periods):
      break

  return int(reduce(lcm, periods))


if __name__ == '__main__':
  data = readlines(rpath('day12.txt', 'aoc2019'))

  print(part1(data))
  print(part2(data))
