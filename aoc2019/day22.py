from time import perf_counter
from util.helpers import readlines, rpath, tpath


class Deck:
  def __init__(self, size=10007):
    self.size = size
    self.cards = [i for i in range(size)][::-1]

  def new_stack(self):
    self.cards = self.cards[::-1]

  def cut(self, n):
    self.cards = self.cards[-n:] + self.cards[:-n]

  def deal(self, inc):
    tmp = [None for n in range(self.size)]
    p = 0
    while self.cards:
      tmp[p] = self.cards.pop()
      p += inc
      if p > self.size:
        p %= self.size
    self.cards = tmp[::-1]

  def run_commands(self, data):
    for line in data:
      if line == 'deal into new stack':
        self.new_stack()
      elif line.startswith('cut'):
        n = int(line.split(' ')[-1])
        self.cut(n)
      elif line.startswith('deal'):
        n = int(line.split(' ')[-1])
        self.deal(n)

class Deck2:
  def __init__(self, size, pos):
    self.size = size
    self.pos = pos

  def new_stack(self):
    self.pos = self.size - self.pos - 1

  def cut(self, n):
    if n > 0:
      if self.pos >= n:
        self.pos -= n
      else:
        self.pos += self.size - n
    else:
      n = abs(n)
      if self.pos < self.size - n:
        self.pos += n
      else:
        self.pos -= self.size - n

  def deal(self, inc):
    self.pos = self.pos * inc % self.size

Deck2.run_commands = Deck.run_commands

def part1(data):
  deck = Deck()
  deck.run_commands(data)
  return deck.cards[::-1].index(2019)

def part2(data):
  inipos = 2020
  deck = Deck2(119315717514047, 2020)
  deck.run_commands(data)
  return deck.pos

if __name__ == '__main__':
  data = readlines(rpath('day22.txt', 'aoc2019'))

  print(part1(data))
  print(part2(data))
