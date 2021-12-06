import re
from util.helpers import readlines, rpath, tpath


def score_after(nth_win, nums, boards):
  winningpos = [tuple(range(i, i+5)) for i in (0, 5, 10, 15, 20)]
  winningpos += list(zip(*winningpos))

  winners = []
  checks = [set() for b in boards]

  for num in nums:
    for i, board in enumerate(boards):
      if num in board:
        checks[i].add(board.index(num))

    for i, check in enumerate(checks):
      for win in winningpos:
        if all((w in check for w in win)) and i not in winners:
          winners.append(i)
          break

    if len(winners) == nth_win:
      board, check = boards[winners[-1]], checks[winners[-1]]
      return (sum(board) - sum([board[w] for w in check])) * num

def part1(nums, boards):
  return score_after(1, nums, boards)

def part2(nums, boards):
  return score_after(len(boards), nums, boards)


if __name__ == '__main__':
  data = readlines(rpath('day04.txt', 'aoc2021'), sep='\n\n')

  nums, boards = data[0], data[1:]
  nums = [int(n) for n in nums.split(',')]
  boards = [[int(n) for n in re.split(r'\s+', b)] for b in boards]

  print(part1(nums, boards))
  print(part2(nums, boards))
