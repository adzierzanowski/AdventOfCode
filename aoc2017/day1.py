import timeit

from si_prefix import si_format as si


def pt1(data):
  dlen = len(data)
  return sum([n for i, n in enumerate(data) if n == data[(i+1) % dlen]])

def pt2(data):
  dlen = len(data)
  step = dlen//2
  return sum([n for i, n in enumerate(data) if n == data[(i+step) % dlen]])

if __name__ == '__main__':
  with open('day1.txt', 'r') as f:
    data = [int(n) for n in f.read().strip()]


  pt1_time = timeit.timeit(lambda: pt1(data), number=1000)
  pt2_time = timeit.timeit(lambda: pt2(data), number=1000)
  print(f'pt1: {pt1(data):10} | {si(pt1_time)}s')
  print(f'pt2: {pt2(data):10} | {si(pt2_time)}s')
