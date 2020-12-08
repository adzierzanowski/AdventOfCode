'''
I'm not proud of this code, it's pretty embarassing. :/
'''

import json
import re

from helpers import readlines, rpath, tpath

content_rx = re.compile(r'(?P<bagcnt>\d+) (?P<bagname>[\w ]+) bags?')


class Bag:
  def __init__(self, name, children=None, count=None):
    self.name = name
    self.children = children
    self.count = count

  def __repr__(self):
    return f'<{self.name}>'

  @staticmethod
  def from_line(line):
    bagname, contents = line.split('contain')
    bagname = bagname.replace('bags', '').strip()
    contents = [c.strip() for c in contents.replace('.', '').split(',')]
    children = {}
    for content in contents:
      try:
        count, childname = re.findall(content_rx, content)[0]
        children[childname] = Bag(childname, count=int(count))
      except IndexError:
        children = {}

    return Bag(bagname, children=children)

def find_paths(from_, to, bags):
  '''Returns all paths from `from_` to `to`. If `to` is None, then the returned
  paths end with the element with no further children'''

  first = bags[from_]

  if to is not None:
    last = bags[to]

  paths = []
  if to is None and not first.children:
    paths.append([first])
    return paths
  elif to in first.children:
    paths.append([first, last])
    return paths
  else:
    for cname, child in first.children.items():
      for path in find_paths(cname, to, bags):
        paths.append([first] + path)
  return paths

def count_bags(from_, bags):
  first = bags[from_]
  if first.children:
    sum_ = 0
    for cname, child in first.children.items():
      sum_ += child.count * count_bags(cname, bags)
    return sum_ + 1
  else:
    return 1

def part1(bags):
  all_paths = []
  outermost = set()

  # For every bag, find all paths to shiny gold
  for bagname, bag in bags.items():
    paths = find_paths(bagname, 'shiny gold', bags)
    if paths:
      # Now, if first (outermost) element of the path is already counted
      # then don't count it
      for path in paths:
        first = path[0]
        if not first.name in outermost:
          all_paths.append(path)
          outermost.add(first.name)

  return len(all_paths)

def part2(bags):
  return count_bags('shiny gold', bags) - 1

if __name__ == '__main__':
  data = readlines(rpath('day7.txt'))
  bags = {b.name: b for b in [Bag.from_line(line) for line in data]}

  print(part1(bags))
  print(part2(bags))
