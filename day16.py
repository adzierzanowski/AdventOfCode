from itertools import chain

from helpers import readlines, rpath, tpath


def parse_range(s):
  s = s.split(' or ')
  s1, s2 = s[0].split('-'), s[1].split('-')
  r1 = range(int(s1[0]), int(s1[1])+1)
  r2 = range(int(s2[0]), int(s2[1])+1)
  return r1, r2

def parse(data):
  ranges = [s.split(': ') for s in data[0].split('\n')]
  ranges = {s[0]: parse_range(s[1]) for s in ranges}
  my_ticket = [int(x) for x in data[1].split('\n')[1].split(',')]
  tickets = [[int(x) for x in line.split(',')] for line in data[2].split('\n')[1:]]
  return ranges, my_ticket, tickets

def part1(ranges, tickets):
  rng = list(chain(*[chain(r1, r2) for r1, r2 in ranges.values()]))
  all_tickets = sum(tickets, [])
  return sum((x for x in all_tickets if x not in rng))

def part2(ranges, tickets):
  rng = list(chain(*[chain(r1, r2) for r1, r2 in ranges.values()]))

  ts = [t for t in tickets if all([x in rng for x in t])]
  ts_fields = [[t[i] for t in ts] for i in range(len(ts[0]))]

  fields = {k: None for k in ranges}

  for rname, r in ranges.items():
    rng = list(chain(*r))
    for i, fld in enumerate(ts_fields):
      if all([x in rng for x in fld]):
        fields[rname] = i
        break
  print(fields)

if __name__ == "__main__":
  data = readlines(rpath('day16.txt'), sep='\n\n')
  ranges, my_ticket, tickets = parse(data)

  print(part1(ranges, tickets))
  print(part2(ranges, tickets))
