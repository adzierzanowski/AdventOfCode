from util.helpers import readlines, rpath, tpath


class Seat:
  MAX_ROW = 127
  MAX_COL = 7

  def __init__(self, row, col):
    self.row = row
    self.col = col
    self.seat_number = self.row * 8 + self.col

  @staticmethod
  def from_string(string):
    row_range = [0, Seat.MAX_ROW]
    col_range = [0, Seat.MAX_COL]

    for c in string:
      row_pivot = int(row_range[0] + (row_range[1] - row_range[0]) / 2)
      col_pivot = int(col_range[0] + (col_range[1] - col_range[0]) / 2)

      if c == 'F':
        row_range[1] = row_pivot
      elif c == 'B':
        row_range[0] = row_pivot + 1
      elif c == 'L':
        col_range[1] = col_pivot
      elif c == 'R':
        col_range[0] = col_pivot + 1

      if row_range[0] == row_range[1]:
        row = row_range[0]
      if col_range[0] == col_range[1]:
        col = col_range[0]

    return Seat(row, col)

def part1(seats):
  return max([s.seat_number for s in seats])

def part2(seats):
  seats = sorted([s.seat_number for s in seats])
  for i, seat in zip(range(min(seats), max(seats)+1), seats):
    if i != seat:
      return seat - 1


if __name__ == '__main__':
  data = readlines(rpath('day05.txt', 'aoc2020'))
  seats = [Seat.from_string(s) for s in data]
  print(part1(seats))
  print(part2(seats))
