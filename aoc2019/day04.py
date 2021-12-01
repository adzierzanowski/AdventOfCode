import re

from util.helpers import readlines, rpath, tpath


rx = re.compile(r'(\d)\1{2,6}')

def valid1(data):
  r1, r2 = data
  valid = []
  for i in range(r1, r2+1):
    istr = str(i)
    if len(set(istr)) == len(istr):
      continue

    digits = [int(x) for x in istr]
    mono = True
    for j in range(len(digits)-1):
      if digits[j] > digits[j+1]:
        mono = False
        break
    if mono:
      valid.append(i)

  return valid

def part1(data):
  return len(valid1(data))

def part2(data):
  valid = valid1(data)
  new = []
  for n in valid:
    strn = str(n)
    match = re.search(rx, strn)
    if match:
      strpd = strn.replace(match.group(0), '')
      m2 = re.search(rx, strpd)
      if not m2 and len(strpd) in (2,3) and len(set(strpd)) != len(strpd):
        new.append(n)

    else:
      new.append(n)
  return len(new)


if __name__ == '__main__':
  data = readlines(rpath('day04.txt', 'aoc2019'),
                   conv=lambda m: [int(x) for x in m.split('-')])[0]
  print(part1(data))
  print(part2(data))
