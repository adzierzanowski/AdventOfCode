from os import close
from util.helpers import readlines, rpath, tpath


bracematch = {'{': '}', '[': ']', '<': '>', '(': ')'}
corruptscore = {')': 3, ']': 57, '}': 1197, '>': 25137}
completescore = {k: ')]}>'.index(k)+1 for k in ')]}>'}

def uncorrupted(data):
  score = 0
  uncorrupted = []

  for line in data:
    toclose = []
    corrupted = False
    for c in line:
      if c in '[({<':
        toclose.append(bracematch[c])
      else:
        closing = toclose.pop()
        if c != closing:
          score += corruptscore[c]
          corrupted = True
          break
    if not corrupted:
      uncorrupted.append((line, toclose))

  return score, uncorrupted

def part1(data):
  score, _ = uncorrupted(data)
  return score

def part2(data):
  _, lines = uncorrupted(data)
  scores = []
  for line, toclose in lines:
    closestr = ''.join(reversed(toclose))
    score = 0
    for c in closestr:
      score *= 5
      score += completescore[c]
    scores.append(score)

  return sorted(scores)[len(scores)//2]

def get_data():
  return readlines(rpath('day10.txt', 'aoc2021'))


if __name__ == '__main__':
  data = get_data()
  print(part1(data))
  print(part2(data))
