import re
from dataclasses import dataclass

from helpers import readlines, rpath, tpath


rx = re.compile(r'(?P<key>\w{3}):(?P<val>[#\w\d]+)\b')
pid_rx = re.compile(r'\d{9}')
hcl_rx = re.compile(r'#[\da-f]{6}')

class Passport:
  VALID_KEYS = ('byr', 'iyr', 'eyr', 'hgt', 'hcl', 'ecl', 'pid')
  VALID_ECLS = ('amb', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth')

  def __init__(self, **kwargs):
    self.keys = []
    for k, v in kwargs.items():
      setattr(self, k, v)
      self.keys.append(k)

  def valid1(self):
    return all((k in self.keys for k in self.VALID_KEYS))

  def valid2(self):
    hgt = getattr(self, 'hgt', '0')
    if hgt.endswith('cm'):
      hgt_condition = 150 <= int(hgt[:-2]) <= 193
    elif hgt.endswith('in'):
      hgt_condition = 59 <= int(hgt[:-2]) <= 76
    else:
      return False

    return all((
      1920 <= int(getattr(self, 'byr', 0)) <= 2002,
      2010 <= int(getattr(self, 'iyr', 0)) <= 2020,
      2020 <= int(getattr(self, 'eyr', 0)) <= 2030,
      hgt_condition,
      re.fullmatch(hcl_rx, getattr(self, 'hcl', 'invalid')),
      getattr(self, 'ecl', 'invalid') in self.VALID_ECLS,
      re.fullmatch(pid_rx, getattr(self, 'pid', 'invalid')),
    ))

def get_passports(data):
  passports = []
  for string in data:
    passports.append(
      Passport(
        **{m.group('key'): m.group('val') for m in re.finditer(rx, string)}))
  return passports

def part1(passports):
  return len([passport for passport in passports if passport.valid1()])

def part2(passports):
  return len([passport for passport in passports if passport.valid2()])


if __name__ == '__main__':
  data = readlines(rpath('day4.txt'), sep='\n\n')
  passports = get_passports(data)
  print(part1(passports))
  print(part2(passports))
