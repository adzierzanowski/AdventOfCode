import re

from dataclasses import dataclass

from helpers import readlines


test_data = [
  'ecl:gry pid:860033327 eyr:2020 hcl:#fffffd\n'
  'byr:1937 iyr:2017 cid:147 hgt:183cm',

  'iyr:2013 ecl:amb cid:350 eyr:2023 pid:028048884\n'
  'hcl:#cfa07d byr:1929',

  'hcl:#ae17e1 iyr:2013\n'
  'eyr:2024\n'
  'ecl:brn pid:760753108 byr:1931\n'
  'hgt:179cm',

  'hcl:#cfa07d eyr:2025 pid:166559648\n'
  'iyr:2011 ecl:brn hgt:59in'
]

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

def part1(data):
  passports = get_passports(data)
  return len([passport for passport in passports if passport.valid1()])

def part2(data):
  passports = get_passports(data)
  return len([passport for passport in passports if passport.valid2()])


if __name__ == '__main__':
  data = readlines('day4.txt', separator='\n\n')
  print(part1(data))
  print(part2(data))
