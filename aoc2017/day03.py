from util.helpers import readraw, rpath, tpath

def get_squares(limit):
  squares = []
  base = 1
  sq = 0
  while sq < limit:
    sq = base ** 2
    squares.append(sq)
    base += 1
  return squares

def nearest_square_index(val, squares):
  return min([(i, abs(sq-val)) for i, sq in enumerate(squares)], key=lambda m: m[1])[0]

def numpos(val):
  squares = get_squares(val)
  nearest = nearest_square_index(val, squares)

  nearest_pos = None
  pos = [0, 0]
  if nearest % 2 == 1:
    base = -(nearest // 2) - 1
    nearest_pos = (base + 1, base)

    square = squares[nearest]
    diff = val - square
    if diff >= 0:
      pos[0] = nearest_pos[0] - (1 if diff > 0 else 0)
      pos[1] = nearest_pos[1] + diff - (1 if diff > 0 else 0)
    else:
      pos[1] = nearest_pos[1]
      pos[0] = nearest_pos[0] - diff

  else:
    base = nearest // 2
    nearest_pos = (base, base)
    square = squares[nearest]
    diff = val - square
    if diff > 0:
      pos[0] = nearest_pos[0] + 1
      pos[1] = nearest_pos[1] - diff + 1
    else:
      pos[0] = nearest_pos[0] + diff
      pos[1] = nearest_pos[1]

  return pos

def part1(data):
  pos = numpos(data)
  return abs(pos[0]) + abs(pos[1])

def part2(data):
  pass


if __name__ == '__main__':
  data = readraw(rpath('day03.txt', 'aoc2017'), conv=int)
  print(part1(data))
  print(part2(data))
