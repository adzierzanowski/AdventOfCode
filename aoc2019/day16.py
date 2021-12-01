from util.helpers import readraw, rpath, tpath
import cProfile


def pattern(rep):
  base = (0, 1, 0, -1)
  ptr = 0 if rep > 1 else 1
  rcnt = 1
  while True:
    yield base[ptr % 4]
    rcnt += 1
    if rcnt >= rep:
      ptr += 1
      rcnt = 0

def evaluate(signal, rep=1):
  out = []
  for i, _ in enumerate(signal):
    val = 0
    patgen = pattern(i+1)
    for _ in range(rep):
      for digit in signal:
        val += next(patgen) * digit
    out.append(abs(val) % 10)

  return out

def part1(data):
  signal = data
  for i in range(100):
    signal = evaluate(signal)
  return ''.join((str(x) for x in signal[:8]))

def part2(data):
  signal = data
  for i in range(1):
    signal = evaluate(signal, rep=10000)
  return ''.join((str(x) for x in signal[:8]))

if __name__ == '__main__':
  data = readraw(rpath('day16.txt', 'aoc2019'))
  data = [int(c) for c in data.strip()]
  #data = [int(c) for c in '12345678']
  print(part1(data))
  #print(part2(data))
