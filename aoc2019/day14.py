import math
from util.helpers import readlines, readraw, rpath, tpath


class Factory:
  def __init__(self, reactions):
    self.reactions = reactions

  @staticmethod
  def from_data(data):
    out = {}
    for line in data:
      subs, prod = line.split(' => ')
      subs = [sub.split(' ') for sub in subs.split(', ')]
      subs = [(int(x), y) for x, y in subs]
      prodcnt, prodname = prod.split(' ')
      out[prodname] = (int(prodcnt), subs)
    return Factory(out)

  def substrates(self, cnt, prod):
    if prod in self.reactions:
      for_cnt_of_prod, subs = self.reactions[prod]
      subs = [(subcnt * math.ceil(cnt / for_cnt_of_prod), subname) for subcnt, subname in subs]
      #print('for', cnt, 'of', prod, 'you need', subs)
      return {sname: scnt for scnt, sname in subs}
    return {}


def part1(data):
  factory = Factory.from_data(data)
  need = factory.substrates(1, 'FUEL')

  def revise(need):
    new_need = {**need}
    keys = sorted(
      [k for k in new_need if k != 'ORE'],
      key=lambda m: -len([x for x in factory.substrates(1, m) if x in new_need]))

    print([(k, len([x for x in factory.substrates(1, k) if x in new_need])) for k in keys])

    key = keys[0]
    print('revise', key)
    needcnt = need[key]
    del new_need[key]
    subs = factory.substrates(needcnt, key)
    for sub, subcnt in subs.items():
      if sub in new_need:
        new_need[sub] += subcnt
      else:
        new_need[sub] = subcnt

    return new_need

  while not len(need) == 1:
    need = revise(need)
    print(need)
    print()

  print(need)

def part2(data):
  pass

if __name__ == '__main__':
  data = readlines(rpath('day14.txt', 'aoc2019'))
  print(part1(data))
  print(part2(data))
