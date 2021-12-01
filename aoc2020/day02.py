import re
from dataclasses import dataclass

from util.helpers import readlines, rpath, tpath


rx = re.compile(r'(?P<min>\d+)-(?P<max>\d+) (?P<chr>\w): (?P<pwd>\w+)')

@dataclass
class Entry:
  min: int
  max: int
  chr: str
  pwd: str

  def __post_init__(self):
    self.min = int(self.min)
    self.max = int(self.max)

def parse(data):
  entries = []
  for line in data:
    edata = re.match(rx, line)
    entry = Entry(**{k: edata.group(k) for k in rx.groupindex})
    entries.append(entry)
  return entries

def valid_part1(e):
  return e.min <= e.pwd.count(e.chr) <= e.max

def valid_part2(e):
  return (e.pwd[e.min-1] == e.chr) ^ (e.pwd[e.max-1] == e.chr)

def part1(entries):
  return len([e for e in entries if valid_part1(e)])

def part2(entries):
  return len([e for e in entries if valid_part2(e)])


if __name__ == '__main__':
  data = readlines(rpath('day02.txt', 'aoc2020'))
  entries = parse(data)
  print(part1(entries))
  print(part2(entries))
