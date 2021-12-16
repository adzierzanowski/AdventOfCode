import math
from functools import reduce
from operator import mul

from util.helpers import readraw, rpath, tpath


class Packet:
  OP = 0
  SUM = 0
  PROD = 1
  MIN = 2
  MAX = 3
  LIT = 4
  GT = 5
  LT = 6
  EQ = 7

  def __init__(self, version, type_):
    self.version = version
    self.type = type_
    self.optype = None
    self.subpackets = []
    self.sublen = 0

  def value(self):
    if self.type == self.LIT:
        return int(''.join(self.subpackets), 2)

    values = [p.value() for p in self.subpackets]
    match self.type:
      case self.SUM:
        return sum(values)
      case self.PROD:
        return reduce(mul, values)
      case self.MIN:
        return min(values)
      case self.MAX:
        return max(values)
      case self.GT:
        return 1 if values[0] > values[1] else 0
      case self.LT:
        return 1 if values[0] < values[1] else 0
      case self.EQ:
        return 1 if values[0] == values[1] else 0

def parse(data, until=math.inf):
  packets = []
  packet = None

  i = 0
  while i < len(data) and len(packets) < until:
    if packet is None:
      try:
        ver, typ = int(data[i:i+3], 2), int(data[i+3:i+6], 2)
        packet = Packet(ver, typ)
        i += 6
      except ValueError:
        return packets, i

    elif packet.type == Packet.LIT:
      stop = data[i] == '0'
      packet.subpackets.append(data[i+1:i+5])
      i += 5

      if stop:
        packets.append(packet)
        packet = None
      else:
        pass

    else:
      if packet.optype is None:
        packet.optype = int(data[i])
        i += 1

      elif packet.optype == 0:
        if packet.sublen:
          subp, subl = parse(data[i:i+packet.sublen])
          packet.subpackets = subp
          i += packet.sublen
          packets.append(packet)
          packet = None
        else:
          packet.sublen = int(data[i:i+15], 2)
          i += 15

      elif packet.optype == 1:
        if packet.sublen:
          subp, subl = parse(data[i:], until=packet.sublen)
          packet.subpackets = subp
          i += subl
          packets.append(packet)
          packet = None
        else:
          packet.sublen = int(data[i:i+11], 2)
          i += 11

  return packets, i


def part1(data):
  packets, _ = parse(data)

  def versum(packets):
    sum_ = 0
    for packet in packets:
      if packet.type == Packet.LIT:
        sum_ += packet.version
      else:
        sum_ += versum(packet.subpackets)
        sum_ += packet.version
    return sum_

  return versum(packets)

def part2(data):
  packets, _ = parse(data)
  return packets[0].value()

def get_data():
  data = readraw(rpath('day16.txt', 'aoc2021')).strip()
  data = ''.join([f'{int(c, 16):04b}' for c in data]).rstrip('0')
  return data

if __name__ == '__main__':
  data = get_data()
  print(part1(data))
  print(part2(data))
