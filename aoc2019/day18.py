from os import path
from util.helpers import readlines, readraw, rpath, tpath
from util.maze import Maze

abet_u = ''.join([chr(x) for x in range(65, 65+26)])
abet_l = abet_u.lower()
abet = abet_l + abet_u

def part1(data):
  maze = Maze(data)
  maze.colormap = {
    '#': (64,64,64),
    **{a: (0,128,128) for a in abet_l},
    **{a: (128,0,128) for a in abet_u}
  }

  fill_radius = 450
  origin = maze.find('@')

  dists = []
  def fill_callback(maze_, src, path, distance):
    def wrapper(pos, radius, nfilled, nblocker, nexcluded):
      if nblocker and maze_[pos].islower():
        #print(maze_[pos], pos, fill_radius-radius)
        dist = distance
        dist += fill_radius - radius + 1
        p = path[:]
        mcpy: Maze = maze_.copy()
        char = mcpy[pos]
        mcpy[pos] = '.'
        door = mcpy.find(char.upper())
        #maze_.draw()
        #print(char, pos, door)
        #input()
        p.append((char, dist))
        if door:
          mcpy[door] = '.'
        mcpy.fill(pos, radius=fill_radius, blockers=abet, callback=fill_callback(mcpy, pos, p, dist))

        dists.append(p)

    return wrapper

  maze.html('day18.html')
  maze.fill(origin, radius=fill_radius, blockers=abet, callback=fill_callback(maze, origin, [], 0))

  for dist in dists:
    print(dist)

def part2(data):
  pass


if __name__ == '__main__':
  data = readraw(tpath('day18.txt', 'aoc2019'))
  print(part1(data))
  print(part2(data))
