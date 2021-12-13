from re import I
from util.helpers import readlines, rpath, tpath


def find(graph, paths, finished, small_unique=True):
  new_paths = []

  for path in paths:
    last = path[-1]
    possible = graph[last]
    for node in possible:
      if node in graph['upper']:
        new_paths.append(path + [node])
      elif node == 'end':
        finished.append(path + [node])
      elif node != 'start':
        if node not in path:
          new_paths.append(path + [node])
        elif not small_unique and path[0] != 'dup':
          p = path + [node]
          p[0] = 'dup'
          new_paths.append(p)
  return new_paths, finished

def part1(data):
  paths, finished = find(data, [['start']], [])
  while len(paths) > 0:
    paths, finished = find(data, paths, finished)
  return len(finished)

def part2(data):
  paths, finished = find(data, [['start']], [])
  while len(paths) > 0:
    paths, finished = find(data, paths, finished, small_unique=False)
  return len(finished)

def get_data():
  data = readlines(rpath('day12.txt', 'aoc2021'))
  graph = {'upper': set()}
  for line in data:
    src, dst = line.split('-')
    if src.isupper():
      graph['upper'].add(src)
    if dst.isupper():
      graph['upper'].add(dst)

    if src in graph:
      graph[src].append(dst)
    else:
      graph[src] = [dst]
    if dst in graph:
      graph[dst].append(src)
    else:
      graph[dst] = [src]
  return graph


if __name__ == '__main__':
  data = get_data()
  print(part1(data))
  print(part2(data))
