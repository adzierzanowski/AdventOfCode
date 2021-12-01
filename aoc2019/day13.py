import time
from io import IncrementalNewlineDecoder
from os import cpu_count
from aoc2019.intcode import Intcode
from util.helpers import readlines, rpath, tpath


class Game:
  TILES = ' =#_o'

  def __init__(self, cpu):
    self.cpu = cpu
    self.score = 0
    self.ball_history = []

  def start(self):
    while not self.cpu.halt:
      self.cpu.run()

      if self.cpu.wait_for_input:
        out = self.cpu.outputs
        tiles = {(out[i], out[i+1]): out[i+2] for i in range(0, len(out), 3)}
        paddle_pos = [pos for pos, tile in tiles.items() if tile == 3][0]
        self.ball_history += [pos for pos, tile in tiles.items() if tile == 4]

        move = 0
        if len(self.ball_history) > 2:
          x2, _ = self.ball_history[-1]
          x1, _ = self.ball_history[-2]
          x, _ = paddle_pos
          left = x2 < x1
          right = x2 > x1

          if left and x > x2:
            move = -1
          elif right and x < x2:
            move = 1

        self.draw(tiles)
        self.score = tiles.get((-1, 0))
        self.cpu.feed_inputs(move)

  def get_score(self):
    out = self.cpu.outputs
    tiles = {(out[i], out[i+1]): out[i+2] for i in range(0, len(out), 3)}
    return tiles.get((-1, 0))

  def draw(self, tiles, *args):
    print('\x1b[2J\x1b[0;0H', *args, end='')
    print(f'score: {tiles.get((-1,0))}')
    for y in range(25):
      for x in range(50):
        if (x, y) in tiles:
          tile = tiles[x, y]
          print(Game.TILES[tile], end='')
        else:
          print(' ', end='')

      print()

def part1(data):
  cpu = Intcode()
  cpu.load_program(data)
  cpu.run()

  return len([tile for i, tile in enumerate(cpu.outputs) if (i % 3, tile) == (2, 2)])

def part2(data):
  cpu = Intcode(debug=False, wfi_mode=True)
  cpu.load_program(data)
  cpu.ram[0] = 2
  game = Game(cpu)
  game.start()
  return game.get_score()


if __name__ == '__main__':
  data = readlines(rpath('day13.txt', 'aoc2019'), sep=',', conv=int)

  print(part1(data))
  print(part2(data))
