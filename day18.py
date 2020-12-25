from functools import reduce
from operator import add, mul

from helpers import readlines, rpath, tpath


def evaluate(expr, plus_precedence=False):
  valstack = []
  opstack = []

  paren = 0
  paren_expr = ''

  for symbol in expr:
    if paren:
      if symbol == '(':
        paren += 1
      elif symbol == ')':
        paren -= 1
      paren_expr += symbol

      if paren == 0:
        # [:-1] omits the last redundant closing paren, it works anyway though
        valstack.append(evaluate(paren_expr[:-1], plus_precedence))
        paren_expr = ''

    elif symbol == '+':
      opstack = [add] + opstack

    elif symbol == '*':
      opstack = [mul] + opstack

    elif symbol == '(':
      paren += 1

    elif symbol not in ' )':
      valstack.append(int(symbol))

  if plus_precedence:
    opstack = list(reversed(opstack))
    while add in opstack:
      i = opstack.index(add)
      s = valstack[i] + valstack[i+1]
      valstack = valstack[:i] + [s] + valstack[i+2:]
      del opstack[i]

  return reduce(lambda a, b: opstack.pop()(a, b), valstack)

def part1(data):
  return sum((evaluate(line) for line in data))

def part2(data):
  return sum((evaluate(line, True) for line in data))


if __name__ == '__main__':
  data = readlines(rpath('day18.txt'))

  print(part1(data))
  print(part2(data))
