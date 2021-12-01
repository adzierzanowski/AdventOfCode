from util.helpers import readlines, rpath, tpath


def fuel_req(mass):
  return mass // 3 - 2

def additional(mass):
  add = 0
  mass = fuel_req(mass)
  while mass > 0:
    add += mass
    mass = fuel_req(mass)
  return add

def part1(data):
  return sum([fuel_req(mass) for mass in data])

def part2(data):
  return sum([fuel_req(m) + additional(fuel_req(m)) for m in data])


if __name__ == '__main__':
  data = readlines(rpath('day01.txt', 'aoc2019'), conv=int)

  print(part1(data))
  print(part2(data))
