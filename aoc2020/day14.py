from itertools import product

from util.helpers import readlines, rpath, tpath


def handle_mem1(mem, mask, addr, val):
  val = f'{int(val):036b}'
  val = ''.join([v if m == 'X' else m for m, v in zip(mask, val)])
  mem[addr] = int(val, 2)

def handle_mem2(mem, mask, addr, val):
  val = int(val)
  addr = f'{addr:036b}'
  addr = ''.join([a if m == '0' else m for m, a in zip(mask, addr)])

  prods = product('01', repeat=addr.count('X'))
  for prod in prods:
    a = addr
    for p in prod:
      a = a.replace('X', p, 1)
    mem[int(a, 2)] = val

def task(data, mem_handler):
  mask = None
  mem = {}

  for line in data:
    what, val = line.split(' = ')

    if what == 'mask':
      mask = val

    elif what.startswith('mem'):
      addr = int(what.split('[')[1].replace(']', ''))
      mem_handler(mem, mask, addr, val)

  return sum((v for _, v in mem.items()))

def part1(data):
  return task(data, handle_mem1)

def part2(data):
  return task(data, handle_mem2)


if __name__ == '__main__':
  data = readlines(rpath('day14.txt', 'aoc2020'))
  print(part1(data))
  print(part2(data))
