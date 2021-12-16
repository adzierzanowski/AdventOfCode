import heapq
import math
from dataclasses import dataclass
from itertools import product

from util.helpers import readlines, rpath, tpath


class PriorityQueue:
  def __init__(self, graph):
    self.graph = graph
    self.inf = {pos: node for pos, node in graph.items() if node.pathrisk == math.inf}
    self.finite = [node for node in graph.values() if node.pathrisk < math.inf]
    heapq.heapify(self.finite)

  def empty(self):
    return len(self.finite) < 1

  def get(self):
    return heapq.heappop(self.finite)

  def move(self, current, node, new_risk):
    n = self.inf.pop(node.pos)
    n.pathrisk = new_risk
    heapq.heappush(self.finite, n)


@dataclass
class Node:
  pathrisk: int
  risk: int
  x: int
  y: int

  @property
  def pos(self):
    return self.x, self.y

  def __lt__(self, other):
    return self.pathrisk < other.pathrisk

  def __eq__(self, other):
    return self.pathrisk == other.pathrisk

  def neighbors(self, graph):
    x, y = self.pos
    return [graph.get(pos) for pos in ((x-1, y), (x+1, y), (x, y-1), (x, y+1))]

def nodify(graph):
  return {pos: Node(0 if pos == (0, 0) else math.inf, r, *pos) for pos, r in graph.items()}

def dijkstra(graph):
  q = PriorityQueue(graph)
  while not q.empty():
    current = q.get()

    for node in current.neighbors(graph):
      if node:
        new_risk = node.risk + current.pathrisk
        if new_risk < node.pathrisk:
          q.move(current, node, new_risk)


def part1(graph, graphsz):
  graph = nodify(graph)
  dijkstra(graph)
  return graph[(graphsz-1,)*2].pathrisk

def part2(graph, graphsz):
  g = {}

  for dx, dy in product(range(5), range(5)):
    for x, y in graph:
      v = graph[x, y] + (dx+dy)
      v = v % 10 + 1 if v > 9 else v
      g[x+dx*graphsz, y+dy*graphsz] = v

  graph = nodify(g)
  dijkstra(graph)
  return graph[(graphsz*5-1,)*2].pathrisk

def get_data():
  lines = readlines(rpath('day15.txt', 'aoc2021'))
  graph = {}
  for y, line in enumerate(lines):
    for x, r in enumerate(line):
      graph[x, y] = int(r)
  return graph, len(line)


if __name__ == '__main__':
  data = get_data()
  print(part1(*data))
  print(part2(*data))
