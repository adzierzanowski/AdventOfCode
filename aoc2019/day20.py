from os import name, pathconf_names
from util.helpers import readlines, rpath, tpath
from PIL import Image
from collections import namedtuple
import subprocess

Edge = namedtuple('Edge', ('src', 'dst', 'dist'))
def chuj(self):
  return f'{self.src}--{self.dist}-->{self.dst}'
Edge.__repr__ = chuj

def get(ls, x, y, default=None):
  try:
    return ls[y][x]
  except IndexError:
    return default

class Maze:
  def __init__(self, data):
    self.data = data
    self.portals = {}
    self.portal_names = {}
    self.portal_xy = []
    self.junctions = []
    self.dead_ends = []
    self.edges_with_dead_ends = []
    self.edges = []

    for y, line in enumerate(data):
      for x, char in enumerate(line):
        if char not in ' .#':
          if (char2 := get(data,x+1,y,'.')) not in ' .#':
            pname = f'{char}{char2}'
            if get(data, x+2, y) == '.':
              self.add_portal(pname, x+2, y)
            elif get(data, x-1, y) == '.':
              self.add_portal(pname, x-1, y)

          elif (char2 := get(data, x, y+1, '.')) not in ' .#':
            pname = f'{char}{char2}'
            if get(data, x, y+2) == '.':
              self.add_portal(pname, x, y+2)
            elif get(data, x, y-1) == '.':
              self.add_portal(pname, x, y-1)

        elif char == '.':
          adj_dots = self.adjacent_dots(x, y)

          if len(adj_dots) >= 3:
            self.junctions.append((x, y))
          elif len(adj_dots) == 1 and (x, y) not in self.portal_xy:
            self.dead_ends.append((x, y))

    self.find_edges()

  def adjacent_dots(self, x, y):
    n = x, y-1
    w = x-1, y
    e = x+1, y
    s = x, y+1
    adj_dots = [pos for pos in (w,n,e,s) if get(self.data, *pos) == '.']
    return adj_dots

  def find_edges(self):
    def find_edges_for(ls):
      for pos in ls:
        visited = []
        visited.append(pos)
        for second in self.adjacent_dots(*pos):
          ln = 1
          adj = second
          visited.append(second)
          while True:
            if adj in self.junctions or adj in self.dead_ends or adj in self.portal_xy:
              edge = Edge(pos, adj, ln)

              if edge not in self.edges:
                self.edges_with_dead_ends.append(edge)

              break
            ln += 1
            adj = [dot for dot in self.adjacent_dots(*adj) if dot not in visited]
            if not adj:
              break
            adj = adj[0]
            visited.append(adj)

    find_edges_for(self.junctions+[pos for pos in self.portal_xy if pos not in (self.portals['AA'], self.portals['ZZ'])])

    # remove duplicates
    filtered = []
    for edge in self.edges_with_dead_ends:
      if Edge(edge.dst, edge.src, edge.dist) not in filtered:
        filtered.append(edge)
    self.edges_with_dead_ends = filtered

    for pname, pdata in self.portals.items():
      if pname not in ('AA', 'ZZ'):
        p0, p1 = pdata
        self.edges_with_dead_ends.append(Edge(p0, p1, 1))

    self.edges = [edge for edge in self.edges_with_dead_ends if edge.src not in self.dead_ends and edge.dst not in self.dead_ends]


  def find_paths(self, paths, dst, nest=0):
    new_paths = []
    for path in paths:
      last = path[-1]
      if last == dst:
        new_paths.append(path)

      next_edges = [edge for edge in self.edges_for_vertex(last.dst) if edge.dst != last.src and not self.in_edges(path, edge.dst)]
      if next_edges:
        for next_e in next_edges:
          new_paths += self.find_paths([path + [next_e]], dst, nest=nest+1)
      else:
        new_paths.append(path)
    return new_paths

  def edges_for_vertex(self, vertex):
    normal = [edge for edge in self.edges if edge.src == vertex]
    rev = [Edge(edge.dst, edge.src, edge.dist) for edge in self.edges if edge.dst == vertex]
    return normal + rev

  def in_edges(self, edgelist, vertex):
    return vertex in [e.dst for e in edgelist]

  def draw(self):
    w, h = len(self.data[3]), len(self.data)
    img = Image.new('RGB', (w+2, h), 'black')
    pix = img.load()
    for y, line in enumerate(data):
      for x, char in enumerate(line):
        if char == '#':
          pix[x, y] = (64, 64, 64)
        if (x, y) in sum([list(x) for x in self.portals.values()], []):
          pix[x, y] = (0,128,128)
        if (x, y) == self.portals['AA']:
          pix[x, y] = (0,128,0)
        if (x, y) == self.portals['ZZ']:
          pix[x, y] = (128,0,0)
        if (x, y) in self.junctions:
          pix[x, y] = (128,0,128)
        if (x, y) in self.dead_ends and not (x, y) in self.portal_xy:
          pix[x, y] = (128,128,0)

    img.resize((w*10, h*10), resample=Image.NEAREST).show()

  def add_portal(self, name, x, y):
    if (x, y) in self.dead_ends:
      self.dead_ends.remove((x, y))
    if name in self.portals:
      self.portals[name] = self.portals[name], (x, y)
    else:
      self.portals[name] = x, y
    self.portal_xy.append((x, y))
    self.portal_names[(x, y)] = name

  def graphviz(self, with_dead_ends=False):
    edges = self.edges_with_dead_ends if with_dead_ends else self.edges
    out = 'graph G {\n'

    dots = {}
    for i, jun in enumerate(self.junctions):
      dots[jun] = f'j{i}'
      out += f'  j{i} [label="J{jun}"];\n'
    if with_dead_ends:
      for i, end in enumerate(self.dead_ends):
        dots[end] = f'e{i}'
        out += f'  e{i} [label="E{end}"];\n'
    for i, por in enumerate(self.portal_xy):
      dots[por] = f'p{i}'
      out += f'  p{i} [label="{self.portal_names[por]}{por}"];\n'

    for edge in edges:
      #if with_dead_ends or (not with_dead_ends and (edge.src not in self.dead_ends and edge.dst not in self.dead_ends)):
      out += f'  {dots[edge.src]}->{dots[edge.dst]} [label="{edge.dist}"];\n'

    for pname, pdata in self.portals.items():
      if type(pdata[0]) == tuple:
        p0, p1 = pdata
        out += f'  {dots[p0]}->{dots[p1]} [label="1"]\n';
      else:
        out += f' {dots[pdata]} [label="{pname}" style=bold fontsize=24 shape=box];\n'

    out += '}\n'

    with open('day20.gv', 'w') as f:
      f.write(out.replace('->', '--'))

    ps = subprocess.Popen(('dot', '-Tpng', 'day20.gv'), stdout=subprocess.PIPE)
    png, _ = ps.communicate()
    with open('day20.png', 'wb') as f:
      f.write(png)
    subprocess.call(('open', 'day20.png'))

def part1(data):
  maze = Maze(data)
  #maze.draw()
  maze.graphviz(with_dead_ends=False)

  aa, zz = maze.portals['AA'], maze.portals['ZZ']
  print(f'AA={aa}')
  paths = maze.find_paths([maze.edges_for_vertex(aa)], zz)
  #print(maze.edges_for_vertex((17, 8)))
  #print(maze.edges)
  print(min(sum([e.dist for e in path]) for path in paths if path[-1].dst == zz))

def part2(data):
  pass


if __name__ == '__main__':
  with open(rpath('day20.txt', 'aoc2019')) as f:
    data = f.read().split('\n')
  print(part1(data))
  print(part2(data))
