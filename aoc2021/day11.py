from util.helpers import readlines, rpath, tpath


def adjacent(points, data):
  adj = []
  for x, y in points:
    for dy in range(-1,2):
      for dx in range(-1, 2):
        if (x+dx, y+dy) in data and (x+dx, y+dy) not in points:
          adj.append((x+dx, y+dy))
  return adj

def step(data):
  whoflashed = []
  for pos, energy in data.items():
    data[pos] += 1
    if energy == 9:
      whoflashed.append(pos)

  newflashes = whoflashed
  while adj := adjacent(newflashes, data):
    newflashes = []
    for pos in adj:
      data[pos] += 1
      if data[pos] == 10:
        whoflashed.append(pos)
        newflashes.append(pos)

  for pos in whoflashed:
    data[pos] = 0

  return len(whoflashed)


def part1(data):
  d = {**data}
  flashcnt = 0
  for _ in range(100):
    flashcnt += step(d)
  return flashcnt

def part2(data):
  d = {**data}
  i = 0
  while True:
    i += 1
    step(d)
    if all((v == 0 for v in d.values())):
      return i

def get_data():
  data = readlines(rpath('day11.txt', 'aoc2021'))
  data = {
    (x, y): int(c) for y, line in enumerate(data) for x, c in enumerate(line)}
  return data

if __name__ == '__main__':
  data = get_data()
  print(part1(data))
  print(part2(data))
