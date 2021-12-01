from typing import Callable, Iterable
from PIL import Image
import jinja2


class Maze:
  def __init__(self, data, wallchars='#', emptychars='. ', ysep='\n', colormap=None):
    self.sdata = [list(x) for x in data.strip().split(ysep)]
    self.emptychars = emptychars
    self.wallchars = wallchars
    self.ysep = ysep
    self.colormap = {c: (128,128,128) for c in wallchars}
    if colormap:
      self.colormap = {**self.colormap, **colormap}

  def __getitem__(self, pos):
    x, y = pos
    return self.sdata[y][x]

  def __setitem__(self, pos, val):
    x, y = pos
    self.sdata[y][x] = val

  def print(self):
    for line in self.sdata:
      print(''.join(line))

  def copy(self):
    data = '\n'.join([''.join(line) for line in self.sdata])
    return Maze(data, wallchars=self.wallchars, emptychars=self.emptychars, ysep=self.ysep, colormap=self.colormap)

  def draw(self, imgpath=None):
    w, h = len(self.sdata[0]), len(self.sdata)
    img = Image.new('RGB', (w, h), 'black')
    pix = img.load()

    for y, line in enumerate(self.sdata):
      for x, char in enumerate(line):
        pix[x, y] = self.colormap.get(char, (0, 0, 0))

    if imgpath:
      img = img.resize((w*10, h*10), resample=Image.NEAREST)
      img.save(imgpath)
    else:
      img = img.resize((w*10, h*10), resample=Image.NEAREST)
      img.show()

  def neighbors_wnse(self, src):
    sx, sy = src
    neighbors = [(x, y)
                 for (x, y) in ((sx-1, sy), (sx+1, sy), (sx, sy-1), (sx, sy+1))
                 if self.sdata[y][x] not in self.wallchars]
    return neighbors

  def fill(self, src: tuple, fillchar:str=None, radius:int=None, exclude:Iterable=None, filled:Iterable=None, blockers:Iterable=None, callback:Callable=None):
    '''
    Traverse the maze until `radius` is `0`. If `radius` is `None`, visit only
    the nearest neighbors. Every step visits neighbouring places and calls
    the `callback` if defined. Neighbors can be excluded in the `exclude` list
    of positions. `blockers` is a list of neighbors that cannot be walked-through.
    '''
    exclude = exclude if exclude else []
    filled = filled if filled else []
    blockers = blockers if blockers else ''
    deferred = []

    for pos in self.neighbors_wnse(src):
      nfilled = pos in filled
      nblocker = self[pos] in blockers
      nexcluded = pos in exclude
      if not nfilled and not nblocker:
        if not nexcluded:
          filled.append(pos)
          if fillchar:
            self[pos] = fillchar
        if radius:
          deferred.append(pos)
      if callback:
        callback(pos, radius, nfilled, nblocker, nexcluded)

    for pos in deferred:
      self.fill(pos, fillchar=fillchar, radius=radius-1, exclude=exclude, filled=filled, blockers=blockers, callback=callback)

  def find(self, char):
    matches = [
      (x, y) for x, y
      in [(x, y)
          for y, line in enumerate(self.sdata)
          for x, char in enumerate(line)]
      if self.sdata[y][x] == char]

    if len(matches) == 0:
      return None
    elif len(matches) == 1:
      return matches[0]
    else:
      return matches

  def html(self, fname):
    env = jinja2.Environment(
      loader=jinja2.PackageLoader('util', '.'),
      autoescape=jinja2.select_autoescape())
    template = env.get_template('maze_template.html')
    with open(fname, 'w') as f:
      f.write(template.render(
        maze=self.sdata,
        wallchars=self.wallchars,
        emptychars=self.emptychars,
        colormap=self.colormap
      ))

def charcolor(char, basefactor=32):
  val = bin(ord(char))[3:]
  factor = basefactor * (2 if char.isupper() else 1)
  color = [0, 0, 0]
  for i, b in enumerate(val):
    color[i % 3] += int(b) * factor
  return tuple(color)

if __name__ == '__main__':
  alphabet = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
  cmap = {
    '#': (32,32,32),
    '@': (128,128,0),
    '%': (0, 128,128),
    **{c: charcolor(c) for c in alphabet}
  }



  with open('aoc2019/data/real/day18.txt', 'r') as f:
    maze = Maze(f.read(), colormap=cmap)
    src = maze.find('@')
    fill_radius = 450
    fillmap = {}
    def fill_callback(pos, radius, nfilled, nblocker, nexcluded):
      #if pos in maze.neighbors_wnse(src):
      #  print('pos', pos, 'radius', fill_radius - radius, 'nfilled', nfilled, 'nblocker', nblocker, 'nexcluded', nexcluded)
      if not nfilled and maze[pos] in alphabet:
        fillmap[maze[pos]] = {'dist': fill_radius - radius, 'pos': pos}
    maze.fill(src, exclude=[src], fillchar=None, radius=fill_radius, blockers=alphabet, callback=fill_callback)

    print(fillmap)

    maze.html('maze.html')
