from functools import reduce
from itertools import chain
from operator import mul

from helpers import readlines, rpath, tpath


def parse_range(rngstr):
  r1str, r2str = rngstr.split(' or ')
  r1a, r1b = ([int(x) for x in r1str.split('-')])
  r2a, r2b = ([int(x) for x in r2str.split('-')])

  return tuple(chain(range(r1a, r1b+1), range(r2a, r2b+1)))

def parse(data):
  ranges = {k: parse_range(v) for k, v in [l.split(': ') for l in data[0]] }
  mytick = [int(x) for x in data[1][1].split(',')]
  tickets = [[int(x) for x in t.split(',')] for t in data[2][1:]]
  allrng = tuple(chain(*ranges.values()))
  return ranges, mytick, tickets, allrng

def part1(ranges, tickets, allrng):
  s = 0
  for t in tickets:
    for v in t:
      if v not in allrng:
        s += v
  return s

def part2(ranges, tickets, allrng, mytick):
  field_cnt = len(tickets[0])

  # Filter valid tickets, assing a name of range to a string representing
  # if given field is valid across all tickets
  validts = [t for t in tickets if all((v in allrng for v in t))]
  valid_cols = [[v[i] for v in validts] for i in range(field_cnt)]
  rng_cols = {rname: ''.join([str(int(all((v in rng for v in col))))
                             for i, col in enumerate(valid_cols)])
              for rname, rng in ranges.items()}

  # Now if a given field is valid in only one column across all tickets,
  # then that must be it, we save that information and remove the column
  # marked as valid from remaining fields
  field_cols = {}
  while len(field_cols) != field_cnt:
    field, val = [(f, v) for f, v in rng_cols.items() if v.count('1') == 1][0]
    field_cols[field] = val.index('1')
    rng_cols = {rname: f'{int(c, 2) & ~int(val, 2):020b}'
                for rname, c in rng_cols.items()}

  my_fields = {k: v for k, v in field_cols.items() if k.startswith('departure')}
  res = [mytick[i] for i in my_fields.values()]
  return reduce(mul, res)


if __name__ == '__main__':
  data = [d.split('\n') for d in readlines(rpath('day16.txt'), sep='\n\n')]
  ranges, mytick, tickets, allrng = parse(data)

  print(part1(ranges, tickets, allrng))
  print(part2(ranges, tickets, allrng, mytick))
