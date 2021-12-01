from util.helpers import readlines, rpath, tpath


def transform(sub, val, n=1):
  for i in range(n):
    val *= sub
    val %= 20201227
  return val

def get_loop_size(sub, target):
  i = 1
  val = 1
  while True:
    val = transform(sub, val)
    if val == target:
      return i
    i += 1

def get_encryption_key(public, loop_sz):
  return transform(public, 1, n=loop_sz)

def part1(cpub, dpub):
  card_loopsz = get_loop_size(7, cpub)
  door_loopsz = get_loop_size(7, dpub)
  card_key = get_encryption_key(cpub, door_loopsz)
  door_key = get_encryption_key(dpub, card_loopsz)

  assert card_key == door_key

  return card_key


if __name__ == '__main__':
  card_pub, door_pub = readlines(rpath('day25.txt', 'aoc2020'), conv=int)
  print(part1(card_pub, door_pub))
