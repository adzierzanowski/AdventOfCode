from util.helpers import readlines, rpath, tpath


def fold(pic, axis, da):
  newpic = []
  for x, y in pic:
    if axis == 'x':
      newpic.append((x, y) if x < da else ((2*da-x), y))
    else:
      newpic.append((x, y) if y < da else (x, (2*da-y)))
  return list(set(newpic))

def draw(pic):
  maxx = max([x for x, _ in pic])
  maxy = max([y for _, y in pic])
  for y in range(maxy+1):
    for x in range(maxx+1):
      print('#' if (x, y) in pic else ' ', end='')
    print()

def part1(pic, folds):
  pic = fold(pic, *folds[0])
  return len(pic)

def part2(pic, folds):
  for fold_ in folds:
    pic = fold(pic, *fold_)
  return pic

def get_data():
  data = readlines(rpath('day13.txt', 'aoc2021'))
  pic = [line.split(',') for line in data if ',' in line]
  pic = [(int(x), int(y)) for x, y in pic]
  folds = [line.replace('fold along ', '').split('=')
    for line in data if line.startswith('fold')]
  folds = [(x, int(y)) for x, y in folds]
  return pic, folds


if __name__ == '__main__':
  data = get_data()
  print(part1(*data))
  draw(part2(*data))
