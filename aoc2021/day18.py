from itertools import product

from util.helpers import readlines, rpath, tpath


def split(number):
  n = number[::-1]
  out = []
  done = False

  while n:
    num, nest = n.pop()
    if num > 9 and not done:
      l = num // 2
      r = num - l
      out += [(l, nest+1), (r, nest+1)]
      done = True
    else:
      out.append((num, nest))
  return out

def explode(number):
  n = number[::-1]
  pair = []
  out = []
  done = False

  while n or pair:
    if len(pair) == 2 and not done:
      l, r = pair
      lnum, lnest = l
      rnum, rnest = r

      try:
        prevnum, prevnest = out.pop()
        out.append((prevnum + lnum, prevnest))
      except IndexError:
        pass

      out.append((0, lnest-1))

      try:
        nextnum, nextnest = n.pop()
        out.append((nextnum + rnum, nextnest))
      except IndexError:
        pass

      done = True
      pair = []

    else:
      num, nest = n.pop()
      if nest < 4 or done:
        out.append((num, nest))
      elif len(pair) < 2:
        pair.append((num, nest))

  return out

def reduce_step(n):
  if any([nest >= 4 for num, nest in n]):
    return explode(n), explode
  elif any([num > 9 for num, nest in n]):
    return split(n), split
  else:
    return n, None

def reduce(n):
  while True:
    n, a = reduce_step(n)
    if a is None:
      return n

def add(n, m):
  return reduce([(num, nest+1) for num, nest in n+m])

def magnitude(n):
  while len(n) > 1:
    for i, number in enumerate(n):
      num, nest = number
      nextnum, nextnest = n[i+1]
      if nest == nextnest:
        n[i] = 3 * num + 2 * nextnum, nest - 1
        del n[i+1]
        break

  return n[0][0]

def part1(data):
  s = data[0]
  for n in data[1:]:
    s = add(s, n)
  return magnitude(s)

def part2(data):
  return max([magnitude(add(n1, n2)) for n1, n2 in product(data, data) if n1 != n2])

def parse(n, nest=-1):
  if type(n) is int:
    return (n, nest)
  l, r = n
  p = parse(l, nest=nest+1)
  q = parse(r, nest=nest+1)
  out = []

  if type(p) is list:
    out += p
  else:
    out.append(p)

  if type(q) is list:
    out += q
  else:
    out.append(q)

  return out

def get_data():
  return readlines(
    rpath('day18.txt', 'aoc2021'), conv=lambda line: parse(eval(line)))

if __name__ == '__main__':
  data = get_data()

  print(part1(data))
  print(part2(data))
