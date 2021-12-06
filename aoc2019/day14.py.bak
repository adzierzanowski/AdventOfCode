import re
import math

from util.helpers import readlines, readraw, rpath, tpath


def parse_reactions(data):
  reactions = {}
  for line in data:
    src, dst = line.split(' => ')
    src = [q.split(' ') for q in src.split(', ')]
    src = {y: int(x) for x, y in src}

    x, y = dst.split(' ')
    reactions[y] = (src, int(x))
  return reactions


def part1(data):
  reactions = parse_reactions(data)

  def find_substrates(substrates, simple=True):
    subs = {}#'ORE': 0}
    for sub, subcnt in substrates.items():
      if sub == 'ORE':
        #subs['ORE'] += subcnt
        continue
      subsub, makecnt = reactions[sub]
      makecnt = math.ceil(subcnt / makecnt)
      #mksub = {s: c * makecnt for s, c in subsub.items()}
      mksub = {}
      for s, c in subsub.items():
        print('\x1b[38;5;2msubsub\x1b[0m', s, c, s == 'ORE', sub)
        if s == 'ORE' and simple:
          if sub in mksub:
            mksub[sub] += subcnt
          else:
            mksub[sub] = subcnt

        else:
          mksub[s] = c * makecnt
      print(sub, subcnt, reactions[sub], 'need', subcnt, 'must make', makecnt, mksub)

      for ms, mscnt in mksub.items():
        if ms in subs:
          subs[ms] += mscnt
        else:
          subs[ms] = mscnt
    return subs

  def simple_terms(substrates):
    for sub, cnt in substrates.items():
      if 'ORE' not in reactions[sub][0]:
        return False
    return True

  def resolve(substrates, count=1, indent=0):
    for sub, cnt in substrates.items():
      if sub == 'ORE':
        continue
      print('        ' * indent, sub, reactions[sub][0])
      resolve(*reactions[sub], indent=indent+1)


  substrates, _ = reactions['FUEL']
  '''
  print(substrates)
  subs = {}
  for sub, cnt in substrates.items():
    print(sub, reactions[sub][0])
    for ssub, ccnt in reactions[sub][0].items():

      if ssub in subs:
        subs[ssub] += ccnt
      else:
        subs[ssub] = ccnt
  print()
  print(subs)



  '''
  while not simple_terms(substrates):
    print('\x1b[38;5;1mSTEP\x1b[0m')
    substrates = find_substrates(substrates)
    print(substrates)
  substrates = find_substrates(substrates, simple=False)
  print(substrates)


def part2(data):
  pass

if __name__ == '__main__':
  data = readlines(tpath('day14.txt', 'aoc2019'))

  print(part1(data))
  #print(part2(data))
